#!/usr/bin/env python

from __future__ import print_function

from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible.template import Templar
from ansible.parsing.dataloader import DataLoader
from .tree import search_groups, build_tree
import os
import sys
import tempfile
import yaml

SYMBOL = {
        'created': '+',
        'updated': '~',
        'deleted': '-',
        }


def template(hostvars, srcdir):
    loader = DataLoader()
    loader.set_basedir(srcdir)
    templar = Templar(variables=hostvars, loader=loader)
    templar._fail_on_lookup_errors = True
    templar._fail_on_filter_errors = True
    return templar.template(hostvars, convert_bare=False, preserve_trailing_newlines=True,
                            escape_backslashes=True, fail_on_undefined=False,
                            convert_data=False, static_vars=None, cache=True, disable_lookups=False)


def diff_hosts(before, beforedir, after, afterdir):
    result = dict()
    result['updated'] = dict()
    result['created'] = set(after.keys()) - set(before.keys())
    result['deleted'] = set(before.keys()) - set(after.keys())
    with tempfile.TemporaryDirectory() as tmpdirname:
        root = os.path.join(tmpdirname, 'root')
        for host in set(after.keys()) & set(before.keys()):
            os.symlink(beforedir, root)
            rendered_before = template(before[host], root)
            os.unlink(root)
            os.symlink(afterdir, root)
            rendered_after = template(after[host], root)
            os.unlink(root)
            if rendered_before != rendered_after:
                result['updated'][host] = recursive_diff(rendered_before, rendered_after)

    return result


def find_changes(inventory_a, dir_a, inventory_b, dir_b):
    with open(inventory_a) as f:
        data_a = yaml.load(f.read(), Loader=yaml.CSafeLoader)
    with open(inventory_b) as f:
        data_b = yaml.load(f.read(), Loader=yaml.CSafeLoader)
    changed_hosts = diff_hosts(data_a['_meta']['hostvars'], dir_a,
                               data_b['_meta']['hostvars'], dir_b)

    a_tree = build_tree(data_a)
    changed_groups = dict()
    changed_groups['deleted'] = search_groups(list(changed_hosts['deleted']), a_tree)
    changed_groups['created'] = search_groups(list(changed_hosts['created']), build_tree(data_b))
    changed_groups['updated'] = search_groups(list(changed_hosts['updated'].keys()), a_tree)
    return changed_hosts, changed_groups


def run(args):
    changed_hosts, changed_groups = find_changes(*args)
    for key in changed_hosts:
        for host in changed_hosts[key]:
            print(f"{SYMBOL[key]}{host}")
    for (host, diff) in changed_hosts['updated'].items():
        print(f"***{host}***")
        for before in diff[0]:
            print(f"< {before}: {diff[0][before]}")
        for after in diff[1]:
            print(f"> {after}: {diff[1][after]}")

    if changed_groups['created']:
        print("created groups: " + ', '.join(changed_groups['created']))
    if changed_groups['deleted']:
        print("deleted groups: " + ', '.join(changed_groups['deleted']))
    if changed_groups['updated']:
        print("updated groups: " + ', '.join(changed_groups['updated']))


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()

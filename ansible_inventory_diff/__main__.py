#!/usr/bin/env python3

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


def run(args):

    with open(args[0]) as f:
        data_a = yaml.load(f.read(), Loader=yaml.CSafeLoader)
    with open(args[2]) as f:
        data_b = yaml.load(f.read(), Loader=yaml.CSafeLoader)
    changed_hosts = diff_hosts(data_a['_meta']['hostvars'], args[1],
                               data_b['_meta']['hostvars'], args[3])

    for key in changed_hosts:
        for host in changed_hosts[key]:
            print(f"{SYMBOL[key]}{host}")
    for (host, diff) in changed_hosts['updated'].items():
        print(f"***{host}***")
        for before in diff[0]:
            print(f"< {before}: {diff[0][before]}")
        for after in diff[1]:
            print(f"> {after}: {diff[1][after]}")

    a_tree = build_tree(data_a)
    deleted_groups = search_groups(changed_hosts['deleted'], a_tree)
    created_groups = search_groups(changed_hosts['created'], build_tree(data_b))
    updated_groups = search_groups(list(changed_hosts['updated'].keys()), a_tree)

    if created_groups:
        print("created groups: " + ', '.join(created_groups))
    if deleted_groups:
        print("deleted groups: " + ', '.join(deleted_groups))
    if updated_groups:
        print("updated groups: " + ', '.join(updated_groups))


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()

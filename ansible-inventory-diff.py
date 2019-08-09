#!/usr/bin/env python3

from ansible.module_utils.common.dict_transformations import recursive_diff
import sys
import yaml

SYMBOL = {
        'created': '+',
        'updated': '~',
        'deleted': '-',
        }


def build_tree(groups):
    tree = dict()
    for group in groups:
        for key in 'hosts', 'children':
            if key in groups[group]:
                for child in groups[group][key]:
                    if child not in tree:
                        tree[child] = list()
                    tree[child].append(group)
    return tree


def search_groups(changed_hosts, tree):
    if not changed_hosts:
        return None
    candidates = set(tree[changed_hosts[0]])
    for host in changed_hosts[1:]:
        candidates &= set(tree[host])
    if len(candidates) == 1:
        return candidates
    return search_groups(candidates, tree) or candidates


def diff_hosts(before, after):
    result = dict()
    result['created'] = set(after.keys()) - set(before.keys())
    result['deleted'] = set(before.keys()) - set(after.keys())
    result['updated'] = [host for host in set(after.keys()) & set(before.keys())
                         if before[host] != after[host]]
    return result


def main(args):

    with open(args[0]) as f:
        data_a = yaml.load(f.read(), Loader=yaml.CSafeLoader)
    with open(args[1]) as f:
        data_b = yaml.load(f.read(), Loader=yaml.CSafeLoader)
    changed_hosts = diff_hosts(data_a['_meta']['hostvars'], data_b['_meta']['hostvars'])

    for key in changed_hosts:
        for host in changed_hosts[key]:
            print(f"{SYMBOL[key]}{host}")
    for host in changed_hosts['updated']:
        print(f"***{host}***")
        diff = recursive_diff(data_a['_meta']['hostvars'][host], data_b['_meta']['hostvars'][host])
        for before in diff[0]:
            print(f"< {before}: {diff[0][before]}")
        for after in diff[1]:
            print(f"> {after}: {diff[1][after]}")


    a_tree = build_tree(data_a)
    deleted_groups = search_groups(changed_hosts['deleted'], a_tree)
    created_groups = search_groups(changed_hosts['created'], build_tree(data_b))
    updated_groups = search_groups(changed_hosts['updated'], a_tree)

    if created_groups:
        print("created hosts: " + ', '.join(created_groups))
    if deleted_groups:
        print("deleted hosts: " + ', '.join(deleted_groups))
    if updated_groups:
        print("updated hosts: " + ', '.join(updated_groups))


if __name__ == '__main__':
    main(sys.argv[1:])

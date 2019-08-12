#!/usr/bin/env python3


def build_tree(groups):
    tree = dict()
    for group in groups:
        if group not in tree:
            tree[group] = dict(parents=[], children=[])
        for key in 'hosts', 'children':
            if key in groups[group]:
                for child in groups[group][key]:
                    if child not in tree:
                        tree[child] = dict(parents=[], children=[])
                    tree[child]['parents'].append(group)
                    tree[group]['children'].append(child)
    return tree


def search_groups(changed_hosts, tree):
    candidates = []
    if not changed_hosts:
        return None
    parents = set(tree[changed_hosts[0]]['parents'])
    for host in changed_hosts[1:]:
        parents |= set(tree[host]['parents'])
    for parent in parents:
        if all([child in changed_hosts for child in tree[parent]['children']]):
            candidates.append(parent)

    return search_groups(candidates, tree) or candidates

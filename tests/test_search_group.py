import pytest
from ansible_inventory_diff.tree import search_groups, build_tree


def test_search_group():
    changed_hosts = ['test-app-A', 'test-web-A']
    inventory = {
        'test': {
            'children': ['test-app', 'test-api', 'test-web']
        },
        'staging': {
            'children': ['staging-app', 'staging-api', 'staging-web']
        },
        'web': {
            'children': ['test-web', 'staging-web']
        },
        'api': {
            'children': ['test-api', 'staging-api']
        },
        'app': {
            'children': ['test-app', 'staging-app']
        },
        'test-web': {
            'hosts': ['test-web-A']
        },
        'test-app': {
            'hosts': ['test-app-A']
        },
        'test-api': {
            'hosts': ['test-api-A']
        },
        'staging-web': {
            'hosts': ['staging-web-A']
        },
        'staging-app': {
            'hosts': ['staging-app-A']
        },
        'staging-api': {
            'hosts': ['staging-api-A']
        }
    }
    expected = ['test-app', 'test-web']
    tree = build_tree(inventory)

    assert set(search_groups(changed_hosts, tree)) == set(expected)

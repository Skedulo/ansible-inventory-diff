# ansible-inventory-diff github action

This action runs ansible-inventory-diff against a comparison
git reference and returns the difference in variables between
the two

## Inputs

### `base-ref`

The base reference for the diff comparison (default `origin/main`)

### `truncate`

Number of lines at which to truncate the diff output for the snippet
(default 200)

## Outputs

### `result`

The full output of the diff

### `snippet`

A truncated version of the diff suitable for a github comment

## Example usage

```
on: [push]

jobs:
  ansible_inventory_diff:
    runs-on: ubuntu-latest
    name: ansible-inventory-diff
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Run ansible inventory diff
        id: run
        uses: Skedulo/ansible-inventory-diff@v1.5
        with:
          base-ref: origin/main
      - name: ansible inventory diff
        run: echo "${{ steps.run.outputs.result }}"
```

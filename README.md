# ansible-inventory-diff github action

This action runs ansible-inventory-diff against a comparison
git reference and returns the difference in variables between
the two

## Inputs

### `base-ref`

The base reference for the diff comparison (default `origin/main`)

## Outputs

### `result`

The result of the diff

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
        run: echo "${{ steps.run.output.result }}"
```

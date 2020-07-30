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
uses: actions/ansible-inventory-diff@v1
with:
  base-ref: v0.1
```

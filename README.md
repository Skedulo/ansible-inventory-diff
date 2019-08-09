# Summary

ansible-inventory-diff will compare the inventories between a fromcommit
and the current working directory, or to an optional commit

ansible-inventory-diff uses docker to isolate the file trees of the checked
out code of the commit and ensure the right tools are installed

We use `slim` rather than `alpine` because even with libyaml installed, pyyaml
didn't seem to provide `CSafeLoader` which is at least 10x faster than the
python `SafeLoader`. Any fix that gets `CSafeLoader` working with alpine
would be welcome!

# Build

```
docker build -t ansible-inventory-diff .
```

# Usage
```
cd /path/to/repo
docker run -it -v `pwd`/.:/git:delegated ansible-inventory-diff:latest <fromcommit> [--to tocommit]
```

# Improvements

- Expand templated variables where possible when comparing outputs
- Output the highest level common groups that have changed related to the hosts
- Tests
- Examples

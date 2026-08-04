# apigee-cli-plugins

Example plugin repository for `apigeecli`.

See the `apigeecli` PyPI page for installation instructions and plugin
documentation:

- PyPI: https://pypi.org/project/apigeecli/

## Install example plugins

```bash
apigee plugins add https://github.com/mdelotavo/apigee-cli-plugins.git

apigee plugins update
```

## Run examples

After installing the plugin:

```bash
apigee examples -h
```

This repository contains example Click-based commands demonstrating how to
create, package, and distribute plugins.

## More plugin tooling

For a more generic command-line tool built on the same plugin system with a
more mature feature set, see
**multitool**:

- https://pypi.org/project/multitool/

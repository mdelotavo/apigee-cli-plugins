# apigee-cli-plugins

Example plugin repository for `apigeecli`.

See the `apigeecli` PyPI page for installation instructions and plugin
documentation:

- PyPI: https://pypi.org/project/apigeecli/

## Install example plugins

```bash
echo -e '[sources]\npublic = https://github.com/mdelotavo/apigee-cli-plugins' >> ~/.apigee/plugins/config

apigee plugins update
```

## Run examples

After installing the plugin:

```bash
apigee examples -h
```

This repository contains example Click-based commands demonstrating how to
create and distribute plugins.

## More plugin tooling

For a more generic command-line tool leveraging the same plugin system,
including quick plugin scaffolding for local prototyping, see **multitool**:

- https://pypi.org/project/multitool/

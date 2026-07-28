# apigee-cli-plugins

Example plugin repository for `apigeecli`.

See the `apigeecli` documentation and PyPI page for details on installing and
using plugins:

- PyPI: https://pypi.org/project/apigeecli/

## Install example plugins

```
echo -e '[sources]\npublic = https://github.com/mdelotavo/apigee-cli-plugins' >> ~/.apigee/plugins/config

apigee plugins update
```

## Run examples

After installing the plugin:

```
apigee examples -h
```

This repository contains example Click-based commands demonstrating how to
create and distribute plugins.

You can create your own plugins using `apigeecli`'s plugin system.

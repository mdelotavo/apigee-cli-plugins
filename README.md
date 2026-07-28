# apigee-cli-plugins

Example plugin repository for `apigeecli`.

See the `apigeecli` PyPI page for installation instructions and plugin
documentation:

- PyPI: https://pypi.org/project/apigeecli/

## Install example plugins

```bash
echo -e '[sources]\npublic = https://github.com/mdelotavo/apigee-cli-plugins.git' >> ~/.apigee/plugins/config

apigee plugins update
```

## Run examples

After installing the plugin:

```bash
apigee examples -h
```

This repository contains example Click-based commands demonstrating how to
create and distribute plugins.

## Limitations

Plugin command names must be unique across all installed repositories.

To avoid naming conflicts, plugin modules should follow the convention of including the repository owner and repository name in the command name.

For example, a repository configured as:

```bash
[sources]
public = https://github.com/mdelotavo/apigee-cli-plugins.git
```

should expose commands using a unique name such as:

```
mdelotavo-apigee-cli-plugins
```

This reduces the likelihood of collisions when multiple repositories expose plugins with the same command name.

## More plugin tooling

For a more generic command-line tool leveraging the same plugin system with a more mature feature set,
including quick plugin scaffolding for local prototyping, see **multitool**:

- https://pypi.org/project/multitool/

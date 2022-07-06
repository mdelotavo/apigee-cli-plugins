# apigee-cli-plugins

## Install the `apigeecli` package
```
pip3 install -U apigeecli
```

## Check available commands before installing plugins
```
$ apigee -h
Usage: apigee [OPTIONS] COMMAND [ARGS]...

  Welcome to the (Unofficial) Apigee Management API command-line interface!

  Docs:    https://darumatic.github.io/apigee-cli/
  PyPI:    https://pypi.org/project/apigeecli/
  GitHub:  https://github.com/darumatic/apigee-cli

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  apiproducts    API products enable you to bundle and distribute your...
  apis           The proxy APIs let you perform operations on API...
  apps           Management APIs available for working with developer apps.
  auth           Custom authorization commands.
  backups        Download configuration files from Apigee that can later...
  caches         A lightweight persistence store that can be used by...
  configure      Configure Apigee Edge credentials.
  deployments    API proxies that are actively deployed in environments...
  developers     Developers implement client/consumer apps and must be...
  keystores      A list of URIs used to create, modify, and delete...
  keyvaluemaps   Key/value maps at the environment scope can be accessed...
  maskconfigs    Specify data that will be filtered out of trace sessions.
  permissions    Permissions for roles in an organization on Apigee Edge.
  plugins        [Experimental] Simple plugins manager for distributing...
  references     References in an organization and environment.
  sharedflows    You can use the following APIs to manage shared flows...
  targetservers  TargetServers are used to decouple TargetEndpoint...
  userroles      Roles for users in an organization on Apigee Edge.
  virtualhosts   A named network configuration (including URL) for an...
```

## Install the commands in this repository
```
echo -e '[sources]\npublic = https://github.com/mdelotavo/apigee-cli-plugins' >> ~/.apigee/plugins/config
apigee plugins update
apigee plugins show
apigee plugins show -n public
apigee plugins show -n public --show-commit-only
apigee plugins show -n public --show-dependencies-only
pip3 install $(apigee plugins show -n public --show-dependencies-only)
```

## Check installed commands
```
$ apigee examples -h
Usage: apigee examples [OPTIONS] COMMAND [ARGS]...

  First paragraph.

  This is a very long second paragraph and as you can see wrapped very early
  in the source text but will be rewrapped to the terminal width in the final
  output.

  This is
  a paragraph
  without rewrapping.

  And this is a paragraph that will be rewrapped again.

Options:
  -V, --version         Show the version and exit.
  --repo-home TEXT
  --debug / --no-debug
  -h, --help            Show this message and exit.

Commands:
  ansi-colors
  callbacks-eager
  cat
  chmod
  clear
  clone
  commit
  convert
  copy                Move file SRC to DST.
  cp
  delete              delete the repo
  digest
  dropdb
  echo                Print value of SRC environment variable.
  edit                Edit FILENAME if the file exists.
  encrypt
  feature-switches
  get-commit-message
  get-streams
  getchar
  greet
  hello               Simple program that greets NAME for a total of...
  info
  init                init the repo
  initdb
  inout               Copy contents of INPUT to OUTPUT.
  launch              This can be used to open the default application...
  less
  log
  login
  parse-bool
  parse-datetime
  parse-float
  parse-int
  parse-str
  parse-uuid
  pause
  perform
  print-stdout
  progress-bar
  prompt
  prompt2
  putitem
  read-config         Print APP_NAME config file.
  read-user
  repeat
  repeat-float
  roll
  runserver
  sync
  touch               Print FILENAME if the file exists.
  write-file          Write 'Hello World!' to FILENAME.
```

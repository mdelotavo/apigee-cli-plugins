#!/usr/bin/env python

import codecs
import configparser
import importlib
import os
import re
import sys
import time
from functools import update_wrapper

import click
import requests

from multitool import (APP, MULTITOOL_LOG_FILE, MULTITOOL_PLUGINS_DIRECTORY,
                       MULTITOOL_PLUGINS_PATH)
from multitool import __version__ as version
from multitool.cls import AliasedGroup
from multitool.exceptions import exception_handler
from multitool.plugins.commands import plugins
from multitool.utils import (import_all_modules_in_directory,
                             run_func_on_dir_files, setup_global_logger,
                             show_message)

URL = 'https://en.wikipedia.org/wiki/"Hello,_World!"_program'
CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    default_map={'runserver': {'port': 5000}}
)
# CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def do_hello():
    result = requests.get(URL)
    show_message(re.findall('<title>(.*?)</title>', result.text)[0])

# @click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for _ in range(count):
#         click.echo(f"Hello, {name}!")

class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

class Repo(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

@click.group(context_settings=CONTEXT_SETTINGS, cls=AliasedGroup, invoke_without_command=False, chain=False)
@click.version_option(version, '-V', '--version')
# @click.command(cls=AliasedGroup)
@click.option('--repo-home', envvar='REPO_HOME', default='.repo')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def examples(ctx, repo_home, debug):
    """First paragraph.

    This is a very long second paragraph and as you
    can see wrapped very early in the source text
    but will be rewrapped to the terminal width in
    the final output.

    \b
    This is
    a paragraph
    without rewrapping.

    And this is a paragraph
    that will be rewrapped again.
    \f

    :param click.core.Context ctx: Click context.
    """
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug

    # if ctx.invoked_subcommand is None:
    #     click.echo('I was invoked without subcommand')
    # else:
    #     click.echo('I am about to invoke %s' % ctx.invoked_subcommand)

    ctx.obj['REPO'] = Repo(repo_home, debug)

# @examples.command()
# @click.argument('src')
# @click.argument('dest', required=False)
# @click.pass_obj
# def clone(repo, src, dest):
#     click.echo((repo, src, dest))

# pass_repo = click.make_pass_decorator(Repo)
pass_repo = click.make_pass_decorator(Repo, ensure=True)

@examples.command()
@click.argument('src')
@click.argument('dest', required=False)
@pass_repo
def clone(repo, src, dest):
    click.echo((repo, src, dest))

@examples.command()
@pass_repo
def cp(repo):
    click.echo(isinstance(repo, Repo))

@examples.command()
def initdb():
    click.echo('Initialized the database')

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@examples.command()
# @click.option('--yes', is_flag=True, callback=abort_if_false,
#               expose_value=False,
#               prompt='Are you sure you want to drop the db?')
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped the database')

@examples.command()
@click.argument('string', nargs=1)
def parse_str(string):
    click.echo(string)

@examples.command()
@click.argument('integer', nargs=1, type=click.INT)
def parse_int(integer):
    click.echo(integer)

@examples.command()
@click.argument('float', nargs=1, type=click.FLOAT)
def parse_float(float):
    click.echo(float)

@examples.command()
@click.argument('bool', nargs=1, type=click.BOOL)
def parse_bool(bool):
    click.echo(bool)

@examples.command()
@click.argument('uuid', nargs=1, type=click.UUID)
def parse_uuid(uuid):#try 12345678-1234-5678-1234-567812345678
    click.echo(uuid)

@examples.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def inout(input, output):
    """Copy contents of INPUT to OUTPUT."""
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        output.write(chunk)

@examples.command()
# @examples.command(context_settings={"ignore_unknown_options": True})
@click.argument('filename', type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False))
def touch(filename):
    """Print FILENAME if the file exists."""
    click.echo(click.format_filename(filename))

@examples.command()
@click.option('--hash-type',
              type=click.Choice(['MD5', 'SHA1'], case_sensitive=False), default='SHA1', show_default=True)
def digest(hash_type):
    click.echo(hash_type)

@examples.command()
@click.option('--count', type=click.IntRange(0, 20, clamp=True), required=True)
@click.option('--digit', type=click.IntRange(0, 10), required=True)
def repeat(count, digit):
    click.echo(str(digit) * count)

@examples.command()
@click.option('--count', type=click.IntRange(0, 20, clamp=True), required=True)
@click.option('--float', type=click.FloatRange(0, 10), required=True)
def repeat_float(count, float):
    click.echo(str(float) * count)

@examples.command()
@click.argument('datetime', nargs=1, type=click.DateTime())
def parse_datetime(datetime):
    click.echo(datetime)

class BasedIntParamType(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except TypeError:
            self.fail(
                "expected string for int() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)

# BASED_INT = BasedIntParamType()

@examples.command()
@click.argument('string', nargs=1, type=BasedIntParamType())
def convert(string):
    click.echo(string)

@examples.command()
@click.option('--item', type=(str, int))
# @click.option('--item', nargs=2, type=click.Tuple([str, int]))
def putitem(item):
    click.echo('name=%s id=%d' % item)

@examples.command()
@click.option('--message', '-m', multiple=True, default=["foo", "bar"], show_default=True)
def commit(message):
    click.echo('\n'.join(message))

@examples.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo('Verbosity: %s' % verbose)

# @examples.command()
# @click.option('/debug;/no-debug')
# def log(debug):
#     click.echo('debug=%s' % debug)

@examples.command()
@click.option('--shout/--no-shout', ' /-S', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)

@examples.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def feature_switches(transformation):
    click.echo(getattr(sys.platform, transformation)())

@examples.command()
# @click.option('--password', prompt=True, hide_input=True,
#               confirmation_prompt=True)
@click.password_option()
def encrypt(password):
    # click.echo('Encrypting password to %s' % password.encode('rot13'))
    click.echo('Encrypting password to %s' % codecs.encode(password, 'rot-13'))

@examples.command()
# @click.option('--username', prompt=True,
@click.option('--username', prompt=False if os.environ.get('USER', '') else True,
              default=lambda: os.environ.get('USER', ''),
              show_default='current user')
def read_user(username):
    print("Hello,", username)

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    # click.echo('Version 1.0')
    click.echo(version)
    ctx.exit()

@examples.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def callbacks_eager():
    click.echo('Hello World!')

# @click.group()
# @click.option('--debug/--no-debug')
# def cli(debug):
#     click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@examples.command()
@click.option('--username', envvar=f'{APP.upper()}_USERNAME')
def greet(username):
    click.echo('Hello %s!' % username)

@examples.command()
# @click.option('paths', '--path', envvar='PATHS', multiple=True,
@click.option('paths', '--path', envvar='PATH', multiple=True,
              type=click.Path())
def perform(paths):
    for path in paths:
        click.echo(path)

@examples.command()
@click.option('+w/-w')
def chmod(w):
    click.echo('writable=%s' % w)

def validate_rolls(ctx, param, value):
    try:
        rolls, dice = map(int, value.split('d', 2))
        return (dice, rolls)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')

@examples.command()
@click.option('--rolls', callback=validate_rolls, default='1d6', show_default=True)
def roll(rolls):
    click.echo('Rolling a %d-sided dice %d time(s)' % rolls)

@examples.command()
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=True, dir_okay=True, file_okay=False))
def copy(src, dst):
    """Move file SRC to DST."""
    for fn in src:
        click.echo('move %s to folder %s' % (fn, dst))

@examples.command()
@click.argument('src', envvar='SRC', type=click.File('r'))
def echo(src):#try export SRC=hello.txt
    """Print value of SRC environment variable."""
    click.echo(src.read())

def common_auth_options(func):
    username_envvar = os.environ.get(f'{APP.upper()}_USERNAME', '')
    password_envvar = os.environ.get(f'{APP.upper()}_PASSWORD', '')
    if username_envvar:
        func = click.option('-u', '--username', default=username_envvar,
                            show_default='current username')(func)
    else:
        func = click.option('-u', '--username', required=True)(func)
    if password_envvar:
        func = click.option('-p', '--password', default=password_envvar,
                            show_default='current password')(func)
    else:
        func = click.option('-p', '--password', required=True)(func)
    return func

@examples.command()
@common_auth_options
def login(*args, **kwargs):
    click.echo((args, kwargs))

# @examples.command()  # @cli, not @click!
# @click.pass_context
# def sync(ctx):
#     click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
#     click.echo('Syncing')

def pass_obj(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.obj, *args, **kwargs)
    return update_wrapper(new_func, f)

@examples.command()  # @cli, not @click!
# @click.pass_obj
@pass_obj
def sync(ctx):
    # click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
    click.echo('Debug is %s' % (ctx['DEBUG'] and 'on' or 'off'))
    # click.echo(str(ctx))
    click.echo('Syncing')

# @examples.command('sdist')
# def sdist():
#     click.echo('sdist called')
#
# @examples.command('bdist_wheel')
# def bdist_wheel():
#     click.echo('bdist_wheel called')

@examples.command()
@click.option('--port', default=8000)
def runserver(port):
    click.echo('Serving on http://127.0.0.1:%d/' % port)

@examples.command()
def prompt():
    # value = click.prompt('Please enter a valid integer', type=int)
    value = click.prompt('Please enter a number', default=42.0)
    click.echo(value)
    if click.confirm('Do you want to continue?', abort=True):
        click.echo('Well done!')

@examples.command()
@click.option("--count", default=1, help="Number of greetings.", metavar='<int>')
@click.option("--name", prompt="Your name", help="The person to greet.", metavar='<name>')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

@examples.command('init', short_help='init the repo')
def init():
    """Initializes the repository."""

@examples.command('delete', short_help='delete the repo')
def delete():
    """Deletes the repository."""

@examples.command()
@click.argument('f', type=click.File())
def cat(f):
    click.echo(f.read())

@examples.command()
@click.option('--foo', prompt=True)
def prompt2(foo):
    click.echo('foo=%s' % foo)

@examples.command()
def print_stdout():
    click.echo('Hello World!')
    click.echo(b'\xe2\x98\x83', nl=False)
    click.echo('Hello World!', err=True)

@examples.command()
def ansi_colors():
    click.secho('Hello World!', fg='green')
    click.secho('Some more text', bg='blue', fg='white')
    click.secho('ATTENTION', blink=True, bold=True)

def _generate_output(lines):
    for idx in range(lines):
        yield "Line %d\n" % idx

@examples.command()
@click.option("--lines", default=50000, help="Number of lines.", show_default=True)
def less(lines):
    click.echo_via_pager(_generate_output(lines))

@examples.command()
def clear():
    click.clear()

@examples.command()
def getchar():
    click.echo('Continue? [yn] ', nl=False)
    c = click.getchar()
    click.echo()
    if c == 'y':
        click.echo('We will go on')
    elif c == 'n':
        click.echo('Abort!')
    else:
        click.echo('Invalid input :(')

@examples.command()
def pause():
    click.pause()

@examples.command()
def get_commit_message():
    MARKER = '# Everything below is ignored\n'
    message = click.edit('\n\n' + MARKER)
    if message is not None:
        return message.split(MARKER, 1)[0].rstrip('\n')

@examples.command()
@click.argument('filename', type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False))
def edit(filename):
    """Edit FILENAME if the file exists."""
    click.edit(filename=filename)

@examples.command()
@click.argument('resource')
def launch(resource):
    """This can be used to open the default application associated with a URL or filetype."""
    click.launch(resource, locate=True)

@examples.command()
def get_streams():
    stdin_text = click.get_text_stream('stdin')
    stdout_binary = click.get_binary_stream('stdout')
    click.echo((stdin_text, stdout_binary))

@examples.command()
@click.argument('filename', type=click.Path(exists=False, dir_okay=False, file_okay=True, resolve_path=False))
def write_file(filename):
    """Write 'Hello World!' to FILENAME."""
    # stdout = click.open_file('-', 'w')
    # test_file = click.open_file('test.txt', 'w')
    with click.open_file(filename, 'w') as f:
        f.write('Hello World!\n')

@examples.command()
@click.argument('app_name', type=click.Path(exists=False, dir_okay=False, file_okay=True, resolve_path=False))
def read_config(app_name):
    """Print APP_NAME config file."""
    cfg = os.path.join(click.get_app_dir(app_name), 'config.ini')
    click.echo(cfg)
    parser = configparser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    click.echo(rv)
    return rv

@examples.command()
def progress_bar():
    with click.progressbar([1, 2, 3], label='Incremental sleep') as bar:
        for x in bar:
            click.echo(' sleep({})...'.format(x))
            time.sleep(x)

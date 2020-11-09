import click

from .world import get_world

@click.command()
def print_hello():
    print('hello!')

def hello_world():
    return f'hello {get_world()}!'

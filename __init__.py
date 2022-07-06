plugins = []

from .examples import examples
plugins.append('examples')

__all__ = []
for plugin in plugins:
    __all__.append(plugin)

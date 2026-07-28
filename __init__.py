# plugins = []

# from .examples import examples
# plugins.append('examples')

# __all__ = []
# for plugin in plugins:
#     __all__.append(plugin)
plugins = []

from .plugin_b797e6c8fe8d47c8ba5c5689b2628c89 import examples
plugins.append("examples")

__all__ = plugins

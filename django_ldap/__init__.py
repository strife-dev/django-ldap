try:
    from .version import version
except ImportError:
    __version__ = "DEV"
else:
    __version__ = version

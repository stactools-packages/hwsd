import stactools.core
from stactools.cli import Registry

from stactools.hwsd.stac import create_collection, create_item

__all__ = ['create_collection', 'create_item']

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    from stactools.hwsd import commands
    registry.register_subcommand(commands.create_hwsd_command)


__version__ = "0.1.0"

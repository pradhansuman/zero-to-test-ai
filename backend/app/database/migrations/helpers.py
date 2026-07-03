"""Migration helper utilities."""
import asyncio
from alembic.config import Config
from alembic import command


def get_alembic_config() -> Config:
    """Get Alembic configuration."""
    return Config("alembic.ini")


async def run_upgrade(revision: str = "head") -> None:
    """Run migrations upgrade."""
    config = get_alembic_config()
    command.upgrade(config, revision)


async def run_downgrade(revision: str = "-1") -> None:
    """Run migrations downgrade."""
    config = get_alembic_config()
    command.downgrade(config, revision)


async def current_revision() -> str:
    """Get current migration revision."""
    config = get_alembic_config()
    return command.current(config)


async def list_revisions():
    """List all migrations."""
    config = get_alembic_config()
    return command.history(config)

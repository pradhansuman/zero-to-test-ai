"""Base repository with generic CRUD operations."""
from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.utils.logger import get_logger

T = TypeVar('T')
logger = get_logger(__name__)


class BaseRepository(Generic[T]):
    """Base repository for generic CRUD operations."""

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, obj_in: Dict[str, Any]) -> T:
        """Create new record."""
        try:
            db_obj = self.model(**obj_in)
            self.session.add(db_obj)
            await self.session.flush()
            logger.info(
                f"Created {self.model.__name__}",
                resource_id=db_obj.id if hasattr(db_obj, 'id') else None
            )
            return db_obj
        except Exception as e:
            logger.error(
                f"Error creating {self.model.__name__}: {str(e)}",
                error=str(e)
            )
            await self.session.rollback()
            raise

    async def get(self, id: int) -> Optional[T]:
        """Get record by ID."""
        try:
            result = await self.session.execute(
                select(self.model).where(self.model.id == id)
            )
            obj = result.scalar_one_or_none()
            logger.debug(
                f"Retrieved {self.model.__name__}",
                resource_id=id,
                found=obj is not None
            )
            return obj
        except Exception as e:
            logger.error(
                f"Error retrieving {self.model.__name__} {id}: {str(e)}",
                error=str(e)
            )
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination."""
        try:
            result = await self.session.execute(
                select(self.model).offset(skip).limit(limit)
            )
            items = result.scalars().all()
            logger.debug(
                f"Retrieved all {self.model.__name__}",
                count=len(items)
            )
            return items
        except Exception as e:
            logger.error(
                f"Error retrieving all {self.model.__name__}: {str(e)}",
                error=str(e)
            )
            raise

    async def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[T]:
        """Update record."""
        try:
            result = await self.session.execute(
                select(self.model).where(self.model.id == id)
            )
            db_obj = result.scalar_one_or_none()
            if not db_obj:
                return None

            for key, value in obj_in.items():
                if value is not None and hasattr(db_obj, key):
                    setattr(db_obj, key, value)

            self.session.add(db_obj)
            await self.session.flush()
            logger.info(
                f"Updated {self.model.__name__}",
                resource_id=id,
                fields_updated=list(obj_in.keys())
            )
            return db_obj
        except Exception as e:
            logger.error(
                f"Error updating {self.model.__name__} {id}: {str(e)}",
                error=str(e)
            )
            await self.session.rollback()
            raise

    async def delete(self, id: int) -> bool:
        """Delete record."""
        try:
            result = await self.session.execute(
                select(self.model).where(self.model.id == id)
            )
            db_obj = result.scalar_one_or_none()
            if not db_obj:
                return False

            self.session.delete(db_obj)
            await self.session.flush()
            logger.info(
                f"Deleted {self.model.__name__}",
                resource_id=id
            )
            return True
        except Exception as e:
            logger.error(
                f"Error deleting {self.model.__name__} {id}: {str(e)}",
                error=str(e)
            )
            await self.session.rollback()
            raise

    async def find_by(self, **filters: Any) -> List[T]:
        """Find records by filters."""
        try:
            conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):
                    conditions.append(getattr(self.model, key) == value)

            query = select(self.model)
            if conditions:
                query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            items = result.scalars().all()
            logger.debug(
                f"Found {self.model.__name__}",
                filters=filters,
                count=len(items)
            )
            return items
        except Exception as e:
            logger.error(
                f"Error finding {self.model.__name__}: {str(e)}",
                error=str(e)
            )
            raise

    async def find_one_by(self, **filters: Any) -> Optional[T]:
        """Find single record by filters."""
        try:
            results = await self.find_by(**filters)
            return results[0] if results else None
        except Exception as e:
            logger.error(
                f"Error finding one {self.model.__name__}: {str(e)}",
                error=str(e)
            )
            raise

    async def count(self) -> int:
        """Count total records."""
        try:
            result = await self.session.execute(
                select(self.model)
            )
            count = len(result.scalars().all())
            logger.debug(f"Counted {self.model.__name__}", count=count)
            return count
        except Exception as e:
            logger.error(
                f"Error counting {self.model.__name__}: {str(e)}",
                error=str(e)
            )
            raise

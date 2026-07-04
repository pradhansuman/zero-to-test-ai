"""Test data management service."""
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)

class TestDataManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.transactions = {}

    async def setup_test_data(self, test_id: int, data_config: dict) -> dict:
        transaction_id = str(uuid.uuid4())
        try:
            created_data = {"test_id": test_id, "data": data_config}
            self.transactions[transaction_id] = created_data
            logger.info("test_data_setup", transaction_id=transaction_id)
            return {
                'transaction_id': transaction_id,
                'data': created_data,
                'created_at': datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error("data_setup_error", error=str(e))
            return {"error": str(e)}

    async def cleanup_test_data(self, transaction_id: str) -> dict:
        if transaction_id in self.transactions:
            del self.transactions[transaction_id]
            return {"success": True, "transaction_id": transaction_id}
        return {"error": "Transaction not found"}

    async def get_transaction(self, transaction_id: str) -> dict:
        return self.transactions.get(transaction_id, {})

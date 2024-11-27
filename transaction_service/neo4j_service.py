import uuid
from datetime import datetime
import neo4j


class TransactionRepository:
    def __init__(self, driver):
        self.driver = driver


    def create_transaction(self, transaction_data):
        query = """
                    MERGE (source:Account {account_id: $source_id})
                    MERGE (target:Account {account_id: $target_id})
                    CREATE (source)-[t:TRANSACTION {
                        transaction_id: $transaction_id,
                        amount: $amount,
                        timestamp: datetime($timestamp),
                        currency: $currency
                    }]->(target)
                    RETURN t.transaction_id as transaction_id
                    """
        with self.driver.session() as session:
            result = session.run(query, {
                'source_id': transaction_data['source_id'],
                'target_id': transaction_data['target_id'],
                # the transaction id is generated by the uuid library
                'transaction_id': str(uuid.uuid4()),
                'amount': transaction_data['amount'],
                'timestamp': datetime.strptime(transaction_data['timestamp'], '%d/%m/%Y, %H:%M:%S'),
                'currency': transaction_data['currency']
            })
            return result.single()['transaction_id']

    def get_transaction(self, transaction_id):
        with self.driver.session() as session:
            query = """
            MATCH (source)-[t:TRANSACTION {transaction_id: $transaction_id}]->(target)
            RETURN source.account_id as source_id,
                    target.account_id as target_id,
                    t.amount as amount,
                    t.timestamp as timestamp,
                    t.currency as currency
            """
            result = session.run(query, {'transaction_id': transaction_id})
            record = result.single()
            if record:
                return self._serialize_transaction(record)
            return None

    def _serialize_transaction(self, record):
        """Helper function to serialize transaction records."""
        transaction = dict(record)
        if isinstance(transaction.get("timestamp"), neo4j.time.DateTime):
            # Convert Neo4j DateTime to ISO-8601 string
            transaction["timestamp"] = transaction["timestamp"].iso_format()
        return transaction
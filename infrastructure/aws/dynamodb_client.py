"""
EN: DynamoDB client for persisting conversation history / document metadata.
FR: Client DynamoDB pour persister l'historique des conversations / métadonnées de documents.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

try:
    import boto3  # type: ignore
    from boto3.dynamodb.conditions import Key  # type: ignore
except Exception:  # pragma: no cover
    boto3 = None
    Key = None  # type: ignore[assignment, misc]


class DynamoDBClient:
    """
    EN: Thin wrapper around a DynamoDB table.
        No-op when boto3 is unavailable or USE_IN_MEMORY_DB=true.
    FR: Couche mince autour d'une table DynamoDB.
        No-op quand boto3 est indisponible ou USE_IN_MEMORY_DB=true.
    """

    def __init__(
        self,
        table_name: str | None = None,
        region: str | None = None,
    ) -> None:
        self.table_name = table_name or os.getenv("DYNAMODB_TABLE", "strata-rag-docs")
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self._table = None

        use_memory = os.getenv("USE_IN_MEMORY_DB", "true").lower() == "true"
        if not use_memory and boto3 is not None:
            ddb = boto3.resource("dynamodb", region_name=self.region)
            self._table = ddb.Table(self.table_name)

        # EN: In-memory fallback store
        # FR: Magasin de repli en mémoire
        self._mem: Dict[str, Dict[str, Any]] = {}

    def put_item(self, item: Dict[str, Any]) -> None:
        if self._table is not None:
            self._table.put_item(Item=item)
        else:
            self._mem[item["id"]] = item

    def get_item(self, key: str) -> Optional[Dict[str, Any]]:
        if self._table is not None:
            resp = self._table.get_item(Key={"id": key})
            return resp.get("Item")
        return self._mem.get(key)

    def query_by_partition(self, partition_key: str, value: str) -> List[Dict[str, Any]]:
        if self._table is not None and Key is not None:
            resp = self._table.query(KeyConditionExpression=Key(partition_key).eq(value))
            return resp.get("Items", [])
        return [v for v in self._mem.values() if v.get(partition_key) == value]
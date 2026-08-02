from dataclasses import dataclass
import sqlite3

from config.operator_definition import DataType


@dataclass
class FieldDefinition:
    id: str
    dataset: str
    region: str
    data_type: DataType
    category_id: str
    category_name: str
    description: str | None


class FieldRepository:
    """
    SQLite fields 테이블 조회 담당

    Generator는 직접 DB를 접근하지 않고
    이 Repository를 통해 Field 정보를 가져온다.
    """

    def __init__(self, db_path="worldquant.db"):

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row


    def _row_to_field(
        self,
        row
    ) -> FieldDefinition:
        """
        SQLite Row -> FieldDefinition 변환
        """

        return FieldDefinition(
            id=row["id"],
            dataset=row["dataset"],
            region=row["region"],
            data_type=DataType(row["type"]),
            category_id=row["category_id"],
            category_name=row["category_name"],
            description=row["description"]
        )


    def get_all_fields(self) -> list[FieldDefinition]:
        """
        모든 field 조회
        """

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                id,
                dataset,
                region,
                type,
                category_id,
                category_name,
                description
            FROM fields
        """)

        rows = cursor.fetchall()

        return [
            self._row_to_field(row)
            for row in rows
        ]


    def get_fields_by_data_type(
        self,
        data_type: DataType
    ) -> list[FieldDefinition]:
        """
        DataType 기준 field 조회

        예:
        DataType.MATRIX
        DataType.VECTOR
        DataType.GROUP
        """

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                id,
                dataset,
                region,
                type,
                category_id,
                category_name,
                description
            FROM fields
            WHERE type = ?
        """, (data_type.value,))


        rows = cursor.fetchall()

        return [
            self._row_to_field(row)
            for row in rows
        ]


    def get_fields_by_dataset(
        self,
        dataset: str
    ) -> list[FieldDefinition]:

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                id,
                dataset,
                region,
                type,
                category_id,
                category_name,
                description
            FROM fields
            WHERE dataset = ?
        """, (dataset,))


        rows = cursor.fetchall()

        return [
            self._row_to_field(row)
            for row in rows
        ]


    def close(self):

        self.conn.close()
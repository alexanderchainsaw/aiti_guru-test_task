from typing import ClassVar

from pydantic import BaseModel


class SQLModel(BaseModel):
    tablename: ClassVar = None

    @classmethod
    def build_str_values_sql(cls, skip: tuple[str] | None = ()) -> str:
        """Creates a `"tablename"."column", ...` structure"""
        return ",".join(
            f"""{f'"{cls.tablename}".' if cls.tablename else ""}{f'"{field_name}"'}"""
            for field_name in cls.model_fields.keys()
            if field_name not in skip
        )

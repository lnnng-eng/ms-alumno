from dataclasses import dataclass  
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app import db

@dataclass(init=False, repr=True, eq=True)
class Documento(db.Model):
    __tablename__ = 'documentos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_documento: Mapped[str] = mapped_column(String(50), nullable=False)

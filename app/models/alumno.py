from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app import db

@dataclass(init=False, repr=True, eq=True)
class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    nro_documento: Mapped[str] = mapped_column(String(50), nullable=False)
    nro_legajo: Mapped[int] = mapped_column(Integer, nullable=False)

#sin fechas y sin relaciones
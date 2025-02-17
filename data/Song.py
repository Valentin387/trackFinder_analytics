
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from .Vehiculo import Vehiculo

# Define ObjectId as a valid type for Pydantic to handle
class ObjectIdField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class VehiculoPlusLocation(BaseModel):
    id: ObjectIdField = Field(..., alias="_id")
    vehiculo: Vehiculo
    latitud: float
    longitud: float
    timeStamp: datetime
    timeStampServer: datetime
    speed: float
    batteryPercentage: Optional[float] = None  # Make this field optional
    usuario: ObjectIdField
    applicationVersion: Optional[str] = None  # Optional field
    locationAccuracy: Optional[float] = None  # Optional field
from typing import List, Optional
from uuid import UUID, uuid4, uuid1
from pydantic import BaseModel, Field
from enum import Enum
from pydantic import BaseModel

class Gender(str, Enum):
 male = "male"
 female = "female"
class Role(str, Enum):
 lecturer = "lecturer"
 user = "user"

class UserModel(BaseModel):
 uid: Optional[str] = uuid4()
 first_name: str = Field(..., example="Yhemmy")
 last_name: str = Field(..., example="John")
 gender: Gender
 aws_credit: int = Field(..., example=100)
 roles: List[Role]
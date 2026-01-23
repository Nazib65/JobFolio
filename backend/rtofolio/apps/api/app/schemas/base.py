"""
Base pydantic Schema Configuration 
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """ Base Schema with common configuration """
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True, 
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None 

        }
    )

class TimeStampMixin(BaseModel):
    """ Mixin for created_at and updated_at fields """
    created_at: datetime 
    updated_at: datetime 

class IDMixin(BaseModel):
    """ Mixin for id field """
    id: int 

class PaginationParams(BaseModel):
    """ Common pagination parameters """
    page: int = 1
    page_size: int = 20

    @property 
    def offset(self) -> int:
        """ Calculate offset for pagination """
        return (self.page -1) * self.page_size
    
class PaginatedResponse(BaseModel):
    """ Generic paginatedresponse wrapper"""
    items: int 
    total: int 
    page: int 
    page_size: int 
    total_pages: int 

    @classmethod
    def create(cls, items: list, total: int, params: PaginationParams) -> "PaginatedResponse":
        total_pages =(total + params.page_size -1) // params.page_size
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages
        )

class ErrorResponse(BaseModel):
    """ Standard error response """
    error: str 
    detail: Optional[str]=None 
    code: Optional[str]=None 

class SucessResponse(BaseModel):
    """ Standard sucess response """
    success: bool =True
    message: Optional[str]=None 


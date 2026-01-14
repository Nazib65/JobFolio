from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

class Theme(BaseModel):
    style: Optional[str] = None
    color_palette: Optional[str] = None
    font: Optional[str] = None
    tone: Optional[str] = None
    # Updated keys to snake_case
    max_width: Optional[str] = "1280px" 
    width: Optional[str] = "100%"
    margin: Optional[str] = "0 auto"
    display: Optional[str] = "flex"
    flex_direction: Optional[str] = "column"
    align_items: Optional[str] = "center"

class Slot(BaseModel):
    name: str
    type: Optional[str] = None
    optional: Optional[bool] = False

class Layout(BaseModel):
    type: Optional[str] = None
    direction: Optional[str] = None
    gap: Optional[str] = None
    align: Optional[str] = None
    justify: Optional[str] = None
    
    # Added sizing/spacing keys found in your JSON
    width: Optional[str] = None
    max_width: Optional[str] = None
    margin: Optional[str] = None
    
    # Supports {"desktop": 5, "mobile": 1}
    columns: Optional[Dict[str, int]] = None
    
    # Supports nested slots for Nav/Footer
    slots: Optional[Dict[str, Union[List[Slot], List[str], str]]] = None
    
    # Allow for nested layouts (desktop/mobile) if strict typing is needed, 
    # though usually handled at the Section level for polymorphism.
    desktop: Optional['Layout'] = None
    mobile: Optional['Layout'] = None

class ItemLayout(BaseModel):
    type: str
    layout: Optional[Layout] = None
    slots: Optional[List[Slot]] = None
    constraints: Optional[Dict[str, Any]] = None

class Section(BaseModel):
    type: str
    priority: Optional[str] = None
    
    # Can be a direct Layout object OR a dict with "desktop"/"mobile" keys
    layout: Union[Layout, Dict[str, Layout]]
    
    props: Optional[Dict[str, Any]] = None
    items: Optional[List[Dict[str, Any]]] = None
    
    # Updated key to snake_case
    item_layout: Optional[ItemLayout] = None

class PortfolioSchema(BaseModel):
    # Updated key to snake_case
    schema_version: str
    theme: Theme
    sections: List[Section]

# Necessary for recursive models (if Layout references itself)
Layout.update_forward_refs()
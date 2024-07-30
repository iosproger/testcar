from pydantic import BaseModel

# Node
class NodeBase(BaseModel):
    name: str

class NodeCreate(NodeBase):
    pass

class Node(NodeBase):
    node_id: int

    class Config:
        from_attributes = True

# Vin
class VinBase(BaseModel):
    name: str

class VinCreate(VinBase):
    pass

class Vin(VinBase):
    vin_id: int

    class Config:
        from_attributes = True

# Bind
class BindBase(BaseModel):
    node_name: str
    vin_name: str

class BindCreate(BindBase):
    pass

class Bind(BindBase):
    bind_id: int

    class Config:
        from_attributes = True

# location
class LocBase(BaseModel):
    node_name: str
    latitude: str
    longitude: str

class LocCreate(LocBase):
    pass

class Location(LocBase):
    loc_id: int

    class Config:
        from_attributes = True
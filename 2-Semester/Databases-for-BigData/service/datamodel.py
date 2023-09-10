from neomodel import (StructuredNode, 
                      RelationshipTo, 
                      RelationshipFrom, 
                      StringProperty, 
                      BooleanProperty, 
                      ArrayProperty,
                      DateTimeProperty,
                      IntegerProperty)

class Tag(StructuredNode):
    # address or name as 'id'
    address = StringProperty(unique_index=True, required=True)
    sensors = ArrayProperty()
    name = StringProperty()
    last_contact = StringProperty() # TODO: date
    online = BooleanProperty
    gateway = RelationshipFrom('Gateway', 'CONNECTED_TO')

class Gateway(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
    network_segment = IntegerProperty()
    last_contact =  StringProperty() # TODO: date
    online = BooleanProperty()
    ip_address = StringProperty()
    tag = RelationshipTo('Tag', 'CONNECTED_TO') # cardiality=ZeroOrMore (default)
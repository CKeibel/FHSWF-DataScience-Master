from neomodel import (StructuredNode,
                      StructuredRel, 
                      RelationshipTo, 
                      RelationshipFrom, 
                      StringProperty, 
                      BooleanProperty,
                      FloatProperty,
                      DateTimeProperty,
                      IntegerProperty)

class Tag(StructuredNode):
    # address or name as 'id'
    address = StringProperty(unique_index=True, required=True)
    name = StringProperty()
    last_contact = StringProperty() # TODO: date
    online = BooleanProperty
    gateway = RelationshipFrom('Gateway', 'CONNECTED_TO')
    accleration_sensor = RelationshipTo('AcclerationSensor', 'CONNECTED_TO')
    humidity_sensor = RelationshipTo('HumiditySensor', 'CONNECTED_TO')
    voltage_sensor = RelationshipTo('VoltageSensor', 'CONNECTED_TO')
    temperature_sensor = RelationshipTo('TemperatureSensor', 'CONNECTED_TO')


# Maybe rel
class GatewayTagConfig(StructuredRel):
    samplerate = IntegerProperty()
    scan_interval = IntegerProperty()
    resolution = IntegerProperty()
    scale = IntegerProperty()
    dsp_function = IntegerProperty()
    dsp_parameter = IntegerProperty()
    mode = IntegerProperty()
    divider = IntegerProperty()

    def to_dict(self) -> dict:
        mapping = {
            "samplerate": self.samplerate,
            "scan_interval": self.scan_interval,
            "resolution": self.resolution,
            "scale": self.scale,
            "dsp_function": self.dsp_function,
            "dsp_parameter": self.dsp_parameter,
            "mode": self.mode,
            "divider": self.divider
        }
        return mapping


class Gateway(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
    network_segment = IntegerProperty()
    last_contact =  StringProperty() # TODO: date
    online = BooleanProperty()
    ip_address = StringProperty()
    tag = RelationshipTo('Tag', 'CONFIGURES', model=GatewayTagConfig) # cardiality=ZeroOrMore (default)
    config = RelationshipTo('Config', 'STORES')


class Config(StructuredNode):
    version = StringProperty()
    poll_interval = IntegerProperty()
    max_allowed_clients = IntegerProperty()
    api_timeout = IntegerProperty()


class AcclerationSensor(StructuredNode):
    acc_x = FloatProperty()
    acc_y = FloatProperty()
    acc_z = FloatProperty()
    movement_counter = IntegerProperty()
    recorded_time = StringProperty()


class HumiditySensor(StructuredNode):
    humidity = FloatProperty()
    humidity_scale = IntegerProperty()
    recorded_time = StringProperty()


class VoltageSensor(StructuredNode):
    voltage = FloatProperty()
    voltage_scale = IntegerProperty()
    recorded_time = StringProperty()


class TemperatureSensor(StructuredNode):
    temperature = FloatProperty()
    temperature_scale = IntegerProperty()
    recorded_time = StringProperty()
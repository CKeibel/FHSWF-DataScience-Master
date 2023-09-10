from datamodel import (Gateway,
                        Tag, 
                        Config, 
                        GatewayTagConfig,
                        AcclerationSensor,
                        TemperatureSensor,
                        HumiditySensor,
                        VoltageSensor
                        )
from neomodel import config
import requests
import json
import logging

# logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.WARNING)


# status code decorator
def check_status_code(func):
    def inner(api):
        logger = logging.getLogger(__name__)
        status_code = requests.get(api).status_code
        if  status_code != 200:
            logger.warning(f"Bad request: {status_code}")
            return None
        
        return func(api)
    
    return inner


@check_status_code
def get_config(api:str) -> Config | None:
    config_api = requests.get(api)
    c = json.loads(config_api.text)["config"]
    cfg = Config(
        version=c["version"],
        poll_interval=c["poll_interval"],
        max_allowed_clients=c["max_allowed_clients"],
        api_timeout=c["api_timeout"]
    ).save()
    return cfg  


@check_status_code
def get_gateway_tag_config(api: str) -> GatewayTagConfig:
    config_api = requests.get(api)
    c: dict = json.loads(config_api.text)["config"]
    cfg = GatewayTagConfig(
        samplerate=c["samplerate"],
        scan_interval=c["scan_interval"],
        resolution=c["resolution"],
        scale=c["scale"],
        dsp_function=c["dsp_function"],
        dsp_parameter=c["dsp_parameter"],
        mode=c["mode"],
        divider=c["divider"]
    )

    return cfg


@check_status_code
def get_sensor_data(api: str) -> tuple[AcclerationSensor, TemperatureSensor, HumiditySensor, VoltageSensor]:
    sensor_api = requests.get(api)
    try:
        s: list[dict] = json.loads(sensor_api.text)["measurements"]
    except json.JSONDecodeError:
        return None

    acc = AcclerationSensor(
        acc_x=s[0]["acc_x"],
        acc_y=s[0]["acc_y"],
        acc_z=s[0]["acc_z"],
        movement_counter=s[0]["movement_counter"],
        recorded_time=s[0]["recorded_time"]
    ).save()

    temp = TemperatureSensor(
        temperature=s[1]["temperature"],
        temperature_scale=s[1]["temperature_scale"],
        recorded_time=s[1]["recorded_time"]
    ).save()

    hum = HumiditySensor(
        humidity=s[2]["humidity"],
        humidity_scale=s[2]["humidity_scale"],
        recorded_time=s[2]["recorded_time"]
    ).save()

    vol = VoltageSensor(
        voltage=s[3]["voltage"],
        voltage_scale=s[3]["voltage_scale"],
        recorded_time=s[3]["recorded_time"]
    ).save()

    return (acc, temp, hum, vol)


def fetch_and_persist() -> None:
    """  Fetching data """

    config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"
    
    # api for fetchin gateway data
    gateway_api = requests.get("http://localhost:8080/api/v1/structure/gateway/list")

    if gateway_api.status_code == 200: # TODO: maybe try-except
        for g in json.loads(gateway_api.text)["gateways"]:
            gateway: Gateway | None = Gateway.nodes.get_or_none(gid=g["id"])
            if gateway is None:
                # Create new gateway
                gateway: Gateway = Gateway(
                    gid=g["id"],
                    network_segment=g["network_segment"],
                    last_contact=g["last_contact"],
                    online=g["online"],
                    ip_address=g["ip_address"]
                ).save()

            # Get gateway config
            cfg = get_config(f"http://localhost:8080/api/v1/config/get/{gateway.gid}")
            if cfg:
                gateway.config.connect(cfg)

            
            # Fetch tags for gateway
            tag_api = requests.get(f"http://localhost:8080/api/v1/structure/tag/list/{g['id']}")
            if tag_api.status_code == 200: # TODO: maybe try-except
                for t in json.loads(tag_api.text):
                    tag: Tag | None = Tag.nodes.get_or_none(address=t["address"])
                    if tag is None:
                        # Add tag to gateway tag-list
                        tag = Tag(
                            address=t["address"],
                            name=t["name"],
                            last_contact=t["last_contact"],
                            online=t["online"],
                        ).save()

                    # Get gateway to tag relationship properties
                    gateway_tag = get_gateway_tag_config(f"http://localhost:8080/api/v1/config/get/{gateway.gid}/{tag.address}")
                    gateway.tag.connect(tag, gateway_tag.to_dict())

                    # Get tag sensor data
                    acc, temp, hum, vol = get_sensor_data(f"http://localhost:8080/api/v1/acc-data/get/{tag.address}") or (None, None, None, None)
                    if acc:
                        tag.accleration_sensor.connect(acc)
                    if temp:
                        tag.temperature_sensor.connect(temp)
                    if hum:
                        tag.humidity_sensor.connect(hum)
                    if vol:
                        tag.voltage_sensor.connect(vol)
            


def main() -> None:
    fetch_and_persist()


if __name__ == "__main__":
    main()
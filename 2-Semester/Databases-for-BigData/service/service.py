from datamodel import Gateway, Tag
from neomodel import config
import requests
import json


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
            
            # Fetch tags for gateway
            tag_api = requests.get(f"http://localhost:8080/api/v1/structure/tag/list/{g['id']}")
            if tag_api.status_code == 200: # TODO: maybe try-except
                for t in json.loads(tag_api.text):
                    tag: Tag | None = Tag.nodes.get_or_none(address=t["address"])
                    if tag is None:
                        # Add tag to gateway tag-list
                        tag = Tag(
                            address=t["address"],
                            sensors=t["sensors"],
                            name=t["name"],
                            last_contact=t["last_contact"],
                            online=t["online"],
                        ).save()

                    gateway.tag.connect(tag)

            


def main() -> None:
    fetch_and_persist()


if __name__ == "__main__":
    main()
from datamodel import Gateway, Tag
from database import CloudService
import requests
import json


def fetch_data() -> list[Gateway]:
    """  Fetching data """
    
    # api for fetchin gateway data
    gateway_api = requests.get("http://localhost:8080/api/v1/structure/gateway/list")

    gateways: list[Gateway] = []
    if gateway_api.status_code == 200: # TODO: maybe try-except
        for gateway in json.loads(gateway_api.text)["gateways"]:
            # Create new gateway
            g: Gateway = Gateway(**gateway)
            
            # Fetch tags for gateway
            tag_api = requests.get(f"http://localhost:8080/api/v1/structure/tag/list/{gateway['id']}")
            if tag_api.status_code == 200: # TODO: maybe try-except
                for tag in json.loads(tag_api.text):
                    # Add tag to gateway tag-list
                    g.tags += [Tag(**tag)]

            gateways += [g]
                
    return gateways


def main() -> None:
    gateways: list[Gateway] = fetch_data()
    cloud_service = CloudService("bolt://localhost:7687", "neo4j", "password")
    cloud_service.create_graph_from_gateway_list(gateways)
    cloud_service.close()


if __name__ == "__main__":
    main()
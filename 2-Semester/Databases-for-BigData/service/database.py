from neo4j import GraphDatabase
from datamodel import Gateway

class CloudService:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_graph_from_gateway_list(self, gateways: list[Gateway]) -> None:
        with self.driver.session() as session:
            session.run("MERGE (:Test)")
            tx = session.begin_transaction()
            query = (""" 
            MERGE (g:Gateway {id:$id, 
                network_segment: $network_segment,
                last_contact: $last_contact,
                online: $online,
                ip_address: $ip_address,
                id: $id})
            RETURN g """)
            for gateway in gateways:
                result = tx.run(
                    query,
                    id=gateway.id,
                    network_segment=gateway.network_segment,
                    last_contact=gateway.last_contact,
                    online=gateway.last_contact,
                    ip_address=gateway.ip_address,
                )

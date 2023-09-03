# starting gateway service container
docker run -d -p 8080:8080 ghcr.io/systematiccaos/ruuvi-simulator/sim:master

# starting neo4j container
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
	--env=NEO4J_AUTH=none \
    neo4j
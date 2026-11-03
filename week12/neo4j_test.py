from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

queries = {
    "Q6 Actors in The Matrix":
        "MATCH (p:Person)-[:ACTED_IN]->(:Movie {title:'The Matrix'}) RETURN p.name AS name",
    "Q10 Total movies":
        "MATCH (m:Movie) RETURN count(m) AS total",
    "Q16 Acted & directed same movie":
        "MATCH (p:Person)-[:ACTED_IN]->(m)<-[:DIRECTED]-(p) RETURN p.name AS name, m.title AS movie",
}

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connected to Neo4j\n")
    for label, q in queries.items():
        records, _, _ = driver.execute_query(q)
        print(f"== {label} ({len(records)} rows) ==")
        for r in records:
            print(dict(r))
        print()
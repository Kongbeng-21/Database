from neo4j import GraphDatabase

qs = [
"MATCH (m:Movie) RETURN m.title, m.released ORDER BY m.title",
"MATCH (p:Person) RETURN p.name, p.born ORDER BY p.name",
"MATCH (p:Person)-[:ACTED_IN]->(:Movie) RETURN DISTINCT p.name",
"MATCH (m:Movie) WHERE m.released > 2000 RETURN m.title",
"MATCH (m:Movie {title: 'The Matrix'}) RETURN m",
"MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: 'The Matrix'}) RETURN p.name, r.roles",
"MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'The Matrix'}) RETURN p.name",
"MATCH (m:Movie) WHERE m.released >= 1990 AND m.released <= 2000 RETURN m.title",
"MATCH (:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m:Movie) RETURN m.title",
"MATCH (m:Movie) RETURN count(m) AS total_movies",
"MATCH (p:Person)-[:ACTED_IN]->() WHERE p.born > 1970 RETURN DISTINCT p.name, p.born",
"MATCH (m:Movie) WHERE toLower(m.tagline) CONTAINS 'love' RETURN m.title",
"MATCH (p:Person)-[r:REVIEWED]->(m:Movie) WHERE r.rating > 50 RETURN m.title, p.name, r.rating",
"MATCH (p:Person)-[:ACTED_IN]->() WHERE p.name STARTS WITH 'K' RETURN DISTINCT p.name",
"MATCH (m:Movie) WHERE m.released < 1995 RETURN m.title",
"MATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(p) RETURN p.name, m.title",
"MATCH (p:Person)-[:ACTED_IN]->(m:Movie) WITH p, count(m) AS movies WHERE movies > 2 RETURN p.name, movies",
"MATCH (a:Person)-[:ACTED_IN]->(m:Movie) WITH m, count(a) AS actors WHERE actors > 3 RETURN m.title, actors",
"MATCH (p:Person)-[:ACTED_IN]->() WHERE p.born IS NOT NULL RETURN DISTINCT p.name, p.born ORDER BY p.born ASC LIMIT 1",
"MATCH (m:Movie) RETURN m.title, m.released ORDER BY m.released DESC LIMIT 1",
"MATCH (:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(co:Person) RETURN DISTINCT co.name",
"MATCH (k:Person {name: 'Keanu Reeves'})-[:ACTED_IN|DIRECTED|PRODUCED]->(m:Movie)<-[:ACTED_IN|DIRECTED|PRODUCED]-(p:Person) WHERE p <> k RETURN DISTINCT p.name",
"MATCH path = shortestPath((a:Person {name: 'Keanu Reeves'})-[*]-(b:Person {name: 'Tom Hanks'})) RETURN path",
"MATCH (k:Person {name: 'Kevin Bacon'})-[*1..2]-(p:Person) WHERE p <> k RETURN DISTINCT p.name",
"MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person) WITH d, collect(DISTINCT a.name) AS actors WHERE size(actors) > 1 RETURN d.name, actors",
"MATCH (a:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(b:Person {name: 'Meg Ryan'}) RETURN m.title",
"MATCH (d:Person)-[:DIRECTED]->(m:Movie) WITH d, count(m) AS n WHERE n >= 3 RETURN d.name, n",
"MATCH (p:Person)-[:ACTED_IN]->() WHERE NOT EXISTS { (p)-[:DIRECTED]->() } RETURN DISTINCT p.name",
"MATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:REVIEWED]-(p) RETURN p.name, m.title",
"MATCH (p:Person) WHERE EXISTS { (p)-[:ACTED_IN]->() } RETURN p.name, COUNT { (p)--() } AS c ORDER BY c DESC LIMIT 3",
]

with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password")) as d:
    for i, q in enumerate(qs, 1):
        recs, _, _ = d.execute_query(q)
        extra = f"  -> {dict(recs[0])}" if len(recs) == 1 else ""
        print(f"Q{i}: {len(recs)} rows{extra}")
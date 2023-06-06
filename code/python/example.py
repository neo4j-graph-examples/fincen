# pip3 install neo4j
# python3 example.py

from neo4j import GraphDatabase, basic_auth

cypher_query = '''
MATCH (from:Entity)<-[:ORIGINATOR]-(f:Filing)-[:BENEFITS]->(to:Entity)-[:COUNTRY]->(c:Country {name:$country})
 WITH from, to, round(sum(f.amount)) as sum
 ORDER BY sum DESC LIMIT 10
 RETURN from.name as originator
'''

with GraphDatabase.driver(
    "neo4j://<HOST>:<BOLTPORT>",
    auth=("<USERNAME>", "<PASSWORD>")
) as driver:
    result = driver.execute_query(
        cypher_query,
        country="Russia",
        database_="neo4j")
    for record in result.records:
        print(record['originator'])

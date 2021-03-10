# pip3 install neo4j-driver
# python3 example.py

from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "bolt://<HOST>:<BOLTPORT>",
  auth=basic_auth("<USERNAME>", "<PASSWORD>"))

cypher_query = '''
MATCH (from:Entity)<-[:ORIGINATOR]-(f:Filing)-[:BENEFITS]->(to:Entity)-[:COUNTRY]->(c:Country {name:$country})
 WITH from, to, round(sum(f.amount)) as sum
 ORDER BY sum DESC LIMIT 10
 RETURN from.name as originator
'''

with driver.session(database="neo4j") as session:
  results = session.read_transaction(
    lambda tx: tx.run(cypher_query,
                      country="Russia").data())
  for record in results:
    print(record['originator'])

driver.close()

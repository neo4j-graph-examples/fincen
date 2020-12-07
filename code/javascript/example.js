// npm install --save neo4j-driver
// node example.js
const neo4j = require('neo4j-driver');
const driver = neo4j.driver('bolt://<HOST>:<BOLTPORT>',
                  neo4j.auth.basic('<USERNAME>', '<PASSWORD>'), 
                  {/* encrypted: 'ENCRYPTION_OFF' */});

const query =
  `
  MATCH (from:Entity)<-[:ORIGINATOR]-(f:Filing)-[:BENEFITS]->(to:Entity)-[:COUNTRY]->(c:Country {name:$country})
  WITH from, to, round(sum(f.amount)) as sum
  ORDER BY sum DESC LIMIT 10
  RETURN from.name as originator
  `;

const params = {"country": "Russia"};

const session = driver.session({database:"neo4j"});

session.run(query, params)
  .then((result) => {
    result.records.forEach((record) => {
        console.log(record.get('originator'));
    });
    session.close();
    driver.close();
  })
  .catch((error) => {
    console.error(error);
  });

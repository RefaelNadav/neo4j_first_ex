

"""cypher
Copy code
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[r:FRIEND]->(b)
RETURN r
הסבר:

מוצאים את שני הצמתים (Alice ו-Bob).
יוצרים קשת מסוג FRIEND שמחברת את Alice ל-Bob.
מחזירים את הקשת שנוצרה.
מחיקת קשת
cypher
Copy code
MATCH (a:Person {name: "Alice"})-[r:FRIEND]->(b:Person {name: "Bob"})
DELETE r
הסבר:

מוצאים את הקשת FRIEND שמחברת בין Alice ל-Bob.
מוחקים את הקשת בלבד, מבלי למחוק את הצמתים.
שינוי סוג של קשר
cypher
Copy code
MATCH (a:Person {name: "Alice"})-[r:FRIEND]->(b:Person {name: "Bob"})
CREATE (a)-[r2:BEST_FRIEND]->(b)
DELETE r
RETURN r2
הסבר:

מוצאים את הקשת FRIEND.
יוצרים קשת חדשה מסוג BEST_FRIEND.
מוחקים את הקשת הישנה (FRIEND).
עדכון תכונות של קשת
cypher
Copy code
MATCH (a:Person {name: "Alice"})-[r:FRIEND]->(b:Person {name: "Bob"})
SET r.since = date("2020-01-01")
RETURN r
הסבר:

מוצאים את הקשת FRIEND.
מוסיפים או מעדכנים את התכונה since עם ערך של תאריך.
מחיקת כל הקשרים הקשורים לצומת מסוים
cypher
Copy code
MATCH (a:Person {name: "Alice"})-[r]->()
DELETE r
הסבר:

מוצאים את כל הקשרים שיוצאים או נכנסים לצומת Alice.
מוחקים את כל הקשרים האלו.
יצירת קשר עם תכונות
cypher
Copy code
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[r:FRIEND {since: date("2022-01-01"), level: "close"}]->(b)
RETURN r
הסבר:

יוצרים קשת עם תכונות since (תאריך יצירת הקשר) ו-level (רמת הקשר).
עדכון מספר קשרים לצומת אחד
cypher
Copy code
MATCH (a:Person {name: "Alice"})-[r:FRIEND]->(b:Person)
SET r.level = "acquaintance"
RETURN r
הסבר:

מעדכנים את התכונה level לכל הקשרים מסוג FRIEND שמחברים את Alice לצמתים אחרים.
"""
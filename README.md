# Keto calc


TODO
Database:
Products (name, protein, fat, fibre, carbs, price per pack(PPP), grams per pack(GPP))
^ Done
Each day separate table
^ Done
Altering tables

Macro calc (depending on lifestyle)
^ Use classes

User info (sex, age, weight, height)
^ Use classes

Calculate price per meal, choose products, enter gram values, return nutr info and price
^ Partly done

Desired protein intake
^ Count as macro calc - ?

Mitigate SQL injection, user input needs to be validated

What other exploits needs to be mitigated? - Search and read

SQL injection for floating/integers can be mitigated by confirming it's int floating/integer
The rest can be mitigated by parameterized SQL
https://blog.codinghorror.com/give-me-parameterized-sql-or-give-me-death/

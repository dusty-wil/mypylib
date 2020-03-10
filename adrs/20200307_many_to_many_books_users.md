# Many-To-Many Books to Users 2020-03-07
## Context
More than one user may have purchased the same book. Allowing two users to enter the same book might 
violate data consistency
## Decision
Place notes and purchase date fields in an association table and create relationships between association, 
books, and users.
## Consequences
+ Allows for easier implementation of a system for users to search for books already entered later, addresses
  users entering multiple instances of the same book. 
- Made the database design process take longer.
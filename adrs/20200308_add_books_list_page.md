# Add Books List Page 2020-03-08
## Context
Adding the association table for Users and Books added some complexity in terms of how a book is
handled when one user removes it  from their library, but another user still has it in theirs
## Decision
Add a page to show a list of all books in the system, whether they are owned or not. Allow users to 
add and edit books from this page as well.
## Consequences
- Complicates the solution somewhat as users now need to differentiate between editing books and
  editing the information about their specific instance of a book. 
- Book editing is done on a separate page
- Users can't delete books, they can only delete their library entry for a book
+ Helps with data consistency
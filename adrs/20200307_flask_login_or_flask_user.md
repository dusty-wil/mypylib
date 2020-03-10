# flask-login or flask-user 2020-03-07
## Context
Two options given for user login handling.
## Decision
Implemented login functionality with flask-login. This was chosen because it seemed to be 
more light-weight; flask-login seems to focus mainly on the aspects of authentication
needed for this specific implementation, especially since the application uses a custom email
implementation.
## Consequences
+ Easy to get going, easy api documentation resulted in rapid implementation of authentication.
+ Might make expansion of authentication and email blueprints easier as development progresses 
  and more custom functionality is added.


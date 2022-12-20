Flask while threading is used for 202 + long tasks.
It addresses the case of a client that request some long task from the server, while  
- the server responds with 202 and process the request 
- the client can wait in some loop  

Other possible solutions for long task are:
- long polling - undesirable
- celery with message broker - It provides other advantages, like a client that is free, multiple workers, etc. 


Refs:
* https://zoltan-varadi.medium.com/flask-api-how-to-return-response-but-continue-execution-828da40881e7

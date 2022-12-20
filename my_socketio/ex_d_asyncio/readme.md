


**Why aiohttp?**  
When a client has to send several requests for which the server(s) has/have to process for some time per each request  
(typically in parallel), it is better for the client work asynchronously and await for the responses.  

A related topic is gunicorn and websocket. Maybe Gunicorn can use a worker that is compatible with websocket,  
but another possibility seems to replace is with uvicorn and use http 

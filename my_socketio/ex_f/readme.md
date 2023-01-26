

Client:
Sends some request
TBD how I use the websocket

Server:
A gunicorn/uvicorn runs the flask app. E.g. 4 workers.
A flask application performs something and sends back to the webhook.
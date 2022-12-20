# socketio
Learn python socketio
References:
  * https://python-socketio.readthedocs.io/en/latest/

## Example a (client_a and server_a):
**Features**
 * Bidirectional traffic between clients and server. Only one client appears in this example, but the sid can  
be the basis for supporting multiple clients,  
along with rooms and namespaces that are not used in this basic example as well ==> todo (worth checking)
 * The client can do some async background task while the server is processing its request.  
Note that the server is synchronous and in this example it responses only after it finishes it processing.  
It is not clear for me whether the server could use sio.start_background_task as the client does (==> todo worth checking)  
but anyway a better way seems to be using threading as used in ex_b.

**Notes:**  
* **sid** - On connect the server creates the sid that 
In the example the client "connect" contains also emit login + credentials that could be processed by the server  
* **background process** As commonly required

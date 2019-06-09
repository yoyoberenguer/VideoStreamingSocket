## Video and sound streaming through tcp/udp socket (client/server application)

This algorithm written in python is showing how to transfer a video and sound data over a tcp socket connection.

You will need the following python libraries install on your system if you are trying to run the code from source.
```
1. socket       # for creating socket object
2. threading    # used for Subclassing code to run in parallel
3. pygame       # for displaying the video on the server and client  
4. lz4          # for compression
```

Start the client socket first then the server socket in a command prompt. 

Your firewall may display a message in order to allow the socket to run on your system, 
allow the present connection for both
```
ClientSocket -a 192.168.1.112 -p 16815
ServerSocket -a 192.168.1.112 -p 16815 
```
Note : _For this application to work, don't forget to add the folder Assets in the same 
directory as the currently running server socket application._


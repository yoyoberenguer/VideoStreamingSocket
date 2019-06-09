## Video and sound streaming through tcp/udp socket (client/server application)

This algorithm written in python is showing how to transfer a video and sound data over a tcp socket connection.

You will need the following python libraries install on your system if you try to run the code from source.
```
1. socket       # for creating socket object
2. threading    # used for Subclassing code to run in parallel
3. pygame       # for displaying the video on the server and client  
```

Start the client socket first then the server socket in a command prompt
```
ClientSocket -a 192.168.1.112 -p 16815
ServerSocket -a 192.168.1.112 -p 16815 
```

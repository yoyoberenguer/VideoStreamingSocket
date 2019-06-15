## Video and sound streaming through a tcp socket (client/server application)

This algorithm written in python is showing how to transfer a video and sound data over a tcp socket connection.

You will need the following python libraries install on your system if you are trying to run the code from source.
```
1. socket       # for creating socket object
2. threading    # used for Subclassing code to run in parallel
3. pygame       # for displaying the video on the server and client  
4. lz4          # for compression
5. pyinstaller  # to build executable files (pip install pyinstaller)
```

Start the client socket first; then start the server socket in a command prompt. 
Your firewall/anti-virus may display a message in order to allow the socket to run on your system, 
please allow the connection for both sockets.
```
ClientSocket -a 192.168.1.112 -p 16815
ServerSocket -a 192.168.1.112 -p 16815 
```
*Note* : _For this application to work, don't forget to add the folder Assets in the same 
directory as the currently running server socket application._

Tasks on the server side:

1. Surface is halfed in order to limit the quantity of bytes to transfer throughout the network.
2. Server dataframe are encoded with LZ4 algo before being send to the client.
3. Display the surface onto the screen

Tasks on the client side: 

1. The data are collected and decompress when all the packets have been collected. 
2. Surface is build with the function pygame.image.frombuffer 
3. Surface is then scale 2x before being display on the client screen.

*Note* : _To create an excutable file from the source code, do the following_

```
pyinstaller --onefile ClientSocket.py
pyinstaller --onefile ServerSocket.py 
```

You will find the executables in the <<dist>> directory.Cut and paste the files in the main branch where directories Assets, build and dist are located.




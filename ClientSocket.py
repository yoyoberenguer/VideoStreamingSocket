import socket
import threading
import pygame
import lz4.frame
from Global import GL
import argparse


class VideoSocketClientUdp(threading.Thread):

    def __init__(self,
                 host_,  # host address
                 port_,  # port value
                 screen_,  # display
                 ):

        """
        Create a socket server to received video data frames
        :param host_: String corresponding to the server address
        :param port_: Integer used for the port.
                      Port to listen on (non-privileged ports are > 1023) and 0 < port_ < 65535
        :param screen_: pygame.Surface, display
        """

        assert isinstance(host_, str), \
            'Expecting string for argument host_, got %s instead.' % type(host_)
        assert isinstance(port_, int), \
            'Expecting integer for argument port_, got %s instead.' % type(port_)
        assert isinstance(screen_, pygame.Surface), \
            'Expecting pygame.Surface for argument screen_, got %s instead.' % type(screen_)
        # Port to listen on (non-privileged ports are > 1023)
        assert 0 < port_ < 65535, \
            'Incorrect value assign to port_, 0 < port_ < 65535, got %s ' % port_
        threading.Thread.__init__(self)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host_
        self.port = port_
        try:
            # Bind the socket to the port
            self.sock.bind((host_, port_))
        except socket.error as error:
            print('\n[-] Error : %s ' % error)
            raise SystemExit

        self.screen = screen_
        self.size = GL.SIZE

    def run(self):

        frame = 0

        while not GL.STOP.isSet():

                buffer = b''
                image = None
                self.size = GL.SIZE

                try:
                    # Receive the data in small chunks
                    while self.size > 0 and not GL.STOP.isSet():

                        # get data
                        data, addr = self.sock.recvfrom(GL.BUFFER)

                        if self.size >= 1024:
                            buffer += data
                            self.size -= len(data)

                        else:
                            buffer += data[:self.size]
                            self.size -= len(data)

                    if len(buffer) != GL.SIZE:
                        image = None
                    else:
                        image = pygame.image.frombuffer(
                            buffer, (GL.SCREEN[0] >> 1, GL.SCREEN[1] >> 1), 'RGB')
                        # adjust the surface to match the screen size ( texture received = screensize /2 )
                        image = pygame.transform.scale2x(image)

                finally:
                    # display surface
                    if image is not None and not GL.STOP.isSet():
                        # print('[+] Info, playing frame number: ', frame)
                        self.screen.blit(image, (0, 0))
                        pygame.display.flip()

                    GL.CLIENT_FRAME = frame
                    frame += 1

        # Clean up the connection
        self.sock.close()
        print('\n[-] Socket server thread is now terminated.')



class VideoSocketClient(threading.Thread):

    def __init__(self,
                 host_,  # host address
                 port_,  # port value
                 screen_,  # display
                 ):

        """
        Create a socket server to received video data frames
        :param host_: String corresponding to the server address
        :param port_: Integer used for the port.
                      Port to listen on (non-privileged ports are > 1023) and 0 < port_ < 65535
        :param screen_: pygame.Surface, display
        """

        assert isinstance(host_, str), \
            'Expecting string for argument host_, got %s instead.' % type(host_)
        assert isinstance(port_, int), \
            'Expecting integer for argument port_, got %s instead.' % type(port_)
        assert isinstance(screen_, pygame.Surface), \
            'Expecting pygame.Surface for argument screen_, got %s instead.' % type(screen_)
        # Port to listen on (non-privileged ports are > 1023)
        assert 0 < port_ < 65535, \
            'Incorrect value assign to port_, 0 < port_ < 65535, got %s ' % port_
        threading.Thread.__init__(self)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Bind the socket to the port
            self.sock.bind((host_, port_))
        except socket.error as error:
            print('\n[-] Error : %s ' % error)
            raise SystemExit

        try:
            # Listen for incoming connections
            self.sock.listen(1)
        except socket.error as error:
            print('\n[-] Error : %s ' % error)
            raise SystemExit

        self.screen = screen_
        self.rect = self.screen.get_size()

    def run(self):

        frame = 0

        while not GL.STOP.isSet():

            # Wait for a connection
            connection, client_address = self.sock.accept()
            buffer = b''
            image = None
            try:
                # Receive the data in small chunks
                while not GL.STOP.isSet():

                    data = connection.recv(8192)

                    if data == b'quit':
                        print('Video socket aborting')
                        GL.STOP.set()
                        break

                    else:
                        # build the frame by adding data chunks
                        if len(data) > 0:
                            buffer += data

                        else:

                            # Decompress the data frame
                            decompress_data = lz4.frame.decompress(buffer)

                            if len(decompress_data) != GL.SIZE:
                                image = None
                            else:
                                # Create a pygame surface from the string buffer
                                image = pygame.image.frombuffer(
                                    decompress_data, (self.rect[0] >> 1, self.rect[1] >> 1), 'RGB')
                                # adjust the surface to match the screen size ( texture received = screensize /2 )
                                image = pygame.transform.scale2x(image)
                            break

            finally:
                # Clean up the connection
                connection.close()

                if image is not None and not GL.STOP.isSet():
                    # print('[+] Info, playing frame number: ', frame)
                    self.screen.blit(image, (0, 0))
                    pygame.display.flip()

                frame += 1

        print('\n[-] Video client thread is now terminated.')


class SoundSocketClient(threading.Thread):

    def __init__(self,
                 host_,  # host address
                 port_,  # port value
                 screen_,  # display
                 ):

        """
        Create a socket server to received sound data frames
        :param host_: String corresponding to the server address
        :param port_: Integer used for the port.
                      Port to listen on (non-privileged ports are > 1023) and 0 < port_ < 65535
        :param screen_: pygame.Surface, display
        """

        assert isinstance(host_, str), \
            'Expecting string for argument host_, got %s instead.' % type(host_)
        assert isinstance(port_, int), \
            'Expecting integer for argument port_, got %s instead.' % type(port_)
        assert isinstance(screen_, pygame.Surface), \
            'Expecting pygame.Surface for argument screen_, got %s instead.' % type(screen_)
        # Port to listen on (non-privileged ports are > 1023)
        assert 0 < port_ < 65535, \
            'Incorrect value assign to port_, 0 < port_ < 65535, got %s ' % port_
        threading.Thread.__init__(self)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Bind the socket to the port
            self.sock.bind((host_, port_))
        except socket.error as error:
            print('\n[-] Error : %s ' % error)
            raise SystemExit

        try:
            # Listen for incoming connections
            self.sock.listen(1)
        except socket.error as error:
            print('\n[-] Error : %s ' % error)
            raise SystemExit

        self.screen = screen_
        self.rect = self.screen.get_size()

    def run(self):

        frame = 0

        while not GL.STOP.isSet():

            # Wait for a connection
            connection, client_address = self.sock.accept()
            buffer = b''
            image = None
            try:
                # Receive the data in small chunks
                while not GL.STOP.isSet():
                    data = connection.recv(8192)

                    if data == b'quit':
                        print('Sound socket aborting')
                        GL.STOP.set()
                        break

                    else:
                        # build the sound by adding data chunks
                        if len(data) > 0:
                            buffer += data

                        else:
                            # Decompress the data frame
                            decompress_data = lz4.frame.decompress(buffer)
                            sound = pygame.mixer.Sound(decompress_data)
                            sound.play()
                            break

            finally:
                # Clean up the connection
                connection.close()
                if image is not None and not GL.STOP.isSet():
                    print('[+] Info, playing frame number: ', frame)
                frame += 1

        print('\n[-] Sound client thread is now terminated.')


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--address", required=False, default='192.168.1.106', help="Server ip address")
    ap.add_argument("-p", "--port", required=False, default='1600', help="Port to use")
    args = vars(ap.parse_args())

    SCREENRECT = pygame.Rect(0, 0, GL.SCREEN[0], GL.SCREEN[1])
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWACCEL, 32)
    SCREEN.set_alpha(None)
    pygame.display.set_caption('Client')
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4095)
    pygame.display.flip()

    # host = '192.168.1.106'
    # port = 16584
    host = args['address']
    port = int(args['port'])

    # video socket
    # th = VideoSocketClientUdp(host, port, SCREEN)

    # th.start()
    VideoSocketClient(host, port, SCREEN).start()

    # Sound socket
    SoundSocketClient(host, port - 1, SCREEN).start()
    CLOCK = pygame.time.Clock()
    while not GL.STOP.isSet():
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break

        pygame.display.flip()

    GL.STOP.set()
    pygame.quit()

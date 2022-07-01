import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
active_clients = []


def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f'empty message from {username}')


def send_messages_to_client(client, message):
    client.sendall(message.encode())

def send_messages_to_all(message):
    for user in active_clients:
        send_messages_to_client(user[1], message)


def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print('empty username')
    threading.Thread(target=listen_for_messages, args=(client, username)).start()


def server_start():
    print('server starting')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print('server up')
    except:
        print(f'unable to bind to ', {HOST}, 'and', {PORT})
    while 1:
        client, address = server.accept()
        print('user connected')
        threading.Thread(target=client_handler, args=(client, )).start()


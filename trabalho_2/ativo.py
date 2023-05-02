import socket

# configuracao do socket
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

# criacao do socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conexao com o servidor
client_socket.connect((HOST, PORT))

while True:
    # solicitacao de acao ao usuario
    action = input("Digite a ação (GET, REMOVE ou ADD): ")
    if action not in ['GET', 'REMOVE', 'ADD']:
        print("Ação inválida. Tente novamente.")
        continue

    # solicitação de palavra-chave ao usuário
    word = input("Digite a palavra-chave: ")
    
    # envio de mensagem ao servidor
    message = f"{action} {word}"
    client_socket.send(message.encode())

    # recebimento de resposta do servidor
    data = client_socket.recv(BUFFER_SIZE)
    print(data.decode())

# fechamento do socket
client_socket.close()
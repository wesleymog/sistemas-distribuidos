import socket
import json

HOST = 'localhost'
PORT = 5000
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(f'Conectado a {self.host}:{self.port}')
    def run(self):
        while True:
            command = input('Digite o comando (GET, ADD, REMOVE, SAVE) ou EXIT para sair: ')
            if command == 'EXIT':
                break
            if command in ['GET', 'ADD', 'REMOVE']:
                word = input('Digite a palavra: ')
            


            # Se for o comando ADD, pede a definição e envia para o servidor
            if command == 'ADD':
                definition = input('Digite a definicao: ')
                data = json.dumps({'word': word, 'definition': definition})
                self.sock.sendall(f'{command}->{data}'.encode())
            else:
                # Envia a mensagem com o comando e a palavra para o servidor
                message = f'{command}->{word}'
                self.sock.sendall(message.encode())
            # Se for o comando REMOVE ou SAVE, pede a senha e envia para o servidor
            if command == 'REMOVE' or command == 'SAVE':
                password = input('Digite a senha: ')
                self.sock.sendall(password.encode())
            # Processa a resposta do servidor
            data = self.sock.recv(1024)
            print(data.decode())

            

if __name__ == '__main__':
    client = Client(HOST, PORT)
    client.run()
import socket
import threading

class DictionaryServer:
    def __init__(self):
        self.dict_lock = threading.Lock()
        self.dictionary = {}

    def add_word(self, word, definition):
        with self.dict_lock:
            self.dictionary[word] = definition

    def remove_word(self, word):
        with self.dict_lock:
            if word in self.dictionary:
                del self.dictionary[word]
                return True
            else:
                return False

    def get_definition(self, word):
        with self.dict_lock:
            return self.dictionary.get(word)

class ClientThread(threading.Thread):
    def __init__(self, client_socket, dictionary):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.dictionary = dictionary

    def run(self):
        print(f"Nova conexao: {self.client_socket}")
        while True:
            try:
                # Recebe a mensagem do cliente
                data = self.client_socket.recv(1024)
                if not data:
                    break
                
                # Decodifica a mensagem e separa o comando da palavra
                message = data.decode()
                command, word = message.split()

                # Processa o comando e envia a resposta
                if command == "GET":
                    definition = self.dictionary.get_definition(word)
                    if definition:
                        self.client_socket.send(definition.encode())
                    else:
                        self.client_socket.send("Palavra nao encontrada".encode())
                elif command == "ADD":
                    definition = self.client_socket.recv(1024).decode()
                    self.dictionary.add_word(word, definition)
                    self.client_socket.send("Palavra adicionada com sucesso".encode())
                elif command == "REMOVE":
                    if self.dictionary.remove_word(word):
                        self.client_socket.send("Palavra removida com sucesso".encode())
                    else:
                        self.client_socket.send("Palavra nao encontrada".encode())
            except Exception as e:
                print(f"Erro: {e}")
                break
        
        print(f"Conexao fechada: {self.client_socket}")
        self.client_socket.close()

class DictionaryServerSocket:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dictionary = DictionaryServer()

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            # Espera por novas conexoes de clientes
            client_socket, client_address = self.server_socket.accept()
            print(f"Nova conexao recebida: {client_address}")

            # Cria uma nova thread para atender o cliente
            client_thread = ClientThread(client_socket, self.dictionary)
            client_thread.start()

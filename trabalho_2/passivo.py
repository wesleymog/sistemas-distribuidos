import os
import socket
import threading
import json
import hashlib


HOST = 'localhost'
PORT = 5000
JSON_FILE = "dictionary.json"
HASH_PASSWORD = "79809644a830ef92424a66227252b87bbdfb633a9dab18ba450c1b8d35665f20"

class Data:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.load_json()

    def load_json(self):
        try:
            with open(self.json_file) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        return data

    def save_json(self):
        with open(self.json_file, 'w') as f:
            json.dump(self.data, f)
class Dictionary:
    def __init__(self, data: Data):
        self.dict_lock = threading.Lock()
        self.json_data = data        
        self.dictionary= data.data

    def add_word(self, word, definition):
        with self.dict_lock:
            if word not in self.dictionary:
                self.dictionary[word] = []
            self.dictionary[word].append(definition)

    def remove_word(self, word):
        with self.dict_lock:
            if word in self.dictionary:
                del self.dictionary[word]
                return True
            else:
                return False

    def get_definition(self, word):
        with self.dict_lock:
            return self.dictionary.get(word, [])

    def save_dictionary(self, password):
        # Gera hash da senha
        hash_password = hashlib.sha256(password.encode()).hexdigest()
                # Verifica se a senha está correta
        if hash_password != HASH_PASSWORD:
            return "Senha incorreta"
        # Abre o arquivo de saída em modo de escrita
        data.data = self.dictionary
        data.save_json()
        
        # Retorna uma mensagem de confirmação
        return f"Dicionário salvo com sucesso com a senha!"

    def remove_word_with_password(self, word, password):
        # Gera hash da senha
        hash_password = hashlib.sha256(password.encode()).hexdigest()

        # Verifica se a senha está correta
        if hash_password != HASH_PASSWORD:
            return "Senha incorreta"

        # Remove a palavra
        with self.dict_lock:
            if word in self.dictionary:
                del self.dictionary[word]
                return "Palavra removida com sucesso"
            else:
                return "Palavra não encontrada"

class Server(threading.Thread):
    def __init__(self, client_socket, dictionary):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.dictionary = dictionary

    def run(self):
        print(f"Nova conexao: {self.client_socket}")
        while True:
            # Recebe a mensagem do cliente
            data = self.client_socket.recv(1024)
            if not data:
                break
            
            # Decodifica a mensagem e separa o comando da palavra
            print(data.decode('utf-8'))
            message = data.decode()
            command, word = message.split("->")
            print(command)
            print(word)
            if command == "ADD":
                word_dict = json.loads(word)
                word = word_dict["word"]
            print(f"vamos começar o {command} {word}")
            # Processa o comando e envia a resposta
            if command == "GET":
                definitions = self.dictionary.get_definition(word)
                response = "\nOs significados encontrados foram: "
                if definitions:
                    response = response + ", ".join(definitions)
                    print(response)
                    self.client_socket.send(response.encode())
                else:
                    self.client_socket.send("Palavra nao encontrada".encode())
            elif command == "ADD":
                definition = word_dict['definition']
                self.dictionary.add_word(word, definition)
                self.client_socket.send("Palavra adicionada com sucesso".encode())
            elif command == "REMOVE":
                password = self.client_socket.recv(1024).decode()
                response = self.dictionary.remove_word_with_password(word, password)
                self.client_socket.send(response.encode())
            elif command == "SAVE":
                password = self.client_socket.recv(1024).decode()
                response = self.dictionary.save_dictionary(password)
                self.client_socket.send(response.encode())
            else:
                self.client_socket.send("Comando invalido".encode())
            # except Exception as e:
            #     print(f"Erro: {e}")
            #     break
        
        print(f"Conexao fechada: {self.client_socket}")
        self.client_socket.close()

if __name__ == "__main__":
    # Cria um servidor e inicia a escuta por conexões
    data = Data(JSON_FILE)
    dictionary = Dictionary(data)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor rodando em {HOST}:{PORT}")

    # Loop infinito para aceitar novas conexões e criar threads para lidar com cada uma
    while True:
        # Aceita uma nova conexão
        client_socket, address = server_socket.accept()
        print(f"Nova conexão de {address}")

        # Cria uma nova thread para lidar com a conexão
        client_thread = Server(client_socket, dictionary)
        client_thread.start()
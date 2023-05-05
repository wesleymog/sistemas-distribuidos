import os
import socket
import threading
import json
import hashlib


HOST = 'localhost'
PORT = 5000
JSON_FILE = "dictionary.json"
HASH_PASSWORD = "79809644a830ef92424a66227252b87bbdfb633a9dab18ba450c1b8d35665f20"

class DictionaryServer:
    def __init__(self):
        self.dict_lock = threading.Lock()
        # Abre o arquivo de saída em modo de escrita
        if os.path.isfile(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                # Escreve o dicionário em JSON no arquivo
                self.dictionary= json.load( f)
        else:
            with open(JSON_FILE, "w") as f:
                json.dump({}, f)

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
        with open(JSON_FILE, "w") as f:
            # Escreve o dicionário em JSON no arquivo
            json.dump(self.dictionary, f)
        
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

class ClientThread(threading.Thread):
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
                    response = response + " , ".join(definitions)
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
    server = DictionaryServer()
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
        client_thread = ClientThread(client_socket, server)
        client_thread.start()
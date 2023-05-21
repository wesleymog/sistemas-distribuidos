#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Servidor de echo usando RPC 
import rpyc #modulo que oferece suporte a abstracao de RPC
import json
import hashlib

#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ForkingServer 

# porta de escuta do servidor de echo
PORTA = 10001
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
        self.json_data = data        
        self.dictionary= data.data

    def add_word(self, word, definition):
        if word not in self.dictionary:
            self.dictionary[word] = []
        self.dictionary[word].append(definition)
        return f"Palavra {word} adicionada ao Dicionário!"

    def remove_word(self, word):
        if word in self.dictionary:
            del self.dictionary[word]
            return True
        else:
            return False

    def get_definition(self, word):
        definitions = self.dictionary.get(word, [])
        definitions.sort()
        return f'As definições para a palavra {word} encontradas foram: {definitions}'

    def save_dictionary(self):
        # Abre o arquivo de saída em modo de escrita
        self.json_data.save_json()

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
                return f"Palavra {word} removida com sucesso"
            else:
                return f"Palavra {word} não encontrada"

# classe que implementa o servico de echo
class Server(rpyc.Service):
    def __init__(self):
        data = Data(JSON_FILE)
        dictionary = Dictionary(data)        
        self.dictionary = dictionary
            
    def on_disconnect(self, conn):
        self.dictionary.save_dictionary()
        print("Conexao finalizada")
    
    def exposed_remove_word(self, word, password):
        response = self.dictionary.remove_word_with_password(word, password)
        return response

    def exposed_add_word(self, word, definition):
        response = self.dictionary.add_word(word, definition)
        return response

    def exposed_get_word(self, word):
        response = self.dictionary.get_definition(word)
        return response
	# executa quando uma conexao eh criada
    def on_connect(self, conn):
        print("Conexão iniciada...")
  
# dispara o servidor
if __name__ == "__main__":
	srv = ForkingServer(Server, port = PORTA)
	srv.start()


### Tipos de servidores
#https://rpyc.readthedocs.io/en/latest/api/utils_server.html

#servidor que dispara uma nova thread a cada conexao
#from rpyc.utils.server import ThreadedServer

#servidor que atende uma conexao e termina
#from rpyc.utils.server import OneShotServer

### Configuracoes do protocolo RPC
#https://rpyc.readthedocs.io/en/latest/api/core_protocol.html#rpyc.core.protocol.DEFAULT_CONFIG
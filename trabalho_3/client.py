#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC
import json
# endereco do servidor de echo
SERVIDOR = 'localhost'
PORTA = 10001

def iniciaConexao():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(SERVIDOR, PORTA) 
	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

class Client:
    def __init__(self):
        self.conn = rpyc.connect(SERVIDOR, PORTA) 
        print(type(self.conn.root)) # mostra que conn.root eh um stub de cliente
        print(self.conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

    def run(self):
        while True:
            command = input('Digite o comando (GET, ADD, REMOVE, SAVE) ou EXIT para sair: ')
            if command == 'EXIT':
                break
            if command in ['GET', 'ADD', 'REMOVE']:
                word = input('Digite a palavra: ')
                if command == 'ADD':
                    definition = input('Digite a definicao: ')
                    response = self.conn.root.exposed_add_word(word, definition)
                elif command == 'REMOVE':
                    password = input('Digite a senha: ')
                    response = self.conn.root.exposed_remove_word(word, password)
                elif command == 'GET':
                    response = self.conn.root.exposed_get_word(word)
                print(response)
            else:
                print('Invalid command')
        self.conn.close()
            


if __name__ == '__main__':
    client = Client()
    client.run()
# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5201        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

# Envia 20 mensagens para o servidor
for i in range(20):
    message = f'Mensagem {i+1}'
    print('Enviando:', message)
    sock.sendall(message.encode())
    data = sock.recv(1024)
    print('Recebido:', data.decode())

# Envia a mensagem "fim" para fechar a conexão com o servidor
message = "fim"
print('Enviando:', message)
sock.sendall(message.encode())

# Fecha o socket
sock.close()
# Lab 2 - Distributed systems 

These programs was developed to the second laboratory exercise for distributed systems classes and follows these [requirements](https://drive.google.com/file/d/1Cv1yoJqKsPTxoiKggyngISPaelmUozpb/view)

## Getting Started
### Atividade 1
Objetivo: Projetar a arquitetura de software da solução. A arquitetura de software deverá conter, no mínimo, tres componentes distintos: (i) acesso e persistência de dados;(ii) processamento das requisições; e (iii) interface com o usuário;

#### Resposta:
A camada de dados é responsável pela persistência dos dados e lida com a manipulação dos mesmos. A classe Data representa esta camada e é responsável por carregar e salvar os dados em um arquivo JSON.
A camada de lógica de negócios é responsável por executar as operações do sistema e implementar as regras de negócios. A classe Dictionary representa esta camada e é responsável por adicionar, remover, obter definições e salvar um dicionário. Além disso, esta camada inclui a criptografia de senha, que é necessária para remover ou salvar o dicionário.
Por fim, a camada de apresentação é a camada superior, que lida com a interação do usuário e a exibição dos resultados. A classe Client representa esta camada e é responsável por obter entrada do usuário e exibir as saídas do servidor. Enquanto a classe Server é responsável por receber as solicitações do cliente, executar as operações solicitadas e enviar a resposta de volta ao cliente.
Embora as camadas estejam claramente separadas, há uma interação intensa entre elas. Por exemplo, a camada de apresentação interage com a camada de lógica de negócios por meio do servidor, e a camada de lógica de negócios interage com a camada de dados por meio da classe Data.

### Atividade 2
Objetivo: Instanciar a arquitetura de software da aplicação (definida na Atividade 1) 
para uma arquitetura de sistema cliente/servidor de dois níveis, com um servidor e
um cliente. O lado servidor abrigara o dicionário remoto, enquanto o lado cliente ficará
responsável pela interface com o usuário.

#### Roteiro:
1. Defina quais componentes ficarão do lado do cliente.
2. Defina quais componentes ficarão do lado do  servidor.
3. Defina o conteúdo e a ordem das mensagens que serão trocadas entre cliente e  servidor, e quais ações cada lado devera tomar quando receber uma mensagem.  
Essa comunicação ficará responsável por fazer a “cola” entre os componentes instanciados em máquinas distintas. 

#### Resposta:
Do lado do cliente, teremos a classe Client, responsável por estabelecer a conexão com o servidor e gerenciar a entrada e saída de dados com o usuário.
Do lado do servidor, teremos a classe Server, responsável por receber as conexões dos clientes, processar as mensagens recebidas e enviar respostas para o cliente. Além disso, teremos a classe Dictionary que abrigará o dicionário e será acessada pelo servidor sempre que necessário.
A ordem das mensagens que serão trocadas entre cliente e servidor serão definidas pelos comandos de entrada fornecidos pelo usuário. O cliente enviará comandos para o servidor e este, por sua vez, responderá ao cliente de acordo com a ação solicitada. Por exemplo, caso o usuário digite o comando 'GET', o cliente enviará essa mensagem ao servidor, que, por sua vez, consultará o dicionário para encontrar a definição da palavra fornecida e enviará a resposta para o cliente. A mesma lógica será seguida para os comandos 'ADD', 'REMOVE' e 'SAVE'.

### Dependencies

* Python 3

### Executing program

* To run the program you just need to run the following command in two differents terminals.
##### Ativo run steps
```
python ativo.py
```
##### Passivo run steps
```
python passivo.py
```

## Authors

Contributors names and contact info

* Wesley Mota  
* [@Wesleymog](https://github.com/wesleymog)

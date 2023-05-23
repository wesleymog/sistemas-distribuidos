# Lab 3 - Distributed systems 

These programs was developed to the third laboratory exercise for distributed systems classes and follows these [requirements](https://drive.google.com/file/d/1Q92bBrMrNRgFN7lApVq-z7h3zHA_y1MR/view)

## Getting Started
### Goal
O objetivo deste Laboratório é praticar a abstração de Chamada Remota de Procedimento (RPC).
Vamos reimplementar o dicionário remoto do Laboratório 2 (com algumas alterações, descritas abaixo), agora usando um middleware RPC (RPyC). As chaves e valores do dicionário serão strings. O dicionário deverá ser armazenado em disco para ser restaurado em uma execução futura.


### Dependencies

* Python 3
* Rpyc
### Installing dependencies

```
pip install rpyc
```

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

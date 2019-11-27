def incluirProd(prod, tipo, quant, dataf, datav):
    try:
        # abre o arquivo para adição de dados
        arq = open('estoque.txt', 'a')

        # obtém data e hora do sistema
       # from datetime import datetime
        # agora = datetime.now()
        # data = agora.strftime('%d/%m/%Y')
        # hora = agora.strftime('%H:%M:%S')

        # grava os dados no arquivo
        arq.write(prod + ';' + tipo + ';' + quant + ';' + dataf + ';' + datav + ';' + '\n')
        arq.close()

        # retorna indicativo de 'ok' (1) ou 'erro' (0)
        conexao.send('1'.encode())
    except:
        conexao.send('0'.encode())


def pesquisarProd(prod):
    try:
        # lista irá acumular os dados a serem retornados
        lista = ''

        arq = open('estoque.txt', 'r')
        linhas = arq.readlines()
        arq.close()

        for linha in linhas:
            partes = linha.split(';')

            if partes[0] == prod:
                lista += partes[0] + ';' + partes[1] + ';' + partes[2] + ';' + partes[3] + ';' + partes[4] + '#'

        if lista == '':
            conexao.send('0'.encode())
        else:
            conexao.send(lista[:-1].encode())

    except:
        conexao.send('0'.encode())


def listar():
    try:
        # lista irá acumular os dados a serem retornados
        lista = ''

        arq = open('estoque.txt', 'r')
        linhas = arq.readlines()
        arq.close()

        for linha in linhas:
            partes = linha.split(';')

            if partes[0] == prod:
                lista += partes[0]+';'+partes[1]+';'+partes[2]+';'+partes[3]+';'+partes[4]+'#'

        if lista == '':
            conexao.send('0'.encode())
        else:
            conexao.send(lista[:-1].encode())

    except:
        conexao.send('0'.encode())



def excluiProd(prod):
    try:
        # abre o arquivo para leitura
        arq = open('estoque.txt', 'r')
        # lê todas as linhas do arquivo
        linhas = arq.readlines()
        # fecha o arquivo
        arq.close()

        while True:
            existe = 0
            # obtém o tamanho do vetor
            tam = len(linhas)
            numLinha = -1

            for i in range(0, tam):
                partes = linhas[i].split(';')
                numLinha = numLinha + 1
                if partes[0] == prod:
                    # retira a linha do vetor
                    linhas.pop(numLinha)
                    existe = 1
                    break

            if existe == 0:
                break

        # Deve-se agora gravar todas as linhas (exceto as excluídas) no arq
        # cria o arquivo novamente
        arq = open('estoque.txt', 'w')

        # percorre e adiciona todas as linhas "que sobraram"
        for linha in linhas:
            arq.write(linha)

        # fecha o arquivo
        arq.close()

        # envia a indicação de exclusão correta
        conexao.send("1".encode())
    except:
        conexao.send("0".encode())


# ------------------------------------
# Programa Principal
# ------------------------------------
import socket

host = ""
porta = 1060

# define protocolo (IPV_4, TCP)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# inicia a escuta do lado do servidor
servidor.bind((host, porta))

print('Aguardando conexões dos clientes...')

# número de conexões na fila
servidor.listen(1)

# recebe uma nova conexão
conexao, endereco = servidor.accept()

print(f'Conectado por: {endereco}')

while True:
    # recebe os dados enviados pelo cliente
    dados = conexao.recv(2048).decode()

    # se vazio, significa que o cliente finalizou a conexão
    if dados == '':
        break

    print(f'Dados recebidos: {dados}')

    # divide os dados recebidos em partes
    partes = dados.split(';')

    if partes[0] == '1':
        incluirProd(partes[1], partes[2], partes[3], partes[4], partes[5])
    elif partes[0] == '2':
        pesquisarProd(partes[1])
    elif partes[0] == '3':
        listar(partes[1])
    elif partes[0] == '4':
        excluiProd(partes[1])

# fecha a conexão
conexao.close()


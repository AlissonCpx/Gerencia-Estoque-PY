def titulo(texto):
    print()
    print(texto)
    print('-' * 40)


def incluir():
    titulo('Controle de Estoque')

    # lê os dados de entrada
    prod = input('Nome do pruto a cadastrar: ')
    tipo = input('Tipo do produto: ')
    quant = input('Quantidade: ')
    dataf = input('Data de fabricação (Ex: 88/88/88): ')
    datav = input('Data de vencimento (Ex: 88/88/88): ')
    mensagem = '1;' + prod + ';' + tipo + ';' + quant + ';' + dataf + ';' + datav + ';'

    # envia mensagem ao servidor
    cliente.send(mensagem.encode())

    # recebe o retorno
    retorno = cliente.recv(2048).decode()

    if retorno == '1':
        print('Ok! Produto cadastro!')
    else:
        print('Erro... Produto não cadastrado!')


def pesquisar():
    titulo('Pesquisa de produto no estoque')

    prod = input('Nome do produto a pesquisar? ')

    mensagem = '2;' + prod

    # envia mensagem ao servidor
    cliente.send(mensagem.encode())

    # recebe o retorno
    retorno = cliente.recv(4096).decode()

    if retorno == '0':
        print('Erro... Produto não encontrado')
    else:
        linhas = retorno.split('#')

        print(
            'Nº Produto......................: Tipo.....: Data de Fabricação......: Data de Vencimento.....: Quantidade:')

        num = 0
        for linha in linhas:
            num += 1
            partes = linha.split(';')

            produto = partes[0]
            tipo = partes[1]
            quantidade = int(partes[2])
            datafab = partes[3]
            dataven = partes[4]

            if (quantidade < 100):

                print(f'{num:2d} {produto:30s} {tipo:10s} {datafab:25s} {dataven:25s} {quantidade}')
                print(("=")*43 + "POUCO PRODUTO EM ESTOQUE" + ("=")*40)
            else:
                print(f'{num:2d} {produto:30s} {tipo:10s} {datafab:25s} {dataven:25s} {quantidade}')


def listagemProd():
    titulo('Listagem de Produtos')

    mensagem = '3'

    print('Nº Produto......................: Tipo.....: Data de Fabricação......: Data de Vencimento.....: Quantidade:')
    arq = open('estoque.txt', 'r')
    linhas = arq.readlines()
    arq.close()

    num = 0
    for linha in linhas:
        num += 1
        partes = linha.split(';')
        produto = partes[0]
        tipo = partes[1]
        quantidade = int(partes[2])
        datafab = partes[3]
        dataven = partes[4]
        if (quantidade < 100):

            print(f'{num:2d} {produto:30s} {tipo:10s} {datafab:25s} {dataven:25s} {quantidade} X')

        else:
            print(f'{num:2d} {produto:30s} {tipo:10s} {datafab:25s} {dataven:25s} {quantidade}')

       # print(f'{num:2d} {produto:30s} {tipo:10s} {datafab:25s} {dataven:25s} {quantidade}')


def excluir():
    titulo('Excluir Produto')

    prod = input('Nome do Produto: ')

    mensagem = '4;' + prod

    # envia mensagem
    cliente.send(mensagem.encode())

    # recebe retorno e decodifica
    retorno = cliente.recv(2048).decode()

    if retorno == '0':
        print('Erro... Não excluído')
    else:
        print(f'O produto {prod} foi excluído com sucesso!')


# --------------------------------------
# Programa Principal: Cliente
# --------------------------------------
import socket

host = "127.0.0.1"
porta = 1060

# define protocolo
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conecta ao servidor
cliente.connect((host, porta))

while True:
    titulo('Controle de Estoque')

    print('1. Incluir Produto.')
    print('2. Pesquisar Produto.')
    print('3. Listar todos os produtos.')
    print('4. Excluir Produto.')
    print('5. Finalizar.')
    opcao = int(input('Opção: '))
    if opcao == 1:
        incluir()
    elif opcao == 2:
        pesquisar()
    elif opcao == 3:
        listagemProd()
    elif opcao == 4:
        excluir()
    else:
        break

# fecha a conexão
cliente.close()

import glob, os, shutil, sys
from tss.TimeSheetSigner import TimeSheetSigner, FileSigner


def ajuda():
    print('= HELP =')
    print('Command: python3 main.py [option]')
    print('Options:')
    print('\t arquivo=')
    print('\t x=')
    print('\t y=')


def definir_ano_mes(arquivo):
    ano = None
    mes = None
    ano_mes = None
    if arquivo is not None:
        try:
            ano = int(arquivo[13:17])
            mes = int(arquivo[18:20])
            ano_mes = '{0}{1}{2}'.format(ano, '-', mes)
        except:
            print('erro trying get ano and mes')
    return ano, mes, ano_mes


def assinar_arquivos(origem, destino, assinatura, tmp):
    for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
        ano, mes, ano_mes = definir_ano_mes(arquivo)
        tss = TimeSheetSigner(assinatura, tmp)
        tss.assinar(arquivo, destino, ano, mes)


def assinar_arquivo(origem, destino, assinatura, x, y, pagina, tmp):
    tss = FileSigner(assinatura, tmp)
    tss.assinar(origem, destino, x, y, pagina)


def definir_entradas():
    x, y, nome_arquivo, pagina = None, None, None, 0
    for i in range(1, len(sys.argv)):
        comando = sys.argv[i]
        if comando.find('=') >= 1:
            comandoChave, comandoValor = comando.split('=')
        else:
            comandoChave = sys.argv[i]

        if comandoChave == 'arquivo':
            nome_arquivo = comandoValor
        elif comandoChave == 'x':
            x = int(comandoValor)
        elif comandoChave == 'y':
            y = int(comandoValor)
        elif comandoChave == 'pagina':
            pagina = int(comandoValor)
        else:
            ajuda()

    return x, y, nome_arquivo, pagina


def encerrar(tmp):
    if os.path.exists(tmp):
        try:
            shutil.rmtree(tmp)
        except PermissionError:
            pass


origem = 'files/origem/'
destino = 'files/destino/'
assinatura = 'files/assinatura-paudadaniele.jpeg'
tmp = 'files/tmp/'
if __name__ == '__main__':
    print()
    print('inicio')

    x, y, nome_arquivo, pagina = definir_entradas()
    if nome_arquivo is not None:
        origem = nome_arquivo
        assinar_arquivo(origem, destino, assinatura, x, y, pagina, tmp)
    else:
        assinar_arquivos(origem, destino, assinatura, tmp)

    encerrar(tmp)
    print('fim')

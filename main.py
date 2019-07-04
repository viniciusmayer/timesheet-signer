import glob, os, shutil, sys
from tss.TimeSheetSigner import TimeSheetSigner


def ajuda():
    print('= HELP =')
    print('Command: python3 main.py [option]')
    print('Options:')
    print('\t assinar')
    print('\t mes=yyyymm')
    print('\t separador=[-, _]. Default: -')
    print('\t ajuda')
    print('Example: python3 main.py assinar')
    print('Example: python3 main.py assinar mes=201811')
    print('Example: python3 main.py assinar mes=201811 separador=-')


def definir_ano_mes(mes, separador):
    ano = None
    _mes = None
    ano_mes = None
    if mes is not None:
        ano = mes[0:4]
        _mes = mes[4:6]
        ano_mes = '{0}{1}{2}'.format(ano, separador, _mes)
        print('ano_mes: {0}'.format(ano_mes))
    return ano, _mes, ano_mes


def realizar_assinatura(origem, destino, assinatura, mes, separador, tmp):
    ano, _mes, ano_mes = definir_ano_mes(mes, separador)
    tss = TimeSheetSigner(assinatura, ano, _mes, tmp)
    for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
        if (ano_mes is None) or (ano_mes in arquivo):
            tss.assinar(arquivo, destino)


def definir_entradas():
    assinar = False
    mes = None
    separador = '-'
    comandoChave, comandoValor = None, None
    for i in range(1, len(sys.argv)):
        if sys.argv[i].find('=') > 1:
            comandoChave, comandoValor = sys.argv[i].split('=')
        else:
            comandoChave = sys.argv[i]

        if comandoChave == 'assinar':
            assinar = True
        elif comandoChave == 'mes':
            mes = comandoValor
        elif comandoChave == 'separador':
            separador = comandoValor
    return assinar, mes, separador


def configurar(tmp):
    if not os.path.exists(tmp):
        os.makedirs(tmp)


def encerrar(tmp):
    if os.path.exists(tmp):
        try:
            shutil.rmtree(tmp)
        except PermissionError:
            pass


origem = 'files/pdf/'
destino = 'files/pdf/'
assinatura = 'files/assinatura.jpg'
tmp = 'files/tmp/'
if __name__ == '__main__':
    print()
    print('inicio')
    configurar(tmp)

    j = len(sys.argv)
    if j > 1:
        assinar, mes, separador = definir_entradas()
        if assinar:
            realizar_assinatura(origem, destino, assinatura, mes, separador, tmp)
        else:
            ajuda()
    else:
        ajuda()

    encerrar(tmp)
    print('fim')

import glob, os, shutil, sys
from tss.TimeSheetSigner import TimeSheetSigner


def ajuda():
    print('= HELP =')
    print('Command: python3 main.py [option]')
    print('Options:')
    print('\t assinar')
    print('\t ajuda')
    print('Example: python3 main.py assinar')


def realizar_assinatura(origem, destino, assinatura, tmp):
    tss = TimeSheetSigner(assinatura, tmp)
    for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
        tss.assinar(arquivo, destino)


origem = 'files/pdf/unassigned/'
destino = 'files/pdf/signed/'
assinatura = 'files/assinatura.jpg'
tmp = 'files/tmp/'
if __name__ == '__main__':

    if not os.path.exists(tmp):
        os.makedirs(tmp)

    j = len(sys.argv)
    if j > 1:
        print()
        print('inicio')
        assinar = False
        comandoChave, comandoValor = None, None
        for i in range(1, len(sys.argv)):
            if sys.argv[i].find('=') > 1:
                comandoChave, comandoValor = sys.argv[i].split('=')
            else:
                comandoChave = sys.argv[i]

            if comandoChave == 'assinar':
                assinar = True
            else:
                ajuda()

        if assinar:
            realizar_assinatura(origem, destino, assinatura, tmp)
        else:
            ajuda()
    else:
        ajuda()

    if os.path.exists(tmp):
        try:
            shutil.rmtree(tmp)
        except PermissionError:
            pass
    print('fim')

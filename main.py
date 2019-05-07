import glob
import os
import shutil
import sys

from PyPDF2 import PdfFileReader

from tss.TimeSheetSigner import TimeSheetSigner


def ajuda():
    print('= HELP =')
    print('Command: python3 Main.py [option]')
    print('Options:')
    print('\t importarlattes[=bancodedados - para escrever a saida em banco de dados. Valor padrao: arquivo]')
    print('\t importarpdfs')
    print('\t gerarevento[=<nome do evento>] - para especificar o event')
    print('\t gerarpdf')
    print('\t fazerbackup')
    print('\t ajuda')
    print('Example: python3 Main.py importarlattes importarpfds gerarevento gerarpdf')
    print('Example: python3 Main.py importarpfds gerarpdf')


def realizar_assinar(origem, destino, assinatura, tmp):
    for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
        nome_arquivo_origem = arquivo[arquivo.rfind('\\') + 1:len(arquivo)]
        pdf_file = PdfFileReader(open(arquivo, 'rb'))
        if not pdf_file.isEncrypted:
            tss = TimeSheetSigner(tmp)
            tss.assinar(nome_arquivo_origem, arquivo, destino, assinatura, tmp)
            print('arquivo lido: {0}'.format(nome_arquivo_origem))
        else:
            print('arquivo ignorado: {0}'.format(nome_arquivo_origem))


origem = 'files/pdf/unassigned/'
destino = 'files/pdf/signed/'
assinatura = 'files/assinatura.gif'
tmp = 'files/tmp/'
if __name__ == '__main__':
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
            realizar_assinar(origem, destino, assinatura, tmp)
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

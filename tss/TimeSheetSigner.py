import os
import uuid

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from calendar import monthrange


class Signer(object):

    def __init__(self, assinatura, tmp):
        self.assinatura = assinatura
        self.tmp = tmp
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp)

    def gerar_pagina_assinada(self, largura, altura, a, b):
        arquivo = '{0}{1}'.format(self.tmp, str(uuid.uuid4()))
        c = canvas.Canvas(arquivo, pagesize=(largura, altura))
        x, y = self.definir_x_y(largura, a, b)
        y += 10
        c.drawImage(self.assinatura, x, y, width=(4.5 * cm), height=(1.5 * cm))
        c.showPage()
        c.save()
        return PdfFileReader(open(arquivo, 'rb')).getPage(0)

    def assinar(self, arquivo, destino, a, b, p):
        nome_arquivo = arquivo[arquivo.rfind('\\') + 1:len(arquivo)]
        _arquivo = PdfFileReader(open(arquivo, 'rb'))
        if _arquivo.isEncrypted:
            print('arquivo ignorado: {0}'.format(nome_arquivo))
        else:
            print('arquivo encontrado: {0}'.format(nome_arquivo))
            paginas = []
            for _p in range(_arquivo.getNumPages()):
                pagina = _arquivo.getPage(_p)
                if _p == p:
                    largura = float(pagina.mediaBox.getWidth())
                    altura = float(pagina.mediaBox.getHeight())
                    pagina_assinada = self.gerar_pagina_assinada(largura, altura, a, b)
                    pagina.mergePage(pagina_assinada)
                paginas.append(pagina)
            _destino = PdfFileWriter()
            for pagina in paginas:
                _destino.addPage(pagina)
            _nome_arquivo = '{0}{1}-{2}'.format(destino, 'assinado', nome_arquivo.replace(' ', '_'))
            with open(_nome_arquivo, 'wb') as f:
                _destino.write(f)
                print('arquivo gerado: {0}'.format(_nome_arquivo))


class FileSigner(Signer):

    def definir_x_y(self, largura, x, y):
        _x = largura - (11.5 * cm)
        _y = (6.75 * cm)
        if x is not None:
            _x = largura - (x * cm)
        if y is not None:
            _y = (y * cm)
        return _x, _y


class TimeSheetSigner(Signer):

    def definir_x_y(self, largura, ano, mes):
        first_weekday, dias = None, None
        if ano is not None and mes is not None:
            first_weekday, dias = monthrange(ano, mes)
        x = largura - (11.5 * cm)
        y = (6.75 * cm)
        if dias == 28:
            y = (7.75 * cm)
        elif dias == 29:
            y = (7.5 * cm)
        elif dias == 30:
            y = (7 * cm)
        return x, y

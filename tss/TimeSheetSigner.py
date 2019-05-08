import os
import uuid

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class TimeSheetSigner(object):

    def __init__(self, assinatura, tmp):
        self.assinatura = assinatura
        self.tmp = tmp
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp)

    def gerar_pagina_assinada(self, largura, altura):
        arquivo = '{0}{1}'.format(self.tmp, str(uuid.uuid4()))
        c = canvas.Canvas(arquivo, pagesize=(largura, altura))
        c.drawImage(self.assinatura, largura - (11.5 * cm), (7.25 * cm), width=(1.5 * cm), height=(1.5 * cm))
        c.showPage()
        c.save()
        return PdfFileReader(open(arquivo, 'rb')).getPage(0)

    def assinar(self, arquivo, destino):
        nome_arquivo = arquivo[arquivo.rfind('\\') + 1:len(arquivo)]
        _arquivo = PdfFileReader(open(arquivo, 'rb'))
        if _arquivo.isEncrypted:
            print('arquivo ignorado: {0}'.format(nome_arquivo))
        else:
            print('arquivo encontrado: {0}'.format(nome_arquivo))
            pagina = _arquivo.getPage(0)
            largura = float(pagina.mediaBox.getWidth())
            altura = float(pagina.mediaBox.getHeight())
            pagina_assinada = self.gerar_pagina_assinada(largura, altura)
            pagina.mergePage(pagina_assinada)
            _destino = PdfFileWriter()
            _destino.addPage(pagina)
            _nome_arquivo = nome_arquivo.replace(' ', '_')
            with open('{0}{1}'.format(destino, _nome_arquivo), 'wb') as f:
                _destino.write(f)
                print('arquivo gerado: {0}'.format(_nome_arquivo))

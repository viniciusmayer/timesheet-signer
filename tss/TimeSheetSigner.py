import os
import uuid

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import Color
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class TimeSheetSigner(object):

    def __init__(self, tmp):
        if not os.path.exists(tmp):
            os.makedirs(tmp)

    '''
        # fundo da assinatura
        #color = Color(255, 255, 255, alpha=0.5)
        #c.setFillColor(color)
        #c.setStrokeColor(color)
        #c.rect(largura - (2 * cm), (0.5 * cm), (1.5 * cm), (1.5 * cm), fill=1)
        # assinatura
        c.setFillColor(Color(0, 0, 0, alpha=1))
        c.drawImage(assinatura, largura - (2 * cm), (0.5 * cm), width=(1.5 * cm), height=(1.5 * cm))
    '''

    def aplicar_assinatura(self, largura, altura, assinatura, tmp):
        arquivo = '{0}{1}'.format(tmp, str(uuid.uuid4()))
        c = canvas.Canvas(arquivo, pagesize=(largura, altura))

        # assinatura
        c.setFillColor(Color(0, 0, 0, alpha=1))
        c.drawImage(assinatura, largura - (11.5 * cm), (7.25 * cm), width=(1.5 * cm), height=(1.5 * cm))

        c.showPage()
        c.save()
        pagina_assinada = PdfFileReader(open(arquivo, 'rb'))
        return pagina_assinada.getPage(0)

    def assinar(self, nome_arquivo, arquivo, destino, assinatura, tmp):
        pagina = PdfFileReader(open(arquivo, 'rb')).getPage(0)
        largura = float(pagina.mediaBox.getWidth())
        altura = float(pagina.mediaBox.getHeight())
        pagina_assinada = self.aplicar_assinatura(largura, altura, assinatura, tmp)
        pagina.mergePage(pagina_assinada)
        arquivo_destino = PdfFileWriter()
        arquivo_destino.addPage(pagina)
        with open('{0}{1}'.format(destino, nome_arquivo), 'wb') as f:
            arquivo_destino.write(f)
            print('arquivo gerado: {0}'.format(nome_arquivo))

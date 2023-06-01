from random import randint
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from textwrap import wrap
import subprocess

nCols = 3      # number of images per row
nRows = 2      # number of images per column

lineSpace = 15 # space between transcript lines
lineWidth = 40 # maximum width of a line

def convertOraToPng(iPage):
    '''Convert .ora files (drawn with MyPaint) to .png files'''

    for iy in range(nRows):
        for ix in range(nCols):
            fileName = f'{iPage}-{iy*nCols+ix+1}'
            tempFile = 'mergedimage.png'
            subprocess.run(['unzip', '-q', f'ora/{fileName}.ora', tempFile])
            subprocess.run(['touch', tempFile])
            subprocess.run(['mv', tempFile, f'png/{fileName}.png'])
            subprocess.run(['convert', '-resize', '50%', f'png/{fileName}.png', f'png/{fileName}.png'])

def generatePage(iPage):
    '''Assemble .png files with transcript to PDF page''' 

    canvas = Canvas(f"figure_{iPage}.pdf")
    canvas.setPageSize(landscape(A4))
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)

    with open(f"transcript/page_{iPage}.txt", "r") as f:    
        
        for iy in range(nRows):    
            for ix in range(nCols):
                pngName = f'png/{iPage}-{iy*nCols+ix+1}.png'
                img = ImageReader(pngName)
                x = 70+ix*250
                y = 370-280*iy
                canvas.drawImage(img, x, y, width=200, height=200, mask='auto')

                text = f.readline()
                while text.strip() == '':
                    text = f.readline()


                textWrapped = wrap(text, width=lineWidth)
                i = 0
                for t in textWrapped:
                    canvas.drawString(x, y-10-lineSpace*i, t)
                    i += 1
    canvas.save()

if __name__ == '__main__':

    for iPage in range(3):
        print(f'---- Page {iPage} ----')
        print('Converting .ora files to .png files...')
        convertOraToPng(iPage+1)
        print('Generating PDF file')
        generatePage(iPage+1)

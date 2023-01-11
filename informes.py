import os, var
from PyQt6 import QtSql
from reportlab.pdfgen import canvas
from datetime import datetime

class Informes:
    def listClientes(self):
        try:
            var.report = canvas.Canvas('informes/listadoClientes.pdf')
            titulo = 'LISTADO CLIENTES'
            var.report.drawString(100, 750, '')
            Informes.pie_Informe(titulo)
            Informes.top_Informe(titulo)
            items = ['DNI', 'Nombre', 'Dirección', 'Municipio', 'Provincia']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(60, 675, str(items[0]))
            var.report.drawString(120, 675, str(items[1]))
            var.report.drawString(270, 675, str(items[2]))
            var.report.drawString(370, 675, str(items[3]))
            var.report.drawString(470, 675, str(items[4]))
            var.report.line(50, 670, 525, 670)
            query = QtSql.QSqlQuery()
            query.prepare('select dni, nombre, direccion, municipio, provincia '
                          'from clientes order by nombre')
            var.report.setFont('Helvetica', size=8)
            if query.exec():
                i = 55
                j = 660
                while query.next():
                    if j <= 80:
                        var.report.drawString(460, 90, 'Página siguiente...')
                        var.report.showPage()
                        Informes.top_Informe(titulo)
                        Informes.pie_Informe(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(60, 675, str(items[0]))
                        var.report.drawString(120, 675, str(items[1]))
                        var.report.drawString(270, 675, str(items[2]))
                        var.report.drawString(370, 675, str(items[3]))
                        var.report.drawString(470, 675, str(items[4]))
                        var.report.line(50, 670, 525, 670)
                        i = 55
                        j = 660
                    var.report.setFont('Helvetica', size=8)
                    var.report.drawString(i, j, Informes.cifrar(str(query.value(0))))
                    var.report.drawString(i+65, j, str(query.value(1)))
                    var.report.drawString(i+210, j, str(query.value(2)))
                    var.report.drawString(i+305, j, str(query.value(3)))
                    var.report.drawString(i+410, j, str(query.value(4)))
                    j = j - 20

            var.report.save()
            rootPath = '.\\informes'

            '''
            for file in os.listdir((rootPath)):
                if file.endswith(('Clientes.pdf')):
                    os.startfile('%s\%s' % (rootPath, file))
            '''

        except Exception as e:
            print('Error informes estado clientes:', e)


    def listAutos(self):
        try:
            var.report = canvas.Canvas('informes/listadoAutos.pdf')
            titulo = 'LISTADO VEHÍCULOS'
            var.report.drawString(100, 750, '')
            Informes.pie_Informe(titulo)
            Informes.top_Informe(titulo)

            items = ['Matricula', 'DniCli', 'Marca', 'Modelo', 'Motor']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(60, 675, str(items[0]))
            var.report.drawString(120, 675, str(items[1]))
            var.report.drawString(270, 675, str(items[2]))
            var.report.drawString(370, 675, str(items[3]))
            var.report.drawString(470, 675, str(items[4]))
            var.report.line(50, 670, 525, 670)
            query = QtSql.QSqlQuery()
            query.prepare('select matricula, dnicli, marca, modelo, motor '
                          'from coches order by matricula')
            var.report.setFont('Helvetica', size=8)
            if query.exec():
                i = 55
                j = 660
                while query.next():
                    if j <= 80:
                        var.report.drawString(460, 90, 'Página siguiente...')
                        var.report.showPage()
                        Informes.top_Informe(titulo)
                        Informes.pie_Informe(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(60, 675, str(items[0]))
                        var.report.drawString(120, 675, str(items[1]))
                        var.report.drawString(270, 675, str(items[2]))
                        var.report.drawString(370, 675, str(items[3]))
                        var.report.drawString(470, 675, str(items[4]))
                        var.report.line(50, 670, 525, 670)
                        i = 55
                        j = 660
                    var.report.setFont('Helvetica', size=8)
                    var.report.drawString(i, j, str(query.value(0)))
                    var.report.drawString(i + 65, j, Informes.cifrar(str(query.value(1))))
                    var.report.drawString(i + 210, j, str(query.value(2)))
                    var.report.drawString(i + 305, j, str(query.value(3)))
                    var.report.drawString(i + 410, j, str(query.value(4)))
                    j = j - 20

            var.report.save()
            rootPath = '.\\informes'
            for file in os.listdir((rootPath)):
                if file.endswith(('Autos.pdf')):
                    os.startfile('%s\%s' % (rootPath, file))

        except Exception as e:
            print('Error informes estado vehiculos:', e)

    #Pie de página
    def pie_Informe(titulo):
        try:
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y   %H:%M:%S') #Sirve para ver si un informe está actualizado
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))

        except Exception as e:
            print('Error pie informe clientes:', e)


    def top_Informe(titulo):
        try:
            logo = '.\img\\logo.png'
            var.report.line(50, 800, 525, 800)
            var.report.setFont('Helvetica-Bold', size=14)
            var.report.drawString(55, 785, 'Taller Mecánica Teis')
            var.report.drawString(240, 705, titulo)
            var.report.line(50, 700, 525, 700)
            var.report.drawImage(logo, 440, 730, width=80, height=45)
            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 770, 'CIF: A12345678')
            var.report.drawString(55, 755, 'Avda Galicia - 101')
            var.report.drawString(55, 745, 'Vigo - 36216 - España')
            var.report.drawString(55, 730, 'e-mail: mitaller@gmail.com')
            var.report.drawString(55, 720, 'Tlfno: 986 132 456')

        except Exception as e:
            print('Error cabecera informe clientes:', e)


    def cifrar(dni):
        asteriscos = [0, 1, 2, 3, 4, 8]
        for i in asteriscos:
            dni = dni[:i] + '*' + dni[i+1:]
        return dni
import sys, var, shutil, os, xlwt
import zipfile

import xlrd as xlrd
from PyQt6 import QtWidgets, QtSql
from datetime import date, datetime

import clientes
import conexion
from ventMain import *

import var


class Eventos:
    '''
    Listado de funciones de la clase Eventos
    '''
    def salir(self):
        '''
        Módulo para salir de la interfaz de usuario

        :param: self

        :return: None
        '''
        try:
            var.avisosalir.show()
            if var.avisosalir.exec():
                sys.exit()
            else :
                var.avisosalir.hide()
        except Exception as error:
            print("Error en función salir:", str(error))

    def letrasCapital(self = None):
        '''
        Módulo para poner un texto en mayúsculas

        :param: None

        :return: None
        '''
        try:
            var.ui.txtNombreCli.setText(var.ui.txtNombreCli.text().title())
            var.ui.txtDir.setText(var.ui.txtDir.text().title())
            var.ui.txtMatricula.setText(var.ui.txtMatricula.text().upper())
            var.ui.txtMarca.setText(var.ui.txtMarca.text().upper())
            var.ui.txtModelo.setText(var.ui.txtModelo.text().title())
        except Exception as error:
            print('Error al capitalizar letras:', error)

    def abrirCalendar(self):
        '''
        Módulo para abrir el calendario y seleccionar una fecha

        :param: self

        :return: None
        '''
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error al abrir el calendario:', error)


    def resizeTablacarcli(self):
        '''
        Módulo para reajustar el tamaño de la tabla de clientes

        :param: self

        :return: None
        '''
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0 or i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        except Exception as error:
            print('Error al reajustar tabla clientes:', error)


    def resizeTablaServicios(self):
        '''
        Módulo para reajustar el tamaño de la tabla de servicios

        :param: self

        :return: None
        '''
        try:
            header = var.ui.tabServizos.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0 or i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        except Exception as error:
            print('Error al reajustar tabla Servicios:', error)


    def creaBackup(self):
        '''
        Módulo para crear una copia de seguridad de los datos la base de datos

        :param: self

        :return: None
        '''
        try:
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            copia = (str(fecha) + '_backup.zip')
            #option = QtWidgets.QFileDialog.Option()
            directorio, filename = var.dlgAbrir.getSaveFileName(None, 'Guardar Copia', copia, '.zip')
            if var.dlgAbrir.accept and filename != '':
                fichzip = zipfile.ZipFile(copia, 'w')
                fichzip.write(var.bbdd, os.path.basename(var.bbdd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(copia), str(directorio))
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Copia de seguridad creada')
                msg.exec()

        except Exception as error:
            print('Error al crear el backup:', error)

    def restauraBackup(self = None):
        '''
        Módulo para restaurar una copia de seguridad en la base de datos

        :param: None

        :return: None
        '''
        try:
            filename = var.dlgAbrir.getOpenFileName(None, 'Restaurar Copia Seguridad',
                                                    '', '*.zip;;All Files')
            if var.dlgAbrir.accept and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
            conexion.Conexion.conexion()
            conexion.Conexion.mostrarTabcarcli()
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Copia de seguridad Restaurada')
            msg.exec()

        except Exception as ex:
            print('Error al restaurar backup:', ex)


    def mostrarExportar(self):
        '''
        Módulo para mostrar el dialogo paa exportar

        :param: self

        :return: None
        '''
        var.dlgExportar.show()

    def exportarDatos(self):
        '''
        Módulo para exportar los datos de un cliente

        :param: self

        :return: None
        '''
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            file = (str(fecha) + '_Clientes.xls')
            directorio, filename = var.dlgAbrir.getSaveFileName(None, 'Guardar Datos', file, '.xls')
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet('Clientes')
            sheet1.write(0, 0, 'DNI')
            sheet1.write(0, 1, 'Nombre')
            sheet1.write(0, 2, 'Fecha Alta')
            sheet1.write(0, 3, 'Direccion')
            sheet1.write(0, 4, 'Provincia')
            sheet1.write(0, 5, 'Municipio')
            sheet1.write(0, 6, 'Forma de pago')
            sheet1.write(0, 7, 'Fecha Baja')
            fila = 1
            query = QtSql.QSqlQuery()
            query.prepare('select * from clientes order by dni')
            if query.exec():
                while query.next():
                    sheet1.write(fila, 0, str(query.value(0)))
                    sheet1.write(fila, 1, str(query.value(1)))
                    sheet1.write(fila, 2, str(query.value(2)))
                    sheet1.write(fila, 3, str(query.value(3)))
                    sheet1.write(fila, 4, str(query.value(4)))
                    sheet1.write(fila, 5, str(query.value(5)))
                    sheet1.write(fila, 6, str(query.value(6)))
                    sheet1.write(fila, 7, str(query.value(7)))
                    fila += 1


            if (wb.save(directorio)):
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Exportación de Datos Realizada')
                msg.exec()

            var.dlgExportar.hide()


        except Exception as error:
            print('Error al exportar datos:', error)


    def exportarServicio(self):
        '''
        Módulo para exportar un servicio

        :param: self

        :return: None
        '''
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            file = (str(fecha) + '_Servicio.xls')
            directorio, filename = var.dlgAbrir.getSaveFileName(None, 'Guardar Datos', file, '.xls')
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet('Servicios')
            sheet1.write(0, 0, 'Codigo')
            sheet1.write(0, 1, 'Concepto')
            sheet1.write(0, 2, 'Precio')
            fila = 1
            query = QtSql.QSqlQuery()
            query.prepare('select * from servicios order by codigo')
            if query.exec():
                while query.next():
                    sheet1.write(fila, 0, str(query.value(0)))
                    sheet1.write(fila, 1, str(query.value(1)))
                    sheet1.write(fila, 2, str(query.value(2)))
                    fila += 1

            if (wb.save(directorio)):
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Exportación de Datos Realizada')
                msg.exec()

            var.dlgExportar.hide()


        except Exception as error:
            print('Error al exportar datos:', error)


    def importarDatos(self):
        '''
        Módulo para importar los datos de un cliente

        :param: self

        :return: None
        '''
        try:
            filename = var.dlgAbrir.getOpenFileName(None, 'Importar datos', '', '*.xls;;All Files(*)')
            if var.dlgAbrir.accept and filename != '':
                file = filename[0]
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                columnas = datos.ncols
                new = []
                for i in range(filas):
                    if i == 0:
                        pass
                    else:
                        new = []
                        for j in range(columnas):
                            new.append(str(datos.cell_value(i,j)))
                            if clientes.Clientes.validarDNI(str(new[1])):
                                conexion.Conexion.altaExcelCoche(new)
                conexion.Conexion.mostrarTabcarcli(self)
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Importación de Datos Realizada')
                msg.exec()

        except Exception as error:
            print('Error al importar datos:', error)

    def resizeTablaventas(self):
        '''
        Módulo para reajustar el tamaño de la tabla de ventas

        :param: self

        :return: None
        '''
        try:
            header = var.ui.tabVentas.horizontalHeader()

            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)


        except Exception as error:
            print('Error:', error)
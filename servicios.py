from PyQt6 import QtSql, QtWidgets, QtCore

import conexion
import var


class Servicios():
    '''
    Listado de funciones de la clase Servicios
    '''

    def limpiaServicio(self=None):
        '''
        Módulo para limpiar los datos de las cajas de texto relacionados con los servicios

        :param: None

        :return: None
        '''
        try:
            servicio = [var.ui.txtCodigo, var.ui.txtConcepto, var.ui.txtPrecio]
            for i in servicio:
                i.setText('')

        except Exception as error:
            print('Error al limpiar el servicio:', error)

    def guardaServicio(self):
        '''
        Módulo para guardar un nuevo servicio

        :param: self

        :return: None
        '''
        try:
            if var.ui.txtConcepto.text() == '' or var.ui.txtPrecio.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede guardar un registro con parámetros vacíos')
                msg.exec()
            else:
                newservicio = []

                servicio = [var.ui.txtConcepto, var.ui.txtPrecio]
                for i in servicio:
                    newservicio.append(i.text())

                conexion.Conexion.altaServicio(newservicio)
                conexion.Conexion.mostrarTabServicios(self)
                print(newservicio)

        except Exception as error:
            print('Error al guardar el servicio:', error)


    def cargaServicio(self=None):
        '''
        Módulo para cargar los datos de un servicio selecicoando en las cajas de texto

        :param: None

        :return: None
        '''
        try:
            Servicios.limpiaServicio()
            fila = var.ui.tabServizos.selectedItems()
            row = [dato.text() for dato in fila]  # Recoge todo lo que hay en cada fila de la tabla
            datos = [var.ui.txtCodigo, var.ui.txtConcepto, var.ui.txtPrecio]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            var.ui.txtCodigo.setText(row[0])
            var.ui.txtConcepto.setText(row[1])
            var.ui.txtPrecio.setText(row[2])

        except Exception as e:
            print('Error carga servicio:', e)


    def modifServ(self=None):
        '''
        Módulo para modificar un servicio

        :param: None

        :return: None
        '''
        try:
            if var.ui.txtConcepto.text() == '' or var.ui.txtPrecio.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede modificar un registro con parámetros vacíos')
                msg.exec()
            else:
                modserv = []

                servicio = [var.ui.txtConcepto, var.ui.txtPrecio, var.ui.txtCodigo]
                for i in servicio:
                    modserv.append(i.text())

                conexion.Conexion.modificaServ(modserv)

                conexion.Conexion.mostrarTabServicios(self)

        except Exception as error:
            print('Error al modificar servicio: ', error)


    def borraServ(self):
        '''
        Módulo para borrar un servicio

        :param: self

        :return: None
        '''
        try:
            if var.ui.txtConcepto.text() == '' or var.ui.txtPrecio.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede eliminar un registro con parámetros vacíos')
                msg.exec()
            else:
                concepto = var.ui.txtConcepto.text()
                var.codigoServicio = str(conexion.Conexion.buscaServicio(concepto))
                codigo = var.codigoServicio
                conexion.Conexion.borraServ(codigo)
                conexion.Conexion.mostrarTabServicios(self)

        except Exception as error:
            print('Error al borrar cliente:', error)
from PyQt6 import QtWidgets, QtCore

import conexion
import var
from clientes import Clientes


class Facturas():
    '''
    Lisatdo de las funciones de la clase Facturas
    '''

    def limpiaFact(self=None):
        '''
        Módulo para limpiar las cajas de texto referenciadas a las facturas

        :param: None

        :return: None
        '''
        try:
            factura = [var.ui.txtNumFactura, var.ui.txtDNIFactura, var.ui.txtMatriculaFactura,
                       var.ui.txtFechaFactura, var.ui.txtBuscar]
            for i in factura:
                i.setText('')

        except Exception as error:
            print('Error al limpiar imprimirFactura:', error)

    def cargaFactura(self=None):
        '''
        Módulo para cargar los datos de la factura seleccionada en las cajas de texto

        :param: None

        :return: None
        '''
        try:
            Facturas.limpiaFact()
            fila = var.ui.tabFacturas.selectedItems()
            row = [dato.text() for dato in fila]  # Recoge todo lo que hay en cada fila de la tabla
            datos = [var.ui.txtNumFactura, var.ui.txtDNIFactura]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            var.ui.txtNumFactura.setText(row[0])
            var.ui.txtDNIFactura.setText(row[1])

            restoDatos = conexion.Conexion.restoDatosFactura(row[0])

            var.ui.txtMatriculaFactura.setText(restoDatos[0])
            var.ui.txtFechaFactura.setText(restoDatos[1])

            conexion.Conexion.cargarLineasVenta(row[0])

        except Exception as e:
            print('Error carga imprimirFactura:', e)


    def cargaLineaVenta(index):
        '''
        Módulo para cargar las lineas de venta de una factura

        :param: index: entero que almacenael valor de un índice

        :return: None
        '''
        try:
            var.cmbServicio = QtWidgets.QComboBox()
            var.cmbServicio.setFixedSize(140, 28)

            conexion.Conexion.cargaComboVenta(None)

            var.txtUnidades = QtWidgets.QLineEdit()
            var.txtUnidades.setFixedSize(140, 30)
            var.txtUnidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            var.txtUnidades.editingFinished.connect(Facturas.totalLineaVenta)

            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbServicio)
            var.ui.tabVentas.setCellWidget(index, 3, var.txtUnidades)

        except Exception as e:
            print("Error carga linea venta:", e)


    def cargaPrecioVenta(self):
        '''
        Módulo para cargar el precio de venta de un servicio en la tabla de ventas

        :param: self

        :return: None
        '''
        try:
            row = var.ui.tabVentas.currentRow()
            servicio = var.cmbServicio.currentText()
            datos = conexion.Conexion.obtenerPrecio(servicio)
            var.codigo_servicio = datos[0]
            var.precio = datos[1]
            precio = var.precio
            precio = str(precio).replace('.', ',')
            precio = precio + ' €'

            var.ui.tabVentas.setItem(row, 1, QtWidgets.QTableWidgetItem(str(precio)))
            var.ui.tabVentas.item(row, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print('Error al cargar precio de venta:', e)

    def totalLineaVenta(self=None):
        '''
        Módulo para calcular el total de una línea de venta

        :param: None

        :return: None
        '''
        try:
            if str(var.ui.txtNumFactura.text()) == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('Debe seleccionar una imprimirFactura')
                msg.exec()
            else:
                venta = []
                venta.append(int(var.ui.txtNumFactura.text()))
                venta.append(int(var.codigo_servicio))
                venta.append(round(float(var.precio), 2))

                row = var.ui.tabVentas.currentRow()
                cantidad = var.ui.tabVentas.cellWidget(row, 3).text()
                venta.append(round(float(cantidad), 2))

                totalFilaVenta = round(float(var.precio) * float(cantidad), 2)
                totalFilaVenta = str(f"{totalFilaVenta:.2f}")
                totalFilaVenta = totalFilaVenta.replace('.', ',') + ' €'
                var.ui.tabVentas.setItem(row, 4, QtWidgets.QTableWidgetItem(str(totalFilaVenta)))
                var.ui.tabVentas.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                conexion.Conexion.cargarVentas(venta)
                conexion.Conexion.cargarLineasVenta(venta[0])

        except Exception as e:
            print('Error al cargar total de la linea de venta:', e)

    def guardarFactura(self):
        '''
        Módulo para guardar una factura en la base de datos

        :param: self

        :return: None
        '''
        try:
            if var.ui.txtDNIFactura.text() == '' or var.ui.txtMatriculaFactura.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede guardar un registro con parámetros vacíos')
                msg.exec()
            else :
                newFac = []

                factura = [var.ui.txtDNIFactura, var.ui.txtMatriculaFactura]
                for i in factura:
                    newFac.append(i.text())

                conexion.Conexion.altaFactura(newFac)
                conexion.Conexion.mostrarTabFacturas(self)
                print(newFac)

        except Exception as error:
            print('Error al guardar la imprimirFactura:', error)

    def borraFactura(self):
        '''
        Módulo para borrar un registro de factura de la base de datos

        :param: self

        :return: None
        '''
        try:
            if var.ui.txtDNIFactura.text() == '' or var.ui.txtMatriculaFactura.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede eliminar un registro con parámetros vacíos')
                msg.exec()
            else:
                numeroFactura = var.ui.txtNumFactura.text()
                conexion.Conexion.borraFactura(numeroFactura)
                conexion.Conexion.mostrarTabFacturas(self)

        except Exception as error:
            print('Error al borrar cliente:', error)
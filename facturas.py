from PyQt6 import QtSql, QtWidgets, QtCore

import conexion
import var
from clientes import Clientes


class Facturas():


    def limpiaFact(self=None):
        try:
            factura = [var.ui.txtNumFactura, var.ui.txtDNIFactura, var.ui.txtMatriculaFactura,
                       var.ui.txtFechaFactura]
            for i in factura:
                i.setText('')

        except Exception as error:
            print('Error al limpiar factura:', error)


    def cargaFactura(self=None):
        try:
            Facturas.limpiaFact()
            fila = var.ui.tabFacturas.selectedItems()
            row = [dato.text() for dato in fila] # Recoge todo lo que hay en cada fila de la tabla
            datos = [var.ui.txtNumFactura, var.ui.txtDNIFactura]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            var.ui.txtNumFactura.setText(row[0])
            var.ui.txtDNIFactura.setText(row[1])

            matricula = conexion.Conexion.oneFac(row[0])
            var.ui.txtMatriculaFactura.setText(str(matricula))

        except Exception as e:
            print('Error carga factura:', e)


    def cargaLineaVenta(index):
        try:
            index = 0
            var.cmbServicio = QtWidgets.QComboBox()
            var.cmbServicio.setFixedSize(140, 30)
            var.txtUnidades = QtWidgets.QLineEdit()
            var.txtUnidades.setFixedSize(140, 30)
            var.txtUnidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 0, var.cmbServicio)
            var.ui.tabVentas.setCellWidget(index, 2, var.txtUnidades)

        except Exception as e:
            print("Error carga linea venta:", e)
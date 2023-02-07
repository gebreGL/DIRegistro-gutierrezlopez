from PyQt6 import QtWidgets, QtCore

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
            conexion.Conexion.cargarLineasVenta(row[0])
            var.ui.txtNumFactura.setText(row[0])
            var.ui.txtDNIFactura.setText(row[1])

            restoDatos = conexion.Conexion.restoDatosFactura(row[0])

            var.ui.txtMatriculaFactura.setText(restoDatos[0])
            var.ui.txtFechaFactura.setText(restoDatos[1])


        except Exception as e:
            print('Error carga factura:', e)

    def cargaLineaVenta(index):
        try:
            index = 0
            var.cmbServicio = QtWidgets.QComboBox()
            var.cmbServicio.setFixedSize(140, 28)
            var.txtUnidades = QtWidgets.QLineEdit()
            var.txtUnidades.setFixedSize(140, 30)
            var.txtUnidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 0, var.cmbServicio)
            var.ui.tabVentas.setCellWidget(index, 2, var.txtUnidades)

        except Exception as e:
            print("Error carga linea venta:", e)


    def cargaPrecioVenta(self):
        try:
            row = var.ui.tabVentas.currentRow()
            servicio = var.cmbServicio.currentText()
            precio = conexion.Conexion.obtenerPrecio(servicio)
            var.precio = precio
            precio = precio.replace('.', ',')
            precio = precio + ' €'
            var.ui.tabVentas.setItem(row, 1, QtWidgets.QTableWidgetItem(str(precio)))
            var.ui.tabVentas.item(row, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        except Exception as e:
            print("Error al cargar precio de venta:", e)


    def totalLineaVenta(self = None):
        try:
            if str(var.ui.txtNumFactura.text() == ''):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('Debe seleccionar una factura')
                msg.exec()
            else:
                row = var.ui.tabVentas.currentRow()
                cantidad = var.ui.tabVentas.cellWidget(row, 2).text()
                totalFilaVenta = round(float(var.precio) * float(cantidad), 2)
                totalFilaVenta = str(f"{totalFilaVenta:.2f}")
                totalFilaVenta = totalFilaVenta.replace('.', ',') + ' €'
                var.ui.tabVentas.setItem(row, 3, QtWidgets.QTableWidgetItem(str(totalFilaVenta)))
                var.ui.tabVentas.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        except Exception as e:
            print('Error al cargar total de la linea de venta:', e)



    def guardarFactura(self):
        try:
            newFac = []

            factura = [var.ui.txtDNIFactura, var.ui.txtMatriculaFactura]
            for i in factura:
                newFac.append(i.text())

            conexion.Conexion.altaFactura(newFac)
            conexion.Conexion.mostrarTabFacturas(self)
            print(newFac)

        except Exception as error:
            print('Error al guardar la factura:', error)
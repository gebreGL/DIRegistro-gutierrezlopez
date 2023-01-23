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
            datos = [var.ui.txtNumFactura, var.ui.txtDNIFactura, var.ui.txtFechaFactura]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            matricula = conexion.Conexion.oneFac(row[0])
            var.ui.txtMatriculaFactura.setText(str(matricula))

        except Exception as e:
            print('Error carga factura:', e)
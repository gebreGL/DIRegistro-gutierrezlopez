from PyQt6 import QtSql, QtWidgets, QtCore

import conexion
import var


class Servicios():

    def limpiaServicio(self=None):
        try:
            servicio = [var.ui.txtConcepto, var.ui.txtPrecio]
            for i in servicio:
                i.setText('')

        except Exception as error:
            print('Error al limpiar el servicio:', error)

    def guardaServicio(self):
        try:
            newservicio = []

            servicio = [var.ui.txtConcepto, var.ui.txtPrecio]
            for i in servicio:
                newservicio.append(i.text())

            conexion.Conexion.altaServicio(newservicio)
            print(newservicio)

        except Exception as error:
            print('Error al guardar el servicio:', error)


    def cargaServicio(self=None):
        try:
            Servicios.limpiaServicio()

            fila = var.ui.tabServizos.selectedItems()
            row = [dato.text() for dato in fila] # Recoge todo lo que hay en cada fila de la tabla
            datos = [var.ui.txtConcepto, var.ui.txtPrecio]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            var.ui.txtConcepto.setText(row[1])
            var.ui.txtPrecio.setText(row[2])

        except Exception as e:
            print('Error carga servicio:', e)


    def modifServ(self=None):
        try:
            modserv = []

            servicio = [var.ui.txtConcepto, var.ui.txtPrecio]
            for i in servicio:
                modserv.append(i.text())

            conexion.Conexion.modificaServ(modserv)

            conexion.Conexion.mostrarTabServicios(self)

        except Exception as error:
            print('Error al modificar cliente: ', error)


    def borraServ(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select concepto, precio-unidad from servicios where concepto = :concepto and precio-unidad = :precio')
            codigo = var.ui.txtCodigo
            conexion.Conexion.borraServ(codigo)
            conexion.Conexion.mostrarTabServicios(self)

        except Exception as error:
            print('Error al borrar cliente:', error)
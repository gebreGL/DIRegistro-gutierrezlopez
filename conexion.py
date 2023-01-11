from datetime import datetime

from PyQt6 import QtWidgets, QtSql

import var
import clientes
from ventMain import *

class Conexion():
    def conexion(self = None):
        filebd = 'bbdd.sqLite'
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filebd)
        var.bbdd = 'bbdd.sqlite'
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos', 'Conexión no establecida.\n'
                                           'Haga click para cerrar', QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        else:
            print('Conexión establecida')
        return True

    def cargarProv(self = None):
        try:
            var.ui.cbProvincia.clear()  #Cada vez que vaya a cargar, lo limpia y vuelve a citar las provincias
            query = QtSql.QSqlQuery()
            query.prepare('select provincia from provincias')
            if query.exec():
                var.ui.cbProvincia.addItem('')  #Para que aparezca vacío y no el primer elemento
                while query.next():
                    var.ui.cbProvincia.addItem(query.value(0))

        except Exception as error:
            print('Error al cargar las provincias:', error)


    def selMuni(self = None):
        try:
            id = 0
            var.ui.cbMunicipio.clear()
            prov = var.ui.cbProvincia.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia = :prov')
            query.bindValue(':prov', prov)
            if query.exec():
                while query.next():
                    id = query.value(0)
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id = :id')
            query1.bindValue(':id', int(id))
            if query1.exec():
                var.ui.cbMunicipio.addItem('')
                while query1.next():
                    var.ui.cbMunicipio.addItem(query1.value(0))

        except Exception as error:
            print('Error al cargar los municipios:', error)

    @staticmethod
    def altaCli(newcli, newcar):
        try:
            query = QtSql.QSqlQuery()
            queryCli = QtSql.QSqlQuery()
            query.prepare('insert into clientes (dni, nombre, alta, direccion, provincia, municipio, pago) '
                          'VALUES (:dni, :nombre, :alta, :direccion, :provincia, :municipio, :pago)')
            queryCli.prepare('select dni from clientes where dni = :dni')

            queryCli.bindValue(':dni', str(newcli[0]))
            query.bindValue(':dni', str(newcli[0]))
            query.bindValue(':nombre', str(newcli[1]))
            query.bindValue(':alta', str(newcli[2]))
            query.bindValue(':direccion', str(newcli[3]))
            query.bindValue(':provincia', str(newcli[4]))
            query.bindValue(':municipio', str(newcli[5]))
            query.bindValue(':pago', str(newcli[6]))

            if query.exec():
                pass
            query1 = QtSql.QSqlQuery()
            query1.prepare('insert into coches (matricula, dnicli, marca, modelo, motor) '
                          'VALUES (:matricula, :dnicli, :marca, :modelo, :motor)')
            query1.bindValue(':matricula', str(newcar[0]))
            query1.bindValue(':dnicli', str(newcli[0]))
            query1.bindValue(':marca', str(newcar[1]))
            query1.bindValue(':modelo', str(newcar[2]))
            query1.bindValue(':motor', str(newcar[3]))
            if query1.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Cliente - Coche dado de alta correctamente')
                msg.exec()
            else :
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query1.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas en la conexión al dar de alta al cliente:', error)

    @staticmethod
    def altaServicio(newservicio):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into servicios (concepto, precio-unidad) '
                          'VALUES (:concepto, :precio-unidad)')

            query.bindValue(':concepto', str(newservicio[0]))
            query.bindValue(':precio-unidad', str(newservicio[1]))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Servicio dado de alta correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas en la conexión al dar de alta al servicio:', error)


    def altaExcelCoche(new):
        try:
            query1 = QtSql.QSqlQuery()
            query1.prepare('insert into coches (matricula, dnicli, marca, modelo, motor) '
                           'VALUES (:matricula, :dnicli, :marca, :modelo, :motor)')
            query1.bindValue(':matricula', new[0])
            query1.bindValue(':dnicli', new[1])
            query1.bindValue(':marca', new[2])
            query1.bindValue(':modelo', new[3])
            query1.bindValue(':motor', new[4])
            if query1.exec():
                pass

        except Exception as e:
            print('Error al importar coches en Excel:', e)


    def mostrarTabcarcli(self):
        try :
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare(
                'select dnicli, matricula, marca, modelo, motor from coches where fechabajacar is null order by marca, modelo')

            if query.exec():
                while query.next():
                    var.ui.tabClientes.setRowCount(index + 1)  # Creamos la fila
                    var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(2))))
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(query.value(3))))
                    var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(query.value(4))))
                    var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1
        except Exception as error:
            print('Problema al mostrar el listado de coches de clientes:', error)


    def mostrarHistorico(self = None):
        try:
            if var.ui.chkHistorico.isChecked():
                index = 0
                query = QtSql.QSqlQuery()
                query.prepare(
                    'select dnicli, matricula, marca, modelo, motor from coches order by marca, modelo')

                if query.exec():
                    while query.next():
                        var.ui.tabClientes.setRowCount(index + 1)  # Creamos la fila
                        var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                        var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                        var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(2))))
                        var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(query.value(3))))
                        var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(query.value(4))))
                        var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        index += 1
            else:
                index = 0
                query = QtSql.QSqlQuery()
                query.prepare(
                    'select dnicli, matricula, marca, modelo, motor from coches where fechabajacar is null order by marca, modelo')

                if query.exec():
                    while query.next():
                        var.ui.tabClientes.setRowCount(index + 1)  # Creamos la fila
                        var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                        var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                        var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(2))))
                        var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(query.value(3))))
                        var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(query.value(4))))
                        var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        index += 1


        except Exception as error:
            print('Problema al mostrar el historico de coches y clientes:', error)

    def oneCli(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select nombre, alta, direccion, provincia, municipio, pago from '
                          'clientes where dni = :dni')
            query.bindValue(':dni', str(dni))
            if query.exec():
                while query.next():
                    for i in range(6):
                        registro.append(str(query.value(i)))
            return registro

        except Exception as e:
            print('Error en oneCli:', e)


    def borraCli(dni):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y-%m-%d-%H.%M.%S')
            query1 = QtSql.QSqlQuery()
            query1.prepare('update clientes set fechabajacli = :fecha where dni = :dni')
            query1.bindValue(':fecha', str(fecha))
            query1.bindValue(':dni', str(dni))
            if query1.exec():
                pass
            else:
                msg1 = QtWidgets.QMessageBox()
                msg1.setWindowTitle('Aviso')
                msg1.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg1.setText(query1.lastError().text())
                msg1.exec()
            query = QtSql.QSqlQuery()
            query.prepare('update coches set fechabajacar = :fecha where dnicli = :dni')
            query.bindValue(':fecha', str(fecha))
            query.bindValue(':dni', str(dni))
            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Cliente dado de baja correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
            '''
            query1 = QtSql.QSqlQuery()
            query1.prepare('delete from coches where dni_cli = :dni')
            query1.bindValue(':dni', str(dni))
            if query1.exec():
                pass
            query =  QtSql.QSqlQuery()
            query.prepare('delete from clientes where dni = :dni')
            query.bindValue(':dni', str(dni))
            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Cliente dado de baja correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
            '''

        except Exception as error:
            print('Error al borrar cliente:', error)

    def borraServ(concepto, precio):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from servicios where concepto = :concepto and precio-unidad = :precio')
            query.bindValue(':concepto', str(concepto))
            query.bindValue(':precio', str(precio))
            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Cliente dado de baja correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Error al borrar servicio:', error)


    def modificarDatos(modcli, modcar):
        try:
            registroCli = []
            registroCar = []

            query = QtSql.QSqlQuery()
            query.prepare('select nombre from clientes where dni = :dni')

            query.bindValue(':dni', str(modcli[0]))

            if query.exec():
                if query.next():
                    Conexion.modificaCli(modcli, modcar)
                else:
                    registroCli.append(str(modcli[0]))
                    registroCli.append('')
                    registroCli.append('')
                    registroCli.append('')
                    registroCli.append('')
                    registroCli.append('')
                    registroCli.append('')

                    registroCar.append('')
                    registroCar.append('')
                    registroCar.append('')
                    registroCar.append('')

                    Conexion.altaCli(registroCli, registroCar)
            # Comprobar si el dni existe. Si no existe crear al cliente con un coche vacio que tenga fecha de baja.

            Conexion.modificaCli(modcli, modcar)

        except Exception as error:
            print('Error al modificar datos en eventos: ', error)

    def modificaCli(modcli, modcar):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'update clientes set nombre = :nombre, alta = :alta, direccion = :direccion, provincia = :provincia, municipio = :municipio, pago = :pago where dni = :dni')

            query.bindValue(':dni', str(modcli[0]))
            query.bindValue(':nombre', str(modcli[1]))
            query.bindValue(':alta', str(modcli[2]))
            query.bindValue(':direccion', str(modcli[3]))
            query.bindValue(':provincia', str(modcli[4]))
            query.bindValue(':municipio', str(modcli[5]))
            query.bindValue(':pago', str(modcli[6]))

            if query.exec():
                pass

            query1 = QtSql.QSqlQuery()
            query1.prepare(
                'update coches set dnicli = :dnicli, marca = :marca, modelo = :modelo, motor = :motor where matricula = :matricula')

            query1.bindValue(':matricula', str(modcar[0]))
            query1.bindValue(':dnicli', str(modcli[0]))
            query1.bindValue(':marca', str(modcar[1]))
            query1.bindValue(':modelo', str(modcar[2]))
            query1.bindValue(':motor', str(modcar[3]))

            if query1.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Datos modificados correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()


        except Exception as error:
            print('Error en modificar clientes en conexion: ', error)


    def modificaServ(modserv):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'update servicios set concepto = :concepto, precio-unidad = :precio-unidad where codigo = :codigo')

            query.bindValue(':codigo', str(modserv[0]))
            query.bindValue(':concepto', str(modserv[1]))
            query.bindValue(':precio-unidad', str(modserv[2]))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Datos modificados correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()


        except Exception as error:
            print('Error al modificar servicios en conexion: ', error)


    def mostrarTabServicios(self):
        try :
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select * from servicios')

            if query.exec():
                while query.next():
                    var.ui.tabServizos.setRowCount(index + 1)  # Creamos la fila
                    var.ui.tabServizos.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    var.ui.tabServizos.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                    var.ui.tabServizos.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(2))))
                    var.ui.tabServizos.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tabServizos.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tabServizos.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1

        except Exception as error:
            print('Problema al mostrar el listado de servicios:', error)
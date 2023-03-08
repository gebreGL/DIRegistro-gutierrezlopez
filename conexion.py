from datetime import datetime

from PyQt6 import QtWidgets, QtSql

import conexion
import var
import clientes, facturas, events
from ventMain import *



class Conexion():
    '''
    Listado de funciones de la clase Conexión
    '''

    def conexion(self = None):
        '''
        Método que establece la conexión con la base de datos y devuelve un valor booleano en función de
        si esta se establece (true) o no (false)

        :param: None

        :return: boolean
        '''
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
        '''
        Método que carga las provincias de la base de datos en un comboBox

        :param: None

        :return: None
        '''
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
        '''
        Método que carga los municipios de la base de datos en un comboBox en función de la provincia seleccionada

        :param: None

        :return: None
        '''
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
        '''
        Método estático para dar de alta en la base de datos a un cliente

        :param: newcli: array de datos de un cliente
        :param: newcar: array de datos de un coche

        :return: None
        '''
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
        '''
        Método estático para dar de alta en la base de datos a un servicio

        :param: newservicio: array de datos de un servicio

        :return: None
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into servicios (concepto, preciounidad) VALUES (:concepto, :preciounidad)')

            query.bindValue(':concepto', str(newservicio[0]))
            query.bindValue(':preciounidad', str(newservicio[1]))

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
        '''
        Método que da de alta a un coche en la base de datos

        :param: new: array de datos de un coche

        :return: None
        '''
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
        '''
        Método que muestra los datos de un cliente de la base de datos en una tabla

        :param: self

        :return: None
        '''
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
        '''
        Método que muestra en la tabla de cliente todos los registros de los clientes,
        incluso los que han sido dados de baja

        :param: None

        :return: None
        '''
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
        '''
        Método que devuelve un array de datos de un cliente en función de su dni

        :param: dni: String que almacena el dni de un cliente

        :return: array de datos de un cliente
        '''
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
        '''
        Método que da de baja a un cliente en función de su dni insertando una fecha de baja en la base de datos

        :param: dni: String que almacena el dni de un cliente

        :return: None
        '''
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

        except Exception as error:
            print('Error al borrar cliente:', error)


    def borraServ(codigo):
        '''
        Método que borra un servicio de la base de datos

        :param: codigo: entero que almacena el codigo de un servicio, el cual es la clave primaria de la tabla servicios
                        en la base de datos

        :return: None
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from servicios where codigo = :codigo')
            query.bindValue(':codigo', str(codigo))
            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Servicio dado de baja correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Error al borrar servicio en conexion:', error)


    def borraFactura(idfac):
        '''
        Método que borra una factura de la base de datos

        :param: idfac: entero que almacena el codigo de una factura, la cual es la clave primaria de la tabla facturas
                    en la base de datos

        :return: None
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from facturas where idfac = :idfac')
            query.bindValue(':idfac', str(idfac))
            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Factura dada de baja correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Error al borrar imprimirFactura en conexion:', error)



    def modificarDatosCliente(modcli, modcar):
        '''
        Método para modificar los datos de un cliente y un coche en la base de datos

        :param: modcli: array de datos nuevos que va a tomar el nuevo cliente
        :param: modcli: array de datos nuevos que va a tomar el nuevo coche

        :return: None
        '''
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
        '''
        Método que modifica los datos de un cliente y coche en la base de datos

        :param: modcli: array de datos nuevos que va a tomar el nuevo cliente
        :param: modcli: array de datos nuevos que va a tomar el nuevo coche

        :return: None
        '''
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
        '''
        Método que modifica los datos de un servicio en la base de datos

        :param: modserv: array de datos nuevos que va a tomar el nuevo servicio

        :return: None
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'update servicios set concepto = :concepto, preciounidad = :preciounidad where codigo = :codigo')

            query.bindValue(':codigo', str(modserv[2]))
            query.bindValue(':concepto', str(modserv[0]))
            query.bindValue(':preciounidad', str(modserv[1]))

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


    def buscaServicio(concepto):
        '''
        Método que busca un servicio en la base de datos

        :param: concepto: String que almacena el concepto por el cual se va a buscar un servicio

        :return: String con el código del servicio buscado
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo from servicios where concepto = :concepto')
            query.bindValue(':concepto', str(concepto))
            if query.exec():
                while query.next():
                    codigoServicio = str(query.value(0))
            return codigoServicio
        except Exception as e:
            print('Error al buscar Servicio:', e)


    def mostrarTabServicios(self):
        '''
        Método que muestra los datos de todos los servicios de la base de datos

        :param: self

        :return: None
        '''
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


    def mostrarTabFacturas(self):
        '''
        Método que muestra los datos de todas las facturas de la base de datos

        :param: self

        :return: None
        '''
        try :
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select * from facturas')

            if query.exec():
                while query.next():
                    var.ui.tabFacturas.setRowCount(index + 1)  # Creamos la fila
                    var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                    var.ui.tabFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tabFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1

        except Exception as error:
            print('Problema al mostrar el listado de facturas:', error)



    def cargaComboVenta(self):
        '''
        Método que carga en un comboBox todos los concetos de los servicios de la base de datos

        :param: self

        :return: None
        '''
        try:
            var.cmbServicio.clear()
            query = QtSql.QSqlQuery()
            query.prepare('select concepto from servicios order by concepto')
            if query.exec():
                var.cmbServicio.addItem('')
                while query.next():
                    var.cmbServicio.addItem(str(query.value(0)))

        except Exception as e:
            print('Error en carga comboBox ventas:', e)


    def restoDatosFactura(numFactura):
        '''
        Método que devuelve datos de una factura en función de su numéro de factura

        :param: numFactura: entero que almacena el número de una factura

        :return: array de datos de una factura en función de su número de factura
        '''
        try:
            datos = []
            query = QtSql.QSqlQuery()
            query.prepare('select matfac, fechafac from facturas where idfac = :idfac')
            query.bindValue(':idfac', str(numFactura))
            if query.exec():
                while query.next():
                    for i in range(2):
                        datos.append(str(query.value(i)))
            return datos

        except Exception as e:
            print('Error al cargar resto de datos de la imprimirFactura', e)


    def obtenerPrecio(servicio):
        '''
        Método que devuelve el precio de un servicio en función de su concepto

        :param: servicio: String que almacena el concepto de un servicio

        :return: array de datos de un servicio en función de su concepto
        '''
        try:
            datos = []
            query = QtSql.QSqlQuery()
            query.prepare('select preciounidad, codigo from servicios where concepto = :servicio')
            query.bindValue(':servicio', str(servicio))

            if query.exec():
                while query.next():
                    codigo = str(query.value(1))
                    precio = str(query.value(0))

                    datos.append(codigo)
                    datos.append(precio)
            return datos

        except Exception as e:
            print("Error al obtener el precio del producto:", e)


    def buscarFactura(self):
        '''
        Método que facturas en la base de datos en función de su parámetro introducido en la caja de texto

        :param: self

        :return: None
        '''
        try:
            index = 0
            parametro = var.ui.txtBuscar.text()

            if var.ui.txtBuscar.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('Debe introducir un valor en el campo de texto')
                msg.exec()
            else:
                query = QtSql.QSqlQuery()
                query.prepare('select idfac, dni from facturas where idfac = :parametro or dni = :parametro')
                query.bindValue(':parametro', str(parametro))
                if  query.exec():
                    while query.next():
                        var.ui.tabFacturas.setRowCount(index + 1)  # Creamos la fila
                        var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                        var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                        var.ui.tabFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        var.ui.tabFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        index += 1
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    msg.setText(query.lastError().text())
                    msg.exec()

        except Exception as e:
            print('Error al buscar imprimirFactura:', e)


    @staticmethod
    def altaFactura(newFac):
        '''
        Método estático para dar de alta en la base de datos a una factura

        :param: newFac: array de datos de una factura

        :return: None
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas (dni, matfac, fechafac) VALUES (:dni, :matfac, :fechafac)')

            query.bindValue(':dni', str(newFac[0]))
            query.bindValue(':matfac', str(newFac[1]))
            query.bindValue(':fechafac', str(datetime.today().strftime('%Y-%m-%d-%H.%M.%S')))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Factura dada de alta correctamente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas en la conexión al dar de alta la factura:', error)

    def cargarLineasVenta(codigo_factura):
        """
        Carga las lineas de venta de una factura en la tabla de ventas

        :param codigo_factura: el codigo de la facturaactura

        :return: None
        """
        try:
            subtotal = 0.00
            iva = 0.00
            total = 0.00
            index = 0

            var.ui.tabVentas.setRowCount(0)

            query = QtSql.QSqlQuery()
            query.prepare('select codigo_servicio, precio, unidades, id_venta from ventas where codigo_factura = :codigo_factura')
            query.bindValue(':codigo_factura', int(codigo_factura))

            if query.exec():
                while query.next():
                    precio = str('{:.2f}'.format(round(query.value(1), 2))) + ' €'
                    cantidad = str('{:.2f}'.format(round(query.value(2), 2)))
                    servicio = Conexion.buscarConceptoServicio(int(query.value(0)))
                    subtotal = subtotal + round(query.value(1) * query.value(2), 2)
                    iva = subtotal * 0.21
                    total = subtotal + iva

                    suma = str(round(query.value(1) * query.value(2), 2))

                    var.ui.tabVentas.setRowCount(index + 1)

                    var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(3))))
                    # var.ui.tabVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    var.ui.tabVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(servicio))
                    # var.ui.tabVentas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    var.ui.tabVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio).replace('.', ',')))
                    # var.ui.tabVentas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    var.ui.tabVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(cantidad).replace('.', ',')))
                    # var.ui.tabVentas.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    var.ui.tabVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(str(suma + ' €')))
                    # var.ui.tabVentas.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    var.btnBorrar = QtWidgets.QPushButton()
                    var.icon = QtGui.QIcon()
                    var.icon.addPixmap(QtGui.QPixmap('img/papelera.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
                    var.btnBorrar.setIcon(var.icon)
                    var.btnBorrar.setFixedSize(30, 25)

                    var.ui.tabVentas.setCellWidget(index, 5, var.btnBorrar)

                    index = index + 1

                var.ui.lblRecuadroSubtotal.setText(str(str(round(subtotal, 2)) + ' €'))
                var.ui.lblRecuadroIVA.setText(str(str(round(iva, 2)) + ' €'))
                var.ui.lblRecuadroTotal.setText(str(str(round(total, 2)) + ' €'))

                facturas.Facturas.cargaLineaVenta(index)
                events.Eventos.resizeTablaventas(None)
                var.ui.tabVentas.scrollToBottom()
                var.cmbServicio.currentIndexChanged.connect(facturas.Facturas.cargaPrecioVenta)


        except Exception as error:
            print('Error en conexion.cargarlineasventa: ', error)

    def buscarConceptoServicio(codigo_servicio):
        '''
        Método para buscar el concepto de un servicio en la base de datos en función de su código

        :param: newservicio: array de datos de un servicio

        :return: None
        '''
        try:

            query = QtSql.QSqlQuery()
            query.prepare('select concepto from servicios where codigo = :codigo_servicio')
            query.bindValue(':codigo_servicio', str(codigo_servicio))

            if query.exec():
                while query.next():
                    servicio = str(query.value(0))
                return servicio

        except Exception as e:
            print('Error en buscarConceptoServicio:', e)

    def borrarLineaVenta(codigo_venta):
        '''
        Método estático para dar de alta en la base de datos a un servicio

        :param: codigo_servicio: entero que almacena el valor del código de una venta

        :return: None
        '''
        try:

            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where id_venta = :codigo_venta')
            query.bindValue(':codigo_venta', str(codigo_venta))

            if query.exec():
                pass

        except Exception as e:
            print('Error en borrarLineaVenta:', e)


    def cargarVentas(venta):
        '''
        Método para registrar nuevas ventas en la base de datos

        :param: venta: array de datos nuevos de una venta

        :return: None
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into ventas (codigo_factura, codigo_servicio, precio, unidades) '
                          'VALUES (:codigo_factura, :codigo_servicio, :precio, :unidades)')
            query.bindValue(':codigo_factura', int(venta[0]))
            query.bindValue(':codigo_servicio', int(venta[1]))
            query.bindValue(':precio', float(venta[2]))
            query.bindValue(':unidades', float(venta[3]))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Linea venta registrada')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as e:
            print('Error en cargarVenta:', e)
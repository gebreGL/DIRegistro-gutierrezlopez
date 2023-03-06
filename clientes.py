import clientes
import conexion
import facturas
import servicios
import var
from ventMain import *


class Clientes():
    def validarDNI(dni):

        '''
        Modulo para la validacion del DNI
        :return: booleano
        '''

        try:
            tabla = 'TRWAGMYFPDXBNJZSQCHLCKE'
            dig_ext = 'XYZ'
            reemplazar_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            dni = dni.upper()
            numeros = '1234567890'
            if (len(dni) == 9):
                dig_control = dni[8]
                dni = dni[:8]
                if (dni[0] in dig_ext):
                    dni = dni.replace(dni[0], reemplazar_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
            return False

        except Exception as error:
            print('Error al validar dni:', error)

    def mostrarValidadoDNI(self=None):
        try:
            dni = var.ui.txtDNI.text()
            if Clientes.validarDNI(dni):
                var.ui.lblValidarDNI.setStyleSheet('color: green')
                var.ui.lblValidarDNI.setText('V')
                var.ui.txtDNI.setText(dni.upper())
                var.ui.txtDNI.setStyleSheet('background-color: #F3F0A0;')
            else:
                var.ui.lblValidarDNI.setStyleSheet('color: red')
                var.ui.lblValidarDNI.setText('X')
                var.ui.txtDNI.setText(dni.upper())
                var.ui.txtDNI.setStyleSheet('background-color: pink;')
        except Exception as error:
            print('Error al validar dni:', error)

    def selMotor(self=None):
        try:
            var.motor = (var.ui.rbtGasolina, var.ui.rbtDiesel, var.ui.rbtHibrido, var.ui.rbtElectrico)
            for i in var.motor:
                i.toggled.connect(Clientes.checkMotor)

        except Exception as error:
            print('Error seleccion motor:', error)

    def checkMotor(self=None):
        try:
            if var.ui.rbtGasolina.isChecked():
                motor = 'Gasolina'
            elif var.ui.rbtDiesel.isChecked():
                motor = 'Diesel'
            elif var.ui.rbtHibrido.isChecked():
                motor = 'Hibrido'
            elif var.ui.rbtElectrico.isChecked():
                motor = 'Electrico'
            else:
                pass
            return motor
        except Exception as error:
            print('Error seleccion motor:', error)

    def cargaFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.txtFechaAltaCli.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as e:
            print('Error al cargar fecha de alta del cliente: ', e)

    def limpiaCli(self=None):
        try:
            cliente = [var.ui.txtDNI, var.ui.txtNombreCli, var.ui.txtDir,
                       var.ui.txtFechaAltaCli, var.ui.txtMatricula, var.ui.txtModelo, var.ui.txtMarca]
            for i in cliente:
                i.setText('')

            var.ui.cbProvincia.setCurrentText('')
            var.ui.cbMunicipio.setCurrentText('')
            checks = [var.ui.chkTrans, var.ui.chkTarj, var.ui.chkEfectivo]
            for i in checks:
                i.setChecked(False)
            servicios.Servicios.limpiaServicio()
            facturas.Facturas.limpiaFact()

        except Exception as error:
            print('Error al limpiar el cliente:', error)

    def guardaCli(self):
        try:
            if var.ui.txtDNI.text() == '' or var.ui.txtMatricula.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede guardar un registro con parámetros vacíos')
                msg.exec()
            else:
                newcli = []
                newcar = []
                pagos = []

                cliente = [var.ui.txtDNI, var.ui.txtNombreCli, var.ui.txtFechaAltaCli, var.ui.txtDir]
                car = [var.ui.txtMatricula, var.ui.txtMarca, var.ui.txtModelo]
                for i in cliente:
                    newcli.append(i.text())
                for i in car:
                    newcar.append(i.text())

                prov = var.ui.cbProvincia.currentText()
                motor = Clientes.checkMotor()
                muni = var.ui.cbMunicipio.currentText()

                newcli.append(prov)
                newcli.append(muni)
                newcar.append(motor)

                if var.ui.chkTarj.isChecked():
                    pagos.append('Tarjeta')

                elif var.ui.chkEfectivo.isChecked():
                    pagos.append('Efectivo')

                elif var.ui.chkTrans.isChecked():
                    pagos.append('Transferencia')

                pagos = set(pagos)  # Para evitar duplicados
                newcli.append('; '.join(pagos))

                conexion.Conexion.altaCli(newcli, newcar)
                conexion.Conexion.mostrarTabcarcli(self)
                print(newcli)
                print(newcar)

        except Exception as error:
            print('Error al guardar el cliente:', error)


    def modifCli(self=None):
        try:
            if var.ui.txtDNI.text() == '' or var.ui.txtMatricula.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede modificar un registro con parámetros vacíos')
                msg.exec()
            else:
                modcli = []
                modcar = []

                cliente = [var.ui.txtDNI, var.ui.txtNombreCli, var.ui.txtFechaAltaCli, var.ui.txtDir]
                for i in cliente:
                    modcli.append(i.text())

                prov = var.ui.cbProvincia.currentText()
                modcli.append(prov)

                muni = var.ui.cbMunicipio.currentText()
                modcli.append(muni)

                pagos = []
                if var.ui.chkEfectivo.isChecked():
                    pagos.append('Efectivo')
                if var.ui.chkTarj.isChecked():
                    pagos.append('Tarjeta')
                if var.ui.chkTrans.isChecked():
                    pagos.append('Transferencia')
                pagos = set(pagos)
                modcli.append('; '.join(pagos))

                car = [var.ui.txtMatricula, var.ui.txtMarca, var.ui.txtModelo]
                for i in car:
                    modcar.append(i.text())
                motor = Clientes.checkMotor()
                modcar.append(motor)

                conexion.Conexion.modificarDatosCliente(modcli, modcar)

                conexion.Conexion.mostrarTabcarcli(self)

        except Exception as error:
            print('Error al modificar cliente: ', error)


    def cargaCliente(self=None):
        try:
            Clientes.limpiaCli()
            facturas.Facturas.limpiaFact()
            fila = var.ui.tabClientes.selectedItems()
            row = [dato.text() for dato in fila] # Recoge todo lo que hay en cada fila de la tabla
            datos = [var.ui.txtDNI, var.ui.txtMatricula, var.ui.txtMarca, var.ui.txtModelo]

            for i, dato in enumerate(datos):
                dato.setText(row[i])
            if row[4] == 'Diesel':
                var.ui.rbtDiesel.setChecked(True)
            elif row[4] == 'Gasolina':
                var.ui.rbtGasolina.setChecked(True)
            elif row[4] == 'Hibrido':
                var.ui.rbtHibrido.setChecked(True)
            elif row[4] == 'Electrico':
                var.ui.rbtElectrico.setChecked(True)

            registro = conexion.Conexion.oneCli(row[0])
            var.ui.txtNombreCli.setText(registro[0])
            var.ui.txtFechaAltaCli.setText(registro[1])
            var.ui.txtDir.setText(registro[2])
            var.ui.cbProvincia.setCurrentText(str(registro[3]))
            var.ui.cbMunicipio.setCurrentText(str(registro[4]))

            if 'Efectivo' in registro[5]:
                var.ui.chkEfectivo.setChecked(True)
            if 'Tarjeta' in registro[5]:
                var.ui.chkTarj.setChecked(True)
            if 'Transferencia' in registro[5]:
                var.ui.chkTrans.setChecked(True)

            var.ui.txtDNIFactura.setText(row[0])
            var.ui.txtMatriculaFactura.setText(datos[1].text())


        except Exception as e:
            print('Error carga cliente:', e)


    def borraCli(self):
        try:
            if var.ui.txtDNI.text() == '' or var.ui.txtMatricula.text() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('No se puede eliminar un registro con parámetros vacíos')
                msg.exec()
            else:
                dni = var.ui.txtDNI.text()
                #conexion.Conexion.altaHistorico(cliente, coche)
                conexion.Conexion.borraCli(dni)
                conexion.Conexion.mostrarTabcarcli(self)

        except Exception as error:
            print('Error al borrar cliente:', error)

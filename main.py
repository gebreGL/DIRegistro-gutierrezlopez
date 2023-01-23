import facturas
import informes
import servicios
from dlgExportar import Ui_dlgExportar
from ventMain import *
from dlgSalir import *
from ventCalendar import *
from datetime import *
import sys, var, events, clientes, conexion, servicios


class DialogSalir(QtWidgets.QDialog) :
    def __init__ (self) :
        super(DialogSalir, self).__init__()
        var.avisosalir = Ui_dlgSalir()
        var.avisosalir.setupUi(self)
        #var.avisosalir.clicked.connect(events.Eventos.Salir)



class DialogExportar(QtWidgets.QDialog) :
    def __init__ (self) :
        super(DialogExportar, self).__init__()
        var.dlgExportar = Ui_dlgExportar()
        var.dlgExportar.setupUi(self)
        #var.dlgExportar.pushButton.clicked.connect(events.Eventos.exportarDatos)


class DialogCalendar(QtWidgets.QMainWindow) :
    def __init__ (self):
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = Ui_ventCalendar()
        var.dlgCalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        var.dlgCalendar.calendar.setSelectedDate(QtCore.QDate(ano, mes, dia))
        var.dlgCalendar.calendar.clicked.connect(clientes.Clientes.cargaFecha)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_ventMain()
        var.ui.setupUi(self)
        var.avisosalir = DialogSalir()
        var.dlgCalendar = DialogCalendar()
        var.dlgAbrir = FileDialogAbrir()
        var.dlgExportar = DialogExportar()

        '''
        Llamadas de funciones
        '''
        conexion.Conexion.conexion()
        conexion.Conexion.mostrarTabcarcli(self)

        conexion.Conexion.mostrarTabFacturas(self)

        '''
        Listado de eventos menú
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.salir)
        var.ui.actionSalirBar.triggered.connect(events.Eventos.salir)
        var.ui.actionCrear_Copia_Seguridad.triggered.connect(events.Eventos.creaBackup)
        var.ui.actionRestaurar_Copia_Seguridad.triggered.connect(events.Eventos.restauraBackup)
        var.ui.actionbackup.triggered.connect(events.Eventos.creaBackup)
        var.ui.actionrestBackup.triggered.connect(events.Eventos.restauraBackup)
        #var.ui.actionExportar_Datos.triggered.connect(events.Eventos.mostrarExportar)
        var.ui.actionExportar_Datos.triggered.connect(events.Eventos.exportarDatos)
        var.ui.actionImportar_Datos.triggered.connect(events.Eventos.importarDatos)
        var.ui.actionInformes_Clientes.triggered.connect(informes.Informes.listClientes)
        var.ui.actionInforme_Vehiculos.triggered.connect(informes.Informes.listAutos)

        '''
        Listado de eventos de cajas
        '''
        var.ui.txtDNI.editingFinished.connect(clientes.Clientes.mostrarValidadoDNI)
        var.ui.txtNombreCli.editingFinished.connect(events.Eventos.letrasCapital)
        var.ui.txtDir.editingFinished.connect(events.Eventos.letrasCapital)
        var.ui.txtMatricula.editingFinished.connect(events.Eventos.letrasCapital)
        var.ui.txtMarca.editingFinished.connect(events.Eventos.letrasCapital)
        var.ui.txtModelo.editingFinished.connect(events.Eventos.letrasCapital)

        var.ui.txtConcepto.editingFinished.connect(events.Eventos.letrasCapital)

        '''
        Llamadas a eventos de combo box
        '''
        conexion.Conexion.cargarProv()
        var.ui.cbProvincia.currentIndexChanged.connect(conexion.Conexion.selMuni)

        var.ui.chkHistorico.stateChanged.connect(conexion.Conexion.mostrarHistorico)


        '''
        Listado de eventos de botones
        '''
        var.ui.btnGuardarCli.clicked.connect(clientes.Clientes.guardaCli)
        var.ui.btnFechaAltaCliente.clicked.connect(events.Eventos.abrirCalendar)
        var.ui.btnLimpiarCli.clicked.connect(clientes.Clientes.limpiaCli)
        var.ui.btnDeleteCli.clicked.connect(clientes.Clientes.borraCli)
        var.ui.btnModificarCli.clicked.connect(clientes.Clientes.modifCli)

        var.ui.btnGuardarServizo.clicked.connect(servicios.Servicios.guardaServicio)
        var.ui.btnExportarServizo.clicked.connect(events.Eventos.exportarServicio)
        var.ui.btnDeleteCli.clicked.connect(servicios.Servicios.borraServ)



        '''
        Funciones relacionadas con las tablas
        '''
        conexion.Conexion.mostrarTabcarcli(self)
        conexion.Conexion.mostrarTabServicios(self)
        events.Eventos.resizeTablacarcli(self)
        #var.ui.tabClientes.setTelectionBehavior(QtWidgets.QTableWidget.S)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaCliente)

        var.ui.tabServizos.clicked.connect(servicios.Servicios.cargaServicio)

        var.ui.tabFacturas.clicked.connect(facturas.Facturas.cargaFactura)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
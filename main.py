import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.get_available_ss()

        self.setup_ui()
        self.init_signals()

    def setup_ui(self):
        """Первоначальная инициализация интерфейса"""

        self.setWindowTitle('Hello world!')

        # Central widgets & layouts
        self.central_wgt = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QVBoxLayout(self.central_wgt)
        self.header_btns_hl = HeaderButtonsHL()
        self.central_layout.addLayout(self.header_btns_hl)
        self.setCentralWidget(self.central_wgt)

        # Dock widget
        dw_content_wgt = QtWidgets.QWidget()
        dw_layout = QtWidgets.QVBoxLayout(dw_content_wgt)
        self.style_lw = QtWidgets.QListWidget(dw_content_wgt)
        # self.fill_style_lw()
        dw_layout.addWidget(self.style_lw)
        self.style_dw = QtWidgets.QDockWidget('Style', self.central_wgt)
        self.style_dw.setWidget(dw_content_wgt)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.style_dw)

        # Actions
        self.exit_action = QtWidgets.QAction('Exit')
        self.exit_action.setShortcut('Ctrl+Q')
        self.action_1 = QtWidgets.QAction('Action_1')
        self.action_2 = QtWidgets.QAction('Action_2')
        self.action_3 = QtWidgets.QAction('Action_3')

        # Menus
        menu_bar = QtWidgets.QMenuBar()
        first_menu = QtWidgets.QMenu('First menu', menu_bar)
        second_menu = QtWidgets.QMenu('Second menu', menu_bar)
        sub_menu = QtWidgets.QMenu('Sub menu', menu_bar)
        first_menu.addAction(self.exit_action)
        second_menu.addAction(self.action_1)
        second_menu.addMenu(sub_menu)
        sub_menu.addAction(self.action_2)
        sub_menu.addAction(self.action_3)
        menu_bar.addMenu(first_menu)
        menu_bar.addMenu(second_menu)
        self.setMenuBar(menu_bar)

    def init_signals(self):
        """Инициализация сигналов"""
        self.exit_action.triggered.connect(QtWidgets.qApp.exit)

    def center(self):
        """Располагает виджет MainWindow в центре экрана, на котором располагается курсор мыши"""
        desktop = QtWidgets.qApp.desktop()
        screen = desktop.screenNumber(QtGui.QCursor.pos())
        center = desktop.screenGeometry(screen).center()
        self.move(center.x() - int(self.width() / 2), center.y() - int(self.height() / 2))

    def get_available_ss(self):
        config_dir_path = Path(QtWidgets.qApp.property('config_dir_path'))
        for path in config_dir_path.iterdir():
            if path.suffix == '.stylesheet':
                print(path)


class HeaderButtonsHL(QtWidgets.QHBoxLayout):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.style_wgt_pb = QtWidgets.QPushButton()
        self.table_wgt_pb = QtWidgets.QPushButton()
        self.text_wgt_pb = QtWidgets.QPushButton()
        self.text_clear_pb = QtWidgets.QPushButton()
        self.text_add_pb = QtWidgets.QPushButton()
        for pb in (self.style_wgt_pb, self.table_wgt_pb, self.text_wgt_pb, self.text_clear_pb, self.text_add_pb):
            self.addWidget(pb)

    def connect_signals(self):
        # self.style_wgt_pb.clicked.connect()
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    config_dir_path = Path(sys.argv[0]).parent / 'config'
    app.setProperty('config_dir_path', config_dir_path)

    main_window = MainWindow()
    main_window.center()
    main_window.show()

    sys.exit(app.exec())

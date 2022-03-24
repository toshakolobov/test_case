import configparser
import re
import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.iniconfig_path = Path(QtWidgets.qApp.property('config_dir_path')) / 'conf.ini'

        self.style_dict = {}
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
        self.init_fill_style_lw()
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
        # self.style_lw.currentItemChanged.connect(self.on_style_lw_current_item_changed)
        self.style_lw.itemSelectionChanged.connect(self.on_style_lw_selection_changed)

    def center(self):
        """Располагает виджет MainWindow в центре экрана, на котором располагается курсор мыши"""
        desktop = QtWidgets.qApp.desktop()
        screen = desktop.screenNumber(QtGui.QCursor.pos())
        center = desktop.screenGeometry(screen).center()
        self.move(center.x() - int(self.width() / 2), center.y() - int(self.height() / 2))

    def get_available_ss(self):
        config_dir_path = Path(QtWidgets.qApp.property('config_dir_path'))
        wgt_types = ('QFrame', 'QListWidget', 'QStatusBar')
        for path in config_dir_path.iterdir():
            if path.suffix == '.stylesheet':
                style_name = path.stem.capitalize()
                self.style_dict[style_name] = {
                    'style_lw_item': QtWidgets.QListWidgetItem(style_name)
                }
                with open(path, 'r') as handle:
                    content = handle.read()
                    for wgt_type in wgt_types:
                        style = None
                        if search := re.search(fr'{wgt_type}\s*({{.+?}})', content, re.DOTALL):
                            style = re.sub('\s+', ' ', search.group(1))
                        self.style_dict[style_name][wgt_type] = style

    def init_fill_style_lw(self):
        for style_name in sorted(self.style_dict.keys()):
            item = self.style_dict[style_name]['style_lw_item']
            self.style_lw.addItem(item)
        self.select_style(self.iniconfig_style)

    def select_style(self, style_name):
            try:
                self.style_lw.setCurrentItem(self.style_dict[style_name]['style_lw_item'])
            except Exception:
                self.style_lw.setCurrentRow(-1)

    @property
    def iniconfig_style(self):
        inicfg = configparser.ConfigParser()
        inicfg.read(self.iniconfig_path)
        value = None
        try:
            value = inicfg.get('view', 'style')
        except Exception:
            pass
        return value

    @iniconfig_style.setter
    def iniconfig_style(self, value):
        inicfg = configparser.ConfigParser()
        inicfg.read(self.iniconfig_path)
        if not inicfg.has_section('view'):
            inicfg.add_section('view')
        inicfg.set('view', 'style', value)
        with open(self.iniconfig_path, 'w+') as handle:
            inicfg.write(handle)

    # @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    # def on_style_lw_current_item_changed(self, current: QtWidgets.QListWidgetItem,
    #                                      previous: QtWidgets.QListWidgetItem):
    #     print(None if previous is None else previous.text())
    #     print(None if current is None else current.text())
    #     print('#' * 150)

    @QtCore.pyqtSlot()
    def on_style_lw_selection_changed(self):
        print(self.style_lw.selectedItems())


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

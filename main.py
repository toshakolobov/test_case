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
        self.read_available_ss()

        self.setup_ui()
        self.connect_init_signals()

        self.init_fill_style_lw()

    def add_child_text_wgt(self):
        wgt = CustomText(f'Text_{self.text_wgt.layout().count() + 1}')
        wgt.ok_pb_signal.connect(self.on_child_text_ok_pb_signal_emitted)
        wgt.del_pb_signal.connect(self.on_child_text_del_pb_signal_emitted)
        self.text_wgt.layout().addWidget(wgt)

    def center(self):
        """Располагает виджет MainWindow в центре экрана, на котором располагается курсор мыши"""
        desktop = QtWidgets.qApp.desktop()
        screen = desktop.screenNumber(QtGui.QCursor.pos())
        center = desktop.screenGeometry(screen).center()
        self.move(center.x() - int(self.width() / 2), center.y() - int(self.height() / 2))

    def change_wgts_style(self, style_name):
        style_info = None if style_name is None else self.style_dict[style_name]['style']
        self.setStyleSheet(style_info)

    def check_if_spacer_is_needed(self):
        is_needed = True
        for i in range(self.table_text_layout.count()):
            wgt = self.table_text_layout.itemAt(i).widget()
            if wgt.isVisible():
                is_needed = False
                break
        if is_needed:
            self.spacer_item.changeSize(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        else:
            self.spacer_item.changeSize(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)

    def connect_init_signals(self):
        self.exit_action.triggered.connect(QtWidgets.qApp.exit)
        for action in (self.action_1, self.action_2, self.action_3):
            action.triggered.connect(self.on_action_triggered)
        self.style_dw.visibilityChanged.connect(self.on_style_dw_visibility_changed)
        self.style_lw.itemSelectionChanged.connect(self.on_style_lw_selection_changed)

        self.header_btns_wgt.style_wgt_signal.connect(self.on_style_wgt_signal_emitted)
        self.header_btns_wgt.table_wgt_signal.connect(self.on_table_wgt_signal_emitted)
        self.header_btns_wgt.text_wgt_signal.connect(self.on_text_wgt_signal_emitted)
        self.header_btns_wgt.text_clear_signal.connect(self.on_text_clear_signal_emitted)
        self.header_btns_wgt.text_add_signal.connect(self.on_text_add_signal_emitted)

    def init_fill_style_lw(self):
        for style_name in sorted(self.style_dict.keys()):
            item = self.style_dict[style_name]['style_lw_item']
            self.style_lw.addItem(item)
        self.select_style_item(self.iniconfig_style)

    def read_available_ss(self):
        config_dir_path = Path(QtWidgets.qApp.property('config_dir_path'))

        for path in config_dir_path.iterdir():
            if path.suffix == '.stylesheet':
                style_name = path.stem.capitalize()
                self.style_dict[style_name] = {
                    'style_lw_item': QtWidgets.QListWidgetItem(style_name)
                }
                with open(path, 'r') as handle:
                    content = handle.read()
                    self.style_dict[style_name]['style'] = re.sub(r'QFrame', r'#centralwidget', content)

    def select_style_item(self, style_name):
        try:
            self.style_lw.setCurrentItem(self.style_dict[style_name]['style_lw_item'])
        except Exception:
            self.style_lw.setCurrentRow(-1)

    def setup_ui(self):

        # main window title
        self.setWindowTitle('Hello world!')

        # central widgets & layouts
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName('centralwidget')
        central_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.header_btns_wgt = HeaderButtons()
        central_layout.addWidget(self.header_btns_wgt)
        self.spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        central_layout.addSpacerItem(self.spacer_item)

        self.table_text_layout = QtWidgets.QHBoxLayout()
        central_layout.addLayout(self.table_text_layout)

        self.setCentralWidget(self.centralwidget)

        # dock widget
        self.style_dw = QtWidgets.QDockWidget('Style', self.centralwidget)
        dw_content_wgt = QtWidgets.QWidget()
        dw_layout = QtWidgets.QVBoxLayout(dw_content_wgt)
        dw_layout.setContentsMargins(0, 0, 0, 0)
        self.style_lw = QtWidgets.QListWidget(dw_content_wgt)
        dw_layout.addWidget(self.style_lw)
        self.style_dw.setWidget(dw_content_wgt)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.style_dw)

        # table
        self.table_wgt = CustomTable(self.centralwidget)
        self.table_text_layout.addWidget(self.table_wgt)

        # text widget
        self.text_wgt = QtWidgets.QWidget(self.centralwidget)
        self.text_wgt.setLayout(QtWidgets.QVBoxLayout())
        self.add_child_text_wgt()
        self.table_text_layout.addWidget(self.text_wgt)

        # actions
        self.exit_action = QtWidgets.QAction('Exit')
        self.exit_action.setShortcut('Ctrl+Q')
        self.action_1 = QtWidgets.QAction('Action 1')
        self.action_2 = QtWidgets.QAction('Action 2')
        self.action_3 = QtWidgets.QAction('Action 3')

        # menus
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

        # status bar
        status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(status_bar)

    # properties
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
        try:
            inicfg.set('view', 'style', value)
        except Exception:
            inicfg.set('view', 'style', '')
        with open(self.iniconfig_path, 'w+') as handle:
            inicfg.write(handle)

    # qt slots
    @QtCore.pyqtSlot()
    def on_action_triggered(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text())

    @QtCore.pyqtSlot()
    def on_child_text_del_pb_signal_emitted(self):
        sender = self.sender()
        self.text_wgt.layout().removeWidget(sender)

    @QtCore.pyqtSlot()
    def on_child_text_ok_pb_signal_emitted(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text_wgt.toPlainText())

    @QtCore.pyqtSlot(bool)
    def on_style_dw_visibility_changed(self, is_visible):
        self.header_btns_wgt.change_pb_text(self.header_btns_wgt.style_wgt_pb, is_visible)

    @QtCore.pyqtSlot()
    def on_style_lw_selection_changed(self):
        style_name = None
        if items := self.style_lw.selectedItems():
            style_name = items[0].text()
        self.change_wgts_style(style_name)
        self.iniconfig_style = style_name

    @QtCore.pyqtSlot()
    def on_style_wgt_signal_emitted(self):
        self.style_dw.setVisible(not self.style_dw.isVisible())

    @QtCore.pyqtSlot()
    def on_table_wgt_signal_emitted(self):
        self.table_wgt.setVisible(not self.table_wgt.isVisible())
        self.header_btns_wgt.change_pb_text(self.header_btns_wgt.table_wgt_pb, self.table_wgt.isVisible())
        self.check_if_spacer_is_needed()

    @QtCore.pyqtSlot()
    def on_text_add_signal_emitted(self):
        self.add_child_text_wgt()

    @QtCore.pyqtSlot()
    def on_text_clear_signal_emitted(self):
        layout = self.text_wgt.layout()
        for i in range(layout.count()):
            child_text_wgt = layout.itemAt(i).widget()
            child_text_wgt.text_wgt.clear()

    @QtCore.pyqtSlot()
    def on_text_wgt_signal_emitted(self):
        self.text_wgt.setVisible(not self.text_wgt.isVisible())
        self.header_btns_wgt.change_pb_text(self.header_btns_wgt.text_wgt_pb, self.text_wgt.isVisible())
        self.check_if_spacer_is_needed()


class HeaderButtons(QtWidgets.QWidget):
    style_wgt_signal = QtCore.pyqtSignal()
    table_wgt_signal = QtCore.pyqtSignal()
    text_wgt_signal = QtCore.pyqtSignal()
    text_clear_signal = QtCore.pyqtSignal()
    text_add_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_init_signals()

    def connect_init_signals(self):
        self.style_wgt_pb.clicked.connect(self.style_wgt_signal)
        self.table_wgt_pb.clicked.connect(self.table_wgt_signal)
        self.text_wgt_pb.clicked.connect(self.text_wgt_signal)
        self.text_clear_pb.clicked.connect(self.text_clear_signal)
        self.text_add_pb.clicked.connect(self.text_add_signal)

    def setup_ui(self):
        self.setLayout(QtWidgets.QHBoxLayout())
        self.style_wgt_pb = QtWidgets.QPushButton('Hide style panel')
        self.table_wgt_pb = QtWidgets.QPushButton('Hide table')
        self.text_wgt_pb = QtWidgets.QPushButton('Hide text panel')
        self.text_clear_pb = QtWidgets.QPushButton('Clear text fields')
        self.text_add_pb = QtWidgets.QPushButton('Add text field')
        for pb in (self.style_wgt_pb, self.table_wgt_pb, self.text_wgt_pb, self.text_clear_pb, self.text_add_pb):
            self.layout().addWidget(pb)

    # static methods
    @staticmethod
    def change_pb_text(btn: QtWidgets.QPushButton, is_visible):
        if is_visible:
            action = 'Hide'
        else:
            action = 'Show'
        btn.setText(re.sub(r'Hide|Show', action, btn.text()))


class CustomTable(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_init_signals()

    def connect_init_signals(self):
        self.add_line_pb.clicked.connect(self.on_add_line_pb_clicked)
        self.del_line_pb.clicked.connect(lambda f: self.table_wgt.removeRow(self.table_wgt.rowCount() - 1))

    def setup_ui(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        self.table_wgt = QtWidgets.QTableWidget(0, 3)
        self.table_wgt.setHorizontalHeaderLabels(('Id', 'Parameter', 'Value'))
        self.table_wgt.horizontalHeader().setDefaultSectionSize(10)
        self.table_wgt.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.table_wgt.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table_wgt.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.table_wgt.verticalHeader().setVisible(False)
        self.layout().addWidget(self.table_wgt)

        btn_layout = QtWidgets.QHBoxLayout()
        self.add_line_pb = QtWidgets.QPushButton('Add line')
        self.del_line_pb = QtWidgets.QPushButton('Delete line')
        btn_layout.addWidget(self.add_line_pb)
        btn_layout.addWidget(self.del_line_pb)
        self.layout().addLayout(btn_layout)

    # qt slots
    @QtCore.pyqtSlot()
    def on_add_line_pb_clicked(self):
        row_count = self.table_wgt.rowCount()
        self.table_wgt.insertRow(self.table_wgt.rowCount())
        self.table_wgt.setItem(row_count, 0, QtWidgets.QTableWidgetItem(f'Id_{row_count + 1}'))
        self.table_wgt.setItem(row_count, 1, QtWidgets.QTableWidgetItem(f'Parameter_{row_count + 1}'))
        self.table_wgt.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row_count + 1) * 3))


class CustomText(QtWidgets.QWidget):
    ok_pb_signal = QtCore.pyqtSignal()
    del_pb_signal = QtCore.pyqtSignal()

    def __init__(self, init_text: str, parent=None):
        super().__init__(parent)
        self.init_text = init_text
        self.setup_ui()
        self.connect_init_signals()

    def connect_init_signals(self):
        self.del_pb.clicked.connect(self.del_pb_signal)
        self.ok_pb.clicked.connect(self.ok_pb_signal)

    def setup_ui(self):
        self.setLayout(QtWidgets.QHBoxLayout())
        self.text_wgt = QtWidgets.QTextEdit(self.init_text)
        self.layout().addWidget(self.text_wgt)

        btn_layout = QtWidgets.QVBoxLayout()
        self.del_pb = QtWidgets.QPushButton('X')
        self.del_pb.setFixedSize(40, 20)
        self.ok_pb = QtWidgets.QPushButton('OK')
        self.ok_pb.setFixedSize(40, 20)
        btn_layout.addWidget(self.del_pb)
        btn_layout.addWidget(self.ok_pb)
        self.layout().addLayout(btn_layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    config_dir_path = Path(sys.argv[0]).parent / 'config'
    app.setProperty('config_dir_path', config_dir_path)

    main_window = MainWindow()
    main_window.center()
    main_window.show()

    sys.exit(app.exec())

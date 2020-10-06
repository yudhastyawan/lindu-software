style = """
QMainWindow {
    background-color: white;
    color: black;
    border: none;    
}
QMenuBar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 lightgray, stop:1 darkgray);
    spacing: 3px; /* spacing between menu bar items */
}
QMenuBar::item {
    padding: 1px 4px;
    background: transparent;
    border-radius: 4px;
}

QMenuBar::item:selected { /* when selected using mouse or keyboard */
    background: #a8a8a8;
    color: white;
}

QMenuBar::item:pressed {
    background: #888888;
}

QMenu::item {
    /* sets background of menu item. set this to something non-transparent
        if you want menu color and menu item color to be different */
    background-color: transparent;
}
QMenu::item:selected { /* when user selects item using mouse or keyboard */
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #a8a8a8, stop:1 #888888);
    color: white;
}
QMenu {
    background-color: white;
    margin: 2px; /* some spacing around the menu */
}
QMenu::separator {
    height: 3px;
    background: #888888;
    margin-left: 10px;
    margin-right: 5px;
}
QMenu::indicator {
    width: 13px;
    height: 13px;
}

QComboBox {
    border: 1px solid gray;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}
QComboBox:editable {
    background: white;
}
QComboBox:!editable, QComboBox::drop-down:editable {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
}
QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}
QComboBox QAbstractItemView {
    border: 2px solid darkgray;
    selection-background-color: #888888;
}
QTabBar::tab:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #a8a8a8, stop:1 #888888);
    color: white;
}
QTabBar::close-button {
    border: 2px solid white;
    background-color: red;
    border-radius: 8px;
}
QTabBar::close-button::hover {
    background-color: white;
    border-radius: 8px;
    /* image: url(close.png); */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left; /* position at the top center */
    padding: 2 5px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #a8a8a8, stop:1 #888888);
    color: white;
}

QLineEdit {
    border-radius: 4px;
    padding: 0 10px;
    border: 0.5px solid gray;
}
QLineEdit::hover {
    background-color: #888888;
    color: white;
}

QPushButton::hover, QToolButton::hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #a8a8a8, stop:1 #888888);
    color: white;
    border: none;    
}
QPushButton:pressed, QToolButton::pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}
QCheckBox::hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #a8a8a8, stop:1 #888888);
    color: white;
    border: none;    
}
QLabel::hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #a8a8a8, stop:1 #888888);
    color: white;
    border: none;    
}

"""
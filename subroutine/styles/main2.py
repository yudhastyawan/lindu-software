style = """
QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border: 2px solid #C4C4C3;
    border-bottom-color: #C2C7CB; /* same as the pane color */
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 8ex;
    padding: 2px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
}

QTabBar::tab:selected {
    border-color: #9B9B9B;
    border-bottom-color: #C2C7CB; /* same as pane color */
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}

/* make use of negative margins for overlapping tabs */
QTabBar::tab:selected {
    /* expand/overlap to the left and right by 4px */
    margin-left: -4px;
    margin-right: -4px;
}

QTabBar::tab:first:selected {
    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
}

QTabBar::tab:last:selected {
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
}

QTabBar::tab:only-one {
    margin: 0; /* if there is only one tab, we don't want overlapping margins */
}
QGroupBox {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);
    border: 2px solid gray;
    border-radius: 5px;
    margin-top: 1ex; /* leave space at the top for the title */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center; /* position at the top center */
    padding: 2 5px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #FF0ECE, stop: 1 #FFFFFF);
}
QGroupBox::indicator {
    width: 13px;
    height: 13px;
}

QGroupBox::indicator:unchecked {
    image: url(:/images/checkbox_unchecked.png);
}

/* proceed with styling just like QCheckBox */
QLineEdit {
    border: 2px solid gray;
    border-radius: 10px;
    padding: 0 8px;
    background: yellow;
    selection-background-color: darkgray;
}
QListView {
    alternate-background-color: yellow;
}
QListView {
    show-decoration-selected: 1; /* make the selection span the entire width of the view */
}

QListView::item:alternate {
    background: #EEEEEE;
}

QListView::item:selected {
    border: 1px solid #6a6ea9;
}

QListView::item:selected:!active {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #ABAFE5, stop: 1 #8588B2);
}

QListView::item:selected:active {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #6a6ea9, stop: 1 #888dd9);
}

QListView::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);
}
QMainWindow::separator {
    background: yellow;
    width: 10px; /* when vertical */
    height: 10px; /* when horizontal */
}

QMainWindow::separator:hover {
    background: red;
}
QMenu {
    background-color: #ABABAB; /* sets background of the menu */
    border: 1px solid black;
}

QMenu::item {
    /* sets background of menu item. set this to something non-transparent
        if you want menu color and menu item color to be different */
    background-color: transparent;
}

QMenu::item:selected { /* when user selects item using mouse or keyboard */
    background-color: #654321;
}
QMenu {
    background-color: white;
    margin: 2px; /* some spacing around the menu */
}

QMenu::item {
    padding: 2px 25px 2px 20px;
    border: 1px solid transparent; /* reserve space for selection border */
}

QMenu::item:selected {
    border-color: darkblue;
    background: rgba(100, 100, 100, 150);
}

QMenu::icon:checked { /* appearance of a 'checked' icon */
    background: gray;
    border: 1px inset gray;
    position: absolute;
    top: 1px;
    right: 1px;
    bottom: 1px;
    left: 1px;
}

QMenu::separator {
    height: 2px;
    background: lightblue;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::indicator {
    width: 13px;
    height: 13px;
}

/* non-exclusive indicator = check box style indicator (see QActionGroup::setExclusive) */
QMenu::indicator:non-exclusive:unchecked {
    image: url(:/images/checkbox_unchecked.png);
}

QMenu::indicator:non-exclusive:unchecked:selected {
    image: url(:/images/checkbox_unchecked_hover.png);
}

QMenu::indicator:non-exclusive:checked {
    image: url(:/images/checkbox_checked.png);
}

QMenu::indicator:non-exclusive:checked:selected {
    image: url(:/images/checkbox_checked_hover.png);
}

/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
QMenu::indicator:exclusive:unchecked {
    image: url(:/images/radiobutton_unchecked.png);
}

QMenu::indicator:exclusive:unchecked:selected {
    image: url(:/images/radiobutton_unchecked_hover.png);
}

QMenu::indicator:exclusive:checked {
    image: url(:/images/radiobutton_checked.png);
}

QMenu::indicator:exclusive:checked:selected {
    image: url(:/images/radiobutton_checked_hover.png);
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
}

QMenuBar::item:pressed {
    background: #888888;
}
QPushButton {
    border: 2px solid #8f8f91;
    border-radius: 6px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
    min-width: 80px;
}

QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}

QPushButton:flat {
    border: none; /* no border for a flat push button */
}

QPushButton:default {
    border-color: navy; /* make the default button prominent */
}
QPushButton:open { /* when the button has its menu open */
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}

QPushButton::menu-indicator {
    image: url(menu_indicator.png);
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
}

QPushButton::menu-indicator:pressed, QPushButton::menu-indicator:open {
    position: relative;
    top: 2px; left: 2px; /* shift the arrow by 2 px */
}
QStatusBar {
    background: brown;
}

QStatusBar::item {
    border: 1px solid red;
    border-radius: 3px;
}
QStatusBar QLabel {
    border: 3px solid white;
}
QTableView {
    selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
                                stop: 0 #FF92BB, stop: 1 white);
}
QTableView QTableCornerButton::section {
    background: red;
    border: 2px outset red;
}
QTableView::indicator:unchecked {
    background-color: #d7d6d5
}
QToolButton { /* all types of tool button */
    border: 2px solid #8f8f91;
    border-radius: 6px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
}

QToolButton[popupMode="1"] { /* only for MenuButtonPopup */
    padding-right: 20px; /* make way for the popup button */
}

QToolButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}

/* the subcontrols below are used only in the MenuButtonPopup mode */
QToolButton::menu-button {
    border: 2px solid gray;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    /* 16px width + 4px for border = 20px allocated above */
    width: 16px;
}

QToolButton::menu-arrow {
    image: url(downarrow.png);
}

QToolButton::menu-arrow:open {
    top: 1px; left: 1px; /* shift it a bit */
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

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}
QComboBox QAbstractItemView {
    border: 2px solid darkgray;
    selection-background-color: lightgray;
}
QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 13px;
    height: 13px;
"""
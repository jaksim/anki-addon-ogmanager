from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from PyQt4 import QtCore, QtGui

# ===================== Generated UI Code goes below =====================

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(504, 484)
        Dialog.setMinimumSize(QtCore.QSize(400, 300))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.treeWidget = QtGui.QTreeWidget(Dialog)
        self.treeWidget.setAcceptDrops(False)
        self.treeWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropOverwriteMode(False)
        self.treeWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setExpandsOnDoubleClick(True)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.verticalLayout.addWidget(self.treeWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(Dialog)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnRemove = QtGui.QPushButton(Dialog)
        self.btnRemove.setEnabled(False)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.horizontalLayout.addWidget(self.btnRemove)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Options Groups Manager", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p>To see which decks use the options group, click on the plus sign next to its name.</p><p>Double clicking on the name of an options group will bring up the standard Anki dialog to change the settings (it will be opened with a dummy deck).</p><p>Double clicking on the name of a deck will let you change its options group using the standard Anki dialog.</p></body></html>", None))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "1", None))
        self.btnAdd.setText(_translate("Dialog", "Add", None))
        self.btnRemove.setText(_translate("Dialog", "Remove", None))
        self.btnClose.setText(_translate("Dialog", "Close", None))


# ===================== Generated UI code goes above =====================


# ===================== OGManager code =====================

class OGManager(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self)

        self.mw = mw

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.treeWidget.viewport().installEventFilter(self)

        root = self.ui.treeWidget.invisibleRootItem()
        root.setFlags(root.flags() & ~Qt.ItemIsDropEnabled)

    #Event filter allows changing options groups by drag and drop
    def eventFilter(self, obj, event):
        if (event.type() == QEvent.DragEnter):
            self.dragged_item = self.ui.treeWidget.selectedItems()[0]
        if (event.type() == QEvent.Drop and self.dragged_item):
            old_parent = self.dragged_item.parent()
            item_at = self.ui.treeWidget.itemAt(QDropEvent.pos(event))
            new_parent = item_at.parent() if item_at.parent() else item_at
            deck = mw.col.decks.byName(self.dragged_item.text(0))
            index = self.ui.treeWidget.indexOfTopLevelItem(new_parent)
            mw.col.decks.setConf(deck, self.ogs[index]['id'])
        return False

    def refresh(self):
        self.ui.treeWidget.clear()
        self.ogs = mw.col.decks.allConf()
        for og in self.ogs:
            og_item = QTreeWidgetItem(self.ui.treeWidget)
            og_item.setFlags(og_item.flags() & ~Qt.ItemIsDragEnabled)
            og_item.setText(0, og['name'])
            font = og_item.font(0)
            font.setBold(True)
            font.setWeight(75)
            og_item.setFont(0, font)
            self.ui.treeWidget.addTopLevelItem(og_item)
            dids = mw.col.decks.didsForConf(og)
            for did in dids:
                deck = mw.col.decks.get(did)
                deck_item = QTreeWidgetItem(og_item)
                deck_item.setFlags(deck_item.flags() & ~Qt.ItemIsDropEnabled)
                deck_item.setText(0, deck['name'])
                og_item.addChild(deck_item)

    def refresh_and_show(self):
        self.refresh()
        self.show()


# ===================== Add to Anki's Tools menu =====================

og = OGManager(mw)
action = QAction("Options Groups Manager", mw)
mw.connect(action, SIGNAL("triggered()"), og.refresh_and_show)
mw.form.menuTools.addAction(action)




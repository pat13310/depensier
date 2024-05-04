# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'depensesbYcBqU.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDateEdit,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_Depenses(object):
    def setupUi(self, Depenses):
        if not Depenses.objectName():
            Depenses.setObjectName(u"Depenses")
        Depenses.resize(1416, 800)
        self.actionOuvrir = QAction(Depenses)
        self.actionOuvrir.setObjectName(u"actionOuvrir")
        self.actionSauver = QAction(Depenses)
        self.actionSauver.setObjectName(u"actionSauver")
        self.actionCSV = QAction(Depenses)
        self.actionCSV.setObjectName(u"actionCSV")
        self.actionTexte = QAction(Depenses)
        self.actionTexte.setObjectName(u"actionTexte")
        self.actionPDF = QAction(Depenses)
        self.actionPDF.setObjectName(u"actionPDF")
        self.centralwidget = QWidget(Depenses)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(0, 125))
        self.widget.setStyleSheet(u"background-color: rgb(248, 248, 248);\n"
"border: 1px solid rgb(220,220,220);")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.widget_crud = QWidget(self.widget)
        self.widget_crud.setObjectName(u"widget_crud")
        sizePolicy.setHeightForWidth(self.widget_crud.sizePolicy().hasHeightForWidth())
        self.widget_crud.setSizePolicy(sizePolicy)
        self.widget_crud.setMinimumSize(QSize(0, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_crud)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 0, 8, 0)
        self.pushButton = QPushButton(self.widget_crud)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(150, 32))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	background-color: rgb(199, 199, 199);\n"
"	border: 1px solid rgb(99, 99, 99);\n"
"	\n"
"}")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_crud)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(150, 32))
        self.pushButton_2.setStyleSheet(u"QPushButton{\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	background-color: rgb(199, 199, 199);\n"
"	border: 1px solid rgb(99, 99, 99);\n"
"	\n"
"}")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer_4 = QSpacerItem(22, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.pbAdd = QPushButton(self.widget_crud)
        self.pbAdd.setObjectName(u"pbAdd")
        self.pbAdd.setMinimumSize(QSize(150, 32))
        self.pbAdd.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbAdd.setStyleSheet(u"QPushButton{\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	background-color: rgb(199, 199, 199);\n"
"	border: 1px solid rgb(99, 99, 99);\n"
"	\n"
"}")

        self.horizontalLayout_2.addWidget(self.pbAdd)

        self.pbDelete = QPushButton(self.widget_crud)
        self.pbDelete.setObjectName(u"pbDelete")
        self.pbDelete.setMinimumSize(QSize(150, 32))
        self.pbDelete.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbDelete.setStyleSheet(u"QPushButton{\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	background-color: rgb(199, 199, 199);\n"
"	border: 1px solid rgb(99, 99, 99);\n"
"	\n"
"}")

        self.horizontalLayout_2.addWidget(self.pbDelete)

        self.pbModify = QPushButton(self.widget_crud)
        self.pbModify.setObjectName(u"pbModify")
        self.pbModify.setMinimumSize(QSize(150, 32))
        self.pbModify.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbModify.setStyleSheet(u"QPushButton{\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"	background-color: rgb(199, 199, 199);\n"
"	border: 1px solid rgb(99, 99, 99);\n"
"	\n"
"}")

        self.horizontalLayout_2.addWidget(self.pbModify)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget_crud)

        self.widget_filter = QWidget(self.widget)
        self.widget_filter.setObjectName(u"widget_filter")
        sizePolicy.setHeightForWidth(self.widget_filter.sizePolicy().hasHeightForWidth())
        self.widget_filter.setSizePolicy(sizePolicy)
        self.widget_filter.setMinimumSize(QSize(0, 0))
        self.widget_filter.setStyleSheet(u"background-color: rgb(244, 244, 244);\n"
"color: black;")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_filter)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(8, 8, 8, -1)
        self.cmbCategory = QComboBox(self.widget_filter)
        self.cmbCategory.setObjectName(u"cmbCategory")
        self.cmbCategory.setMinimumSize(QSize(200, 24))

        self.horizontalLayout_3.addWidget(self.cmbCategory)

        self.txtDesignation = QLineEdit(self.widget_filter)
        self.txtDesignation.setObjectName(u"txtDesignation")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtDesignation.sizePolicy().hasHeightForWidth())
        self.txtDesignation.setSizePolicy(sizePolicy1)
        self.txtDesignation.setMinimumSize(QSize(100, 24))
        self.txtDesignation.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.txtDesignation)

        self.txtPrice = QLineEdit(self.widget_filter)
        self.txtPrice.setObjectName(u"txtPrice")
        sizePolicy1.setHeightForWidth(self.txtPrice.sizePolicy().hasHeightForWidth())
        self.txtPrice.setSizePolicy(sizePolicy1)
        self.txtPrice.setMinimumSize(QSize(100, 24))
        self.txtPrice.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.txtPrice)

        self.date = QDateEdit(self.widget_filter)
        self.date.setObjectName(u"date")
        self.date.setMinimumSize(QSize(120, 24))
        self.date.setMaximumSize(QSize(200, 16777215))
        self.date.setMaximumDate(QDate(2500, 12, 31))
        self.date.setMinimumDate(QDate(1900, 9, 14))
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate(2024, 4, 28))

        self.horizontalLayout_3.addWidget(self.date)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.widget_filter)


        self.verticalLayout_2.addWidget(self.widget)

        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setObjectName(u"widget1")
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.widget1.setMinimumSize(QSize(0, 40))
        self.widget1.setStyleSheet(u"background-color: rgb(229, 229, 229);\n"
"border: 1px solid rgb(181, 181, 181);")
        self.horizontalLayout_5 = QHBoxLayout(self.widget1)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.widget1)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"border:0")

        self.horizontalLayout_5.addWidget(self.label)

        self.cmbGroup = QComboBox(self.widget1)
        self.cmbGroup.setObjectName(u"cmbGroup")
        self.cmbGroup.setMinimumSize(QSize(130, 24))
        self.cmbGroup.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(168, 168, 168)")

        self.horizontalLayout_5.addWidget(self.cmbGroup)

        self.horizontalSpacer_3 = QSpacerItem(10, 16, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"border: 0px ")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.txtFilter = QLineEdit(self.widget1)
        self.txtFilter.setObjectName(u"txtFilter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.txtFilter.sizePolicy().hasHeightForWidth())
        self.txtFilter.setSizePolicy(sizePolicy2)
        self.txtFilter.setMinimumSize(QSize(228, 24))
        self.txtFilter.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_5.addWidget(self.txtFilter)

        self.pbFilter = QPushButton(self.widget1)
        self.pbFilter.setObjectName(u"pbFilter")
        self.pbFilter.setMinimumSize(QSize(90, 24))
        self.pbFilter.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pbFilter)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.label_3 = QLabel(self.widget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"border:0;")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.pbGraphPoint = QPushButton(self.widget1)
        self.pbGraphPoint.setObjectName(u"pbGraphPoint")
        self.pbGraphPoint.setMinimumSize(QSize(90, 24))
        self.pbGraphPoint.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbGraphPoint.setStyleSheet(u"QPushButton{\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(200, 200, 200);\n"
"}")
        self.pbGraphPoint.setCheckable(True)
        self.pbGraphPoint.setChecked(False)

        self.horizontalLayout_5.addWidget(self.pbGraphPoint)

        self.pbGraphLine = QPushButton(self.widget1)
        self.pbGraphLine.setObjectName(u"pbGraphLine")
        self.pbGraphLine.setMinimumSize(QSize(90, 24))
        self.pbGraphLine.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbGraphLine.setStyleSheet(u"QPushButton{\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(200, 200, 200);\n"
"}")
        self.pbGraphLine.setCheckable(True)
        self.pbGraphLine.setChecked(False)

        self.horizontalLayout_5.addWidget(self.pbGraphLine)

        self.pbGraphHisto = QPushButton(self.widget1)
        self.pbGraphHisto.setObjectName(u"pbGraphHisto")
        self.pbGraphHisto.setMinimumSize(QSize(100, 24))
        self.pbGraphHisto.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbGraphHisto.setStyleSheet(u"QPushButton{\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(200, 200, 200);\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:checked{\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 2px solid rgb(127, 127, 127);\n"
"}")
        self.pbGraphHisto.setCheckable(True)

        self.horizontalLayout_5.addWidget(self.pbGraphHisto)

        self.pbGraphPie = QPushButton(self.widget1)
        self.pbGraphPie.setObjectName(u"pbGraphPie")
        self.pbGraphPie.setMinimumSize(QSize(100, 24))
        self.pbGraphPie.setCursor(QCursor(Qt.PointingHandCursor))
        self.pbGraphPie.setStyleSheet(u"QPushButton{\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(200, 200, 200);\n"
"}")
        self.pbGraphPie.setCheckable(True)

        self.horizontalLayout_5.addWidget(self.pbGraphPie)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addWidget(self.widget1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.tableView = QTableView(self.splitter)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setMinimumSize(QSize(0, 0))
        self.tableView.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.tableView.setAcceptDrops(True)
        self.tableView.setMidLineWidth(0)
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableView.setDragEnabled(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setGridStyle(Qt.PenStyle.DotLine)
        self.tableView.setSortingEnabled(True)
        self.tableView.setCornerButtonEnabled(False)
        self.splitter.addWidget(self.tableView)
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.verticalHeader().setProperty("showSortIndicator", False)
        self.widget_graph = QWidget(self.splitter)
        self.widget_graph.setObjectName(u"widget_graph")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_graph.sizePolicy().hasHeightForWidth())
        self.widget_graph.setSizePolicy(sizePolicy3)
        self.widget_graph.setMinimumSize(QSize(0, 0))
        self.widget_graph.setStyleSheet(u"background-color: rgb(248, 248, 248);\n"
"border: 1px solid rgb(220,220,220);")
        self.horizontalLayout = QHBoxLayout(self.widget_graph)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graphView = QLabel(self.widget_graph)
        self.graphView.setObjectName(u"graphView")
        self.graphView.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.graphView.sizePolicy().hasHeightForWidth())
        self.graphView.setSizePolicy(sizePolicy3)
        self.graphView.setStyleSheet(u"border: 1px solid  rgb(235, 235, 235);")

        self.horizontalLayout.addWidget(self.graphView)

        self.splitter.addWidget(self.widget_graph)

        self.verticalLayout_2.addWidget(self.splitter)

        self.widget_bottom = QWidget(self.centralwidget)
        self.widget_bottom.setObjectName(u"widget_bottom")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_bottom.sizePolicy().hasHeightForWidth())
        self.widget_bottom.setSizePolicy(sizePolicy4)
        self.widget_bottom.setMinimumSize(QSize(0, 50))
        self.widget_bottom.setStyleSheet(u"background-color: rgb(226, 226, 226);")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_bottom)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.txtTotal = QLineEdit(self.widget_bottom)
        self.txtTotal.setObjectName(u"txtTotal")
        self.txtTotal.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(2)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.txtTotal.sizePolicy().hasHeightForWidth())
        self.txtTotal.setSizePolicy(sizePolicy5)
        self.txtTotal.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.txtTotal.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.txtTotal)


        self.verticalLayout_2.addWidget(self.widget_bottom)

        Depenses.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Depenses)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1416, 33))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        self.menuExporter_en = QMenu(self.menuFichier)
        self.menuExporter_en.setObjectName(u"menuExporter_en")
        Depenses.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Depenses)
        self.statusbar.setObjectName(u"statusbar")
        Depenses.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionSauver)
        self.menuFichier.addAction(self.menuExporter_en.menuAction())
        self.menuExporter_en.addAction(self.actionCSV)
        self.menuExporter_en.addAction(self.actionTexte)
        self.menuExporter_en.addAction(self.actionPDF)

        self.retranslateUi(Depenses)

        QMetaObject.connectSlotsByName(Depenses)
    # setupUi

    def retranslateUi(self, Depenses):
        Depenses.setWindowTitle(QCoreApplication.translate("Depenses", u"Mes d\u00e9penses", None))
        self.actionOuvrir.setText(QCoreApplication.translate("Depenses", u"Ouvrir", None))
        self.actionSauver.setText(QCoreApplication.translate("Depenses", u"Sauver", None))
        self.actionCSV.setText(QCoreApplication.translate("Depenses", u"CSV", None))
        self.actionTexte.setText(QCoreApplication.translate("Depenses", u"Texte", None))
        self.actionPDF.setText(QCoreApplication.translate("Depenses", u"PDF", None))
        self.pushButton.setText(QCoreApplication.translate("Depenses", u"Charger", None))
        self.pushButton_2.setText(QCoreApplication.translate("Depenses", u"Sauver", None))
        self.pbAdd.setText(QCoreApplication.translate("Depenses", u"Ajouter", None))
        self.pbDelete.setText(QCoreApplication.translate("Depenses", u"Supprimer", None))
        self.pbModify.setText(QCoreApplication.translate("Depenses", u"Modifier", None))
        self.cmbCategory.setPlaceholderText(QCoreApplication.translate("Depenses", u"cat\u00e9gorie", None))
        self.txtDesignation.setPlaceholderText(QCoreApplication.translate("Depenses", u" lib\u00e9ll\u00e9", None))
        self.txtPrice.setPlaceholderText(QCoreApplication.translate("Depenses", u" prix", None))
        self.label.setText(QCoreApplication.translate("Depenses", u" Grouper par  :", None))
        self.label_2.setText(QCoreApplication.translate("Depenses", u"Filtrer par :", None))
        self.pbFilter.setText(QCoreApplication.translate("Depenses", u"Evaluer", None))
        self.label_3.setText(QCoreApplication.translate("Depenses", u"Type de graphes :", None))
        self.pbGraphPoint.setText(QCoreApplication.translate("Depenses", u"Point", None))
        self.pbGraphLine.setText(QCoreApplication.translate("Depenses", u"Ligne", None))
        self.pbGraphHisto.setText(QCoreApplication.translate("Depenses", u"Histogramme", None))
        self.pbGraphPie.setText(QCoreApplication.translate("Depenses", u"Camembert", None))
        self.graphView.setText("")
        self.menuFichier.setTitle(QCoreApplication.translate("Depenses", u"Fichier", None))
        self.menuExporter_en.setTitle(QCoreApplication.translate("Depenses", u"Exporter en", None))
    # retranslateUi


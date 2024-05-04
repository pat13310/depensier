# Ensure that you import the Ui_Depenses class from the correct module
import re
import sys

from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QTableView, QPushButton

from ColonneType import ColonneType, GraphType
from PandasModel import PandasModel
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
import pandas as pd

register_matplotlib_converters()

from io import BytesIO
from PandasTreeModel import PandasTreeModel
from Ui_Depenses import Ui_Depenses


def is_decimal_or_integer(s):
    return bool(re.match(r'^-?\d+(\.\d+)?$', s))


class DepensesMain(QMainWindow, Ui_Depenses):
    def __init__(self):
        super().__init__()
        # Set up the UI
        self.matplot = None
        self.row = None
        self.setupUi(self)
        # connexion aux slots
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pbAdd.clicked.connect(self.on_add)
        self.pbModify.clicked.connect(self.on_modify)
        self.pbDelete.clicked.connect(self.on_delete)
        self.tableView.horizontalHeader().sectionClicked.connect(self.on_colonne_clicked)
        self.tableView.clicked.connect(self.on_table_clicked)
        self.cmbGroup.currentIndexChanged.connect(self.on_group)
        self.pbFilter.clicked.connect(self.on_filter)
        self.actionOuvrir.triggered.connect(self.load_data)
        self.actionSauver.triggered.connect(self.save_data)

        self.pbGraphPoint.clicked.connect(lambda: self.set_graph_type(self.pbGraphPoint, GraphType.POINT))
        self.pbGraphLine.clicked.connect(lambda: self.set_graph_type(self.pbGraphLine, GraphType.LINE))
        self.pbGraphHisto.clicked.connect(lambda: self.set_graph_type(self.pbGraphHisto, GraphType.BAR))
        self.pbGraphPie.clicked.connect(lambda: self.set_graph_type(self.pbGraphPie, GraphType.PIE))

        self.model = QStandardItemModel(1, 4)
        self.init_table()
        self.model = PandasModel()
        self.model.errorOccurred.connect(self.on_filter_error)
        self.tree_model = PandasTreeModel()
        self.selected_item = None

        self.date.setDate(QDate.currentDate())
        self.date.setMaximumDate(QDate.currentDate())
        self.date.dateChanged.connect(self.on_date)
        self.graph_type: GraphType = GraphType.LINE
        self.column_type: ColonneType = ColonneType.SANS
        #
        self.pbGraphLine.setStyleSheet("background-color: rgb(120, 120, 120); color:white;")
        self.pbGraphLine.setChecked(True)
        self.widget_crud.setVisible(False)

    def init_table(self):
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.setSelectionMode(QTableView.SingleSelection)

    def on_colonne_clicked(self, index):
        order = self.tableView.horizontalHeader().sortIndicatorOrder()
        self.model.sort(index, order)
        self.refresh_table()

    def set_headers(self):
        if self.column_type != ColonneType.ANNEE_DETAILS.value:
            self.tableView.setColumnWidth(1, 110)
            self.tableView.setColumnWidth(2, 155)
            self.tableView.setColumnWidth(3, 100)
            self.tableView.setMinimumSize(QSize(600, 300))
            self.widget_graph.setVisible(True)

        else:
            count = len(self.model.get_data().columns)
            for i in range(len(self.model.get_data().columns)):
                self.tableView.setColumnWidth(i, 120)

            self.widget_graph.setVisible(False)
            self.tableView.setMinimumSize(QSize(1000, 300))

    def load_csv(self, file: str):
        self.model.load(file)
        self.refresh_table()
        self.set_headers()
        # On renseigne le combo box
        self.cmbGroup.clear()
        self.cmbCategory.clear()
        categories = self.model.get_data()["Catégorie"].unique()
        self.cmbCategory.addItems(categories)

        for column in ColonneType:
            self.cmbGroup.addItem(column.name, column.value)

    def refresh_table(self):
        # Calcul la somme avec pandas
        prix_total = self.model.get_data()['Prix'].sum()
        # Met à jour le modèle
        self.tableView.setModel(self.model)
        self.refresh_counters()

    def refresh_counters(self):
        if self.column_type == ColonneType.ANNEE_DETAILS.value:
            return
        prix_total = self.model.get_data()['Prix'].sum()
        self.txtTotal.setText(
            f"Total des dépenses : {prix_total:.2f} €   -  Nombre d'éléments : {len(self.model.get_data())}")
        self.txtTotal.setStyleSheet("font: bold;")

    def on_pushButton_clicked(self):
        # Handle the button click event
        self.load_csv("donnees.csv")

    def on_table_clicked(self, index):
        # index est de type QModelIndex
        self.row = index.row()  # Récupère l'indice de la ligne cliquée

        # Assurez-vous que le modèle est un QAbstractTableModel ou dérivé
        model = self.tableView.model()

        # Récupérer les données de toute la ligne
        row_data = [model.data(model.index(self.row, col)) for col in range(model.columnCount())]

        # Stocker les données récupérées ou les utiliser selon vos besoins
        self.selected_item = row_data

        # Pour déboguer ou afficher les informations collectées
        # print("Complete Row Data:", self.selected_item)
        self.show_row()

    def is_valide_field(self):
        if self.model.get_data() is None:
            return False

        if self.txtPrice.text().strip() == "":
            return False

        if len(self.txtDesignation.text().strip()) == 0:
            return False

        if not is_decimal_or_integer(self.txtPrice.text()):
            return False

        if is_decimal_or_integer(self.txtDesignation.text()):
            return False

        return True

    def on_add(self):

        if not self.is_valide_field():
            return

        date = self.date.text()
        category = "Texte"
        libelle = self.txtDesignation.text()
        price = float(self.txtPrice.text())

        row = {"Date": date, "Catégorie": category, "Libellé": libelle, "Prix": price}
        self.model.addRow(row=row)
        # Faites défiler jusqu'au bas du QTableView
        self.tableView.scrollToBottom()
        self.refresh_counters()

    def on_modify(self):

        if self.selected_item and self.is_valide_field():
            modify_value = {"Date": self.date.text(),
                            "Catégorie": self.cmbCategory.currentText(),
                            "Libellé": self.txtDesignation.text(),
                            "Prix": float(self.txtPrice.text())
                            }
            self.model.update(self.row, modify_value)
            self.refresh_counters()

    def on_delete(self):
        if self.selected_item:
            reply = QMessageBox.question(self, 'Confirmation de la suppression',
                                         f"Etes-vous sûr de supprimer cet enregistrement  {self.selected_item}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.model.removeRow(self.row)
                self.tableView.setModel(None)
                self.tableView.setModel(self.model)
                self.selected_item = None
                self.row = -1
                self.refresh_counters()
        else:
            QMessageBox.information(self, 'Information', 'Pas de sélection.')

    def show_row(self):
        if self.model.is_group:
            return
        if self.selected_item:
            self.txtDesignation.setText(self.selected_item[2])
            self.txtPrice.setText(self.selected_item[3])
            selected_category = self.selected_item[1]
            # On vérifie que le texte existe bien dans la liste
            if selected_category in [self.cmbCategory.itemText(i) for i in range(self.cmbCategory.count())]:
                self.cmbCategory.setCurrentText(selected_category)

    def on_group(self, index):
        if self.model is None:
            return
        self.column_type = self.cmbGroup.currentData(Qt.UserRole)

        if self.column_type == ColonneType.SANS.value:
            self.widget_crud.setVisible(True)
        else:
            self.widget_crud.setVisible(False)

        self.txtFilter.setText("")

        if self.column_type == ColonneType.SANS.value:
            self.model.to_original()
        elif self.column_type == ColonneType.DATE.value:
            self.model.group_by(0)
        elif self.column_type == ColonneType.CATEGORIE.value:
            self.model.group_by(1)
        elif self.column_type == ColonneType.LIBELLE.value:
            self.model.group_by(2)
        elif self.column_type == ColonneType.MOIS.value:
            self.model.per_month()
        elif self.column_type == ColonneType.ANNEE.value:
            self.model.per_year()
        elif self.column_type == ColonneType.ANNEE_DETAILS.value:
            data = self.model.get_data()

            self.model.pivot(data, values="Prix", index="Année", columns="Catégorie")

        self.set_headers()
        self.show_graphview(self.cmbGroup.currentData(Qt.UserRole))
        self.refresh_counters()

    def on_filter(self):
        # if len(self.txtFilter.text().strip()) == 0:
        #    self.model.to_original()
        # else:
        self.model.filter(self.txtFilter.text())

        self.show_graphview(self.cmbGroup.currentData(Qt.UserRole))
        self.refresh_counters()

    def on_filter_error(self, err):
        QMessageBox.information(self, 'Information', err)

    def on_date(self, new_date):
        pass

    def show_graphview(self, sort):

        data = self.model.get_data()

        plt.figure(figsize=(8, 4))  # Taille du graphe
        ax = plt.gca()
        plt.subplots_adjust(bottom=0.3)  # Ajuster la marge inférieure

        if self.graph_type & GraphType.LINE:
            plt.xticks(rotation=45, ha='right')  # Rotation à 45 degrés et alignement à droite
            plt.rc('xtick', labelsize=6)
            plt.rc('ytick', labelsize=7)

        if self.graph_type & GraphType.POINT:
            plt.xticks(rotation=45, ha='right')  # Rotation à 45 degrés et alignement à droite
            plt.rc('xtick', labelsize=6)
            plt.rc('ytick', labelsize=7)

        if sort == ColonneType.DATE.value:
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.DATE.value)
                plt.ylabel('Prix')
                ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))  # Limiter le nombre de marqueurs de date
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))  # Format de date
                self.draw_graph(data, ColonneType.DATE, self.graph_type)
            else:
                df = pd.DataFrame(data)
                df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
                self.draw_graph(df, ColonneType.DATE, self.graph_type)

        elif sort == ColonneType.CATEGORIE.value:
            self.draw_graph(data, ColonneType.CATEGORIE, self.graph_type)
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.CATEGORIE.value)
                plt.ylabel('Prix')

        elif sort == ColonneType.LIBELLE.value:
            self.draw_graph(data, ColonneType.LIBELLE, self.graph_type)
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.LIBELLE.value)
                plt.ylabel('Prix')

        elif sort == ColonneType.MOIS.value:
            df = pd.DataFrame(data)
            df['Mois'] = pd.to_datetime(df['Mois'].dt.to_timestamp())
            self.draw_graph(df, ColonneType.MOIS, self.graph_type)
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.MOIS.value)
                plt.ylabel('Prix')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))  # Format de date
            else:
                df = pd.DataFrame(data)
                df['Mois'] = df['Mois'].dt.strftime('%m-%Y')
                self.draw_graph(df, ColonneType.MOIS, self.graph_type)

        elif sort == ColonneType.ANNEE.value:
            self.draw_graph(data, ColonneType.ANNEE, self.graph_type)
            plt.xlabel(ColonneType.ANNEE.value)
            if not self.graph_type & GraphType.PIE:
                plt.ylabel('Prix')
                plt.xticks(rotation=0, ha='center')

        elif sort == ColonneType.SANS.value:
            plt.figure(figsize=(4, 4))

        elif sort == ColonneType.ANNEE_DETAILS.value:
            plt.figure(figsize=(2, 2))

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue(), 'PNG')
        self.graphView.setPixmap(pixmap)

    def draw_graph(self, data, colonne_type: ColonneType, graph_type: GraphType):
        if self.graph_type.value & GraphType.BAR.value:
            # data.plot(kind='bar', color='skyblue')
            plt.bar(data[colonne_type.value], data["Prix"], color='skyblue')
            plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
            plt.grid(True, linestyle='--', alpha=0.6)  # Ajout de grille pour une meilleure visibilité des valeurs

        if self.graph_type.value & GraphType.LINE.value:
            plt.plot(data[colonne_type.value], data['Prix'])
        if self.graph_type.value & GraphType.POINT.value:
            plt.scatter(data[colonne_type.value], data['Prix'])

        if self.graph_type.value & GraphType.PIE.value:
            plt.figure(figsize=(5, 5))
            plt.pie(data['Prix'], labels=data[colonne_type.value], autopct='%1.1f%%', startangle=180)
            # plt.title('Répartition des dépenses par catégorie')
            plt.axis('equal')  # Assure que le pie chart est un cercle

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Ouvrir le fichier dépenses", "",
                                                   "Fichier CSV (*.csv);;Fichier JSON (*.json);;Fichier Excel (*.xlsx)")
        if file_name:
            self.load_csv(file_name)

    def save_data(self):
        # Ouvre une boîte de dialogue pour sauvegarder un fichier
        file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le fichier dépenses")
        if file_name:
            self.model.save_to_csv(file_name)
            print(f"Fichier sauvegardé : {file_name}")
            # Vous pouvez ici ajouter la logique pour sauvegarder les données dans le fichier

    def set_graph_type(self, button, graph_type):

        self.graph_type = GraphType.NONE
        if self.pbGraphPoint.isChecked():
            self.graph_type |= GraphType.POINT
            self.pbGraphPoint.setStyleSheet("background-color: rgb(120, 120, 120); color:white;")
        else:
            self.pbGraphPoint.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")

        if self.pbGraphLine.isChecked():
            self.graph_type |= GraphType.LINE
            self.pbGraphLine.setStyleSheet("background-color: rgb(120, 120, 120); color:white;")
        else:
            self.pbGraphLine.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")

        if self.pbGraphHisto.isChecked():
            self.graph_type |= GraphType.BAR
            self.pbGraphHisto.setStyleSheet("background-color: rgb(120, 120, 120); color:white;")
        else:
            self.pbGraphHisto.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")

        if self.pbGraphPie.isChecked():
            self.graph_type = GraphType.PIE
            self.pbGraphPoint.setChecked(False)
            self.pbGraphLine.setChecked(False)
            self.pbGraphHisto.setChecked(False)
            self.pbGraphPie.setStyleSheet("background-color: rgb(120, 120, 120); color:white;")
            self.pbGraphLine.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")
            self.pbGraphPoint.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")
            self.pbGraphHisto.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")
        else:
            self.pbGraphPie.setStyleSheet("background-color: rgb(200, 200, 200); color:black;")

        self.show_graphview(self.cmbGroup.currentData(Qt.UserRole))
        self.refresh_counters()


# To run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DepensesMain()
    main_window.show()
    sys.exit(app.exec())

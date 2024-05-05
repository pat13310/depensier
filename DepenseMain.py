# Ensure that you import the Ui_Depenses class from the correct module
import locale
import os
import re
import sys

from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QTableView, QPushButton

from ColonneType import ColonneType, GraphType, FileFormatType
from PandasModel import PandasModel
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
import pandas as pd

register_matplotlib_converters()

from io import BytesIO
from PandasTreeModel import PandasTreeModel
from Ui_Depenses import Ui_Depenses


def is_decimal_or_integer(s: str):
    """ Vérifie si un nombre est un entier ou décimal.

        Args :
            s(str) : expression à vérifier
    """

    return bool(re.match(r'^-?\d+(\.\d+)?$', s))


class DepensesMain(QMainWindow, Ui_Depenses):

    def __init__(self):
        """
        Constructeur de la classe DepensesMain
        On initialise les variables et on connecte les évènements des objets
        """
        super().__init__()
        # Set up the UI
        self.file_base = None
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
        self.actionCSV.triggered.connect(lambda: self.export_data(FileFormatType.CSV))
        self.actionJSON.triggered.connect(lambda: self.export_data(FileFormatType.JSON))
        self.actionExcel.triggered.connect(lambda: self.export_data(FileFormatType.EXCEL))

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

        locale.setlocale(locale.LC_TIME, 'fr_FR')  # On localise sur la France

    def init_table(self):
        """
        Définit la sélection sur la ligne entière (Vue)
        """
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.setSelectionMode(QTableView.SingleSelection)

    def on_colonne_clicked(self, index):
        """
            Fait le trie ascendant ou descendant quand on clique sur la colonne
        """
        order = self.tableView.horizontalHeader().sortIndicatorOrder()
        self.model.sort(index, order)
        self.refresh_table()

    def set_headers(self):
        """
        Définit la liste des colonnes dans la table
        """
        if self.column_type != ColonneType.ANNEE_DETAILS.value and self.column_type != ColonneType.RESUME.value:
            self.tableView.setColumnWidth(1, 110)
            self.tableView.setColumnWidth(2, 155)
            self.tableView.setColumnWidth(3, 100)
            self.tableView.setMinimumSize(QSize(600, 300))
            self.widget_graph.setVisible(True)

        elif self.column_type == ColonneType.RESUME.value:
            for i in range(len(self.model.get_data().columns)):
                self.tableView.setColumnWidth(i, 120)
                self.widget_graph.setVisible(False)
                self.tableView.setMinimumSize(QSize(1000, 300))

        else:
            for i in range(len(self.model.get_data().columns)):
                self.tableView.setColumnWidth(i, 120)

            self.widget_graph.setVisible(False)
            self.tableView.setMinimumSize(QSize(1000, 300))

    def load_file(self, file: str):
        """
        Charge le fichier dépense

        Args :
            file (str) : le fichier
        """
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
        """ Met à jour les informations le model avec la vue (tableView)
        et rafraîchit les informations du prix et des éléments
        """
        # Calcul la somme avec pandas
        # Met à jour le modèle
        self.tableView.setModel(self.model)
        self.refresh_counters()

    def refresh_counters(self):
        """ Met à jour les informations sur le prix et le nombre d'éléments"""
        if self.column_type == ColonneType.ANNEE_DETAILS.value:
            return
        prix_total = self.model.get_data()['Prix'].sum()
        self.txtTotal.setText(
            f"Total des dépenses : {prix_total:.2f} €   -  Nombre d'éléments : {len(self.model.get_data())}")
        self.txtTotal.setStyleSheet("font: bold;")

    def on_pushButton_clicked(self):
        """Chargement ou rechargement du model dans la vue"""
        self.load_file("donnees.csv")

    def on_table_clicked(self, index):
        """ Récupère la ligne sélectionnée (Vue)
        et envoie les informations dans les champs de saisie """
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
        """ vérifie que les champs sont valides """
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
        """ Ajoute la ligne dans le dataframe et la table (model) """
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
        """ Modifie la ligne dans le dataframe et la table si sélectionné"""
        if self.selected_item and self.is_valide_field():
            modify_value = {"Date": self.date.text(),
                            "Catégorie": self.cmbCategory.currentText(),
                            "Libellé": self.txtDesignation.text(),
                            "Prix": float(self.txtPrice.text())
                            }
            self.model.update(self.row, modify_value)
            self.refresh_counters()

    def on_delete(self):
        """ Supprime la ligne du dataframe et la table si confirmation de l'utilisateur"""
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
        """ Affiche les données dans les champs de saisie """
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
        """ Groupe le modèle et affiche le résultat
                   dans la vue (Table + Graphe)
        """
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
        """ Filtre le modèle et affiche le résultat
            dans la vue (Table + Graphe)
        """
        self.model.filter(self.txtFilter.text())
        self.show_graphview(self.cmbGroup.currentData(Qt.UserRole))
        self.refresh_counters()

    def on_filter_error(self, err):
        """ Affiche les erreurs si le filtre n'est pas correcte

            Args :
                err (str) : description de l'erreur
        """
        QMessageBox.information(self, 'Information', err)

    def on_date(self, new_date):
        pass

    def show_graphview(self, sort):
        """ Affiche le graphe et ajuste les paramètres des axes suivant les types de graphes"""

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
                self.draw_graph(data, ColonneType.DATE)
            else:
                df = pd.DataFrame(data)
                df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
                self.draw_graph(df, ColonneType.DATE)

        elif sort == ColonneType.CATEGORIE.value:
            self.draw_graph(data, ColonneType.CATEGORIE)
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.CATEGORIE.value)
                plt.ylabel('Prix')

        elif sort == ColonneType.LIBELLE.value:
            self.draw_graph(data, ColonneType.LIBELLE)
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.LIBELLE.value)
                plt.ylabel('Prix')

        elif sort == ColonneType.MOIS.value:
            df = pd.DataFrame(data)
            df['Mois'] = pd.to_datetime(df['Mois'].dt.to_timestamp())
            self.draw_graph(df, ColonneType.MOIS)
            if not self.graph_type & GraphType.PIE:
                plt.xlabel(ColonneType.MOIS.value)
                plt.ylabel('Prix')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))  # Format de date
            else:
                df = pd.DataFrame(data)
                df['Mois'] = df['Mois'].dt.strftime('%m-%Y')
                self.draw_graph(df, ColonneType.MOIS)

        elif sort == ColonneType.ANNEE.value:
            self.draw_graph(data, ColonneType.ANNEE)
            plt.xlabel(ColonneType.ANNEE.value)
            if not self.graph_type & GraphType.PIE:
                plt.ylabel('Prix')
                plt.xticks(rotation=0, ha='center')

        elif sort == ColonneType.SANS.value:
            pass
        elif sort == ColonneType.RESUME.value:
            self.model.resume()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue(), 'PNG')
        self.graphView.setPixmap(pixmap)
        plt.close('all')

    def draw_graph(self, data, colonne_type: ColonneType):
        """ Affiche les graphes

            Args :
                data (DataFrame) : données pour afficher les graphes

                colonne_type (ColonneType) : le type de colonne à traiter
        """

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
            plt.axis('equal')  # Assure que le 'pie chart' est un cercle

    def load_data(self):
        """ Charge le fichier dépense à partir de la boite de dialogue"""
        file_name, _ = QFileDialog.getOpenFileName(None, "Ouvrir le fichier dépenses", "",
                                                   "Fichier CSV (*.csv);;Fichier JSON (*.json);;Fichier Excel (*.xlsx)")
        if file_name:
            self.load_file(file_name)
            self.file_base = os.path.basename(file_name).split(".")
            self.file_base = self.file_base[0]

    def save_data(self):
        """
            Sauvegarde le fichier dépense à partir de la boite de dialogue

        """
        # Ouvre une boîte de dialogue pour sauvegarder un fichier
        file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le fichier dépenses")
        if file_name:
            self.model.save(file_name)
            self.file_base = os.path.basename(file_name).split(".")
            self.file_base = self.file_base[0]
            print(f"Fichier sauvegardé : {file_name}")

    def export_data(self, formatType: FileFormatType):
        if formatType == FileFormatType.CSV:
            self.model.save(f"{self.file_base}.csv")
        elif formatType == FileFormatType.JSON:
            self.model.save(f"{self.file_base}.json")
        elif formatType == FileFormatType.EXCEL:
            self.model.save(f"{self.file_base}.xlsx")

    def set_graph_type(self, button, graph_type):
        """ Gestion des boutons pour définir le type ou types de graphes (Vue)
        """
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

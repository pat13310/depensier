import locale

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, Signal
from pandas import DataFrame

""" Classe PandasModel

   Args :
       QAbstractTableModel : hérite de la classe QAbstractTableModel
   """


class PandasModel(QAbstractTableModel):
    """
        Variables de la classe PandasModel :
            errorOccurred (Signal) : Définit un signal qui envoie un message d'erreur
    """
    errorOccurred = Signal(str)  # Définit un signal qui envoie un message d'erreur

    def __init__(self, data=None):
        """ Constructeur pour PandasModel

        Args :
            data (DataFrame) : DataFrame (optionnel) initialisé à None
        """
        super(PandasModel, self).__init__()
        self._data_original: DataFrame = data  # _data_original est le dataFrame d'origine (la référence)
        self._data: DataFrame = data  # _data est un DataFrame de travail courant (change en cours)
        self._data_filter: DataFrame = data  # data_filter est un DataFrame de filtre (garde l'état avant le filter)
        self.is_group: bool = False
        locale.setlocale(locale.LC_TIME, 'fr_FR')  # On localise sur la France
        if self._data is not None:
            for index, name in enumerate(self._data.columns):
                self.setHeaderData(index, Qt.Horizontal, name)

    def rowCount(self, parent=None):
        """Compte the nombre of lignes

        Args :
            parent (QModelIndex) le pointeur

        Returns : le nombre de lignes

        """
        return self._data.shape[0]

    def columnCount(self, parent=None):
        """Compte the nombre de colonnes

        Args :
            parent (QModelIndex) le pointeur

        Returns : le nombre de colonnes
        """

        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """ Définit les lignes à afficher suivant l'index

        Args :
            index (QModelIndex) : l'index de la cellule
            role : (Qt.DisplayRole) donnée de type textuelle pour l'affichage

        Returns :
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.format_display_data(index)

        if role == Qt.TextAlignmentRole:
            return self.format_text_alignment(index)

        return None

    def format_display_data(self, index):
        value = self._data.iloc[index.row(), index.column()]
        column_name = self._data.columns[index.column()]

        if 'Mois' in column_name and isinstance(value, pd.Period):
            return value.strftime('%B %Y').capitalize()

        if 'Date' in column_name and isinstance(value, pd.Timestamp):
            return value.strftime('%d/%m/%Y')

        if isinstance(value, float):
            return "{:.2f}".format(value)

        return str(value)

    def format_text_alignment(self, index):
        # column_name = self._data.columns[index.column()]
        value = self._data.iloc[index.row(), index.column()]
        if isinstance(value, float):
            return Qt.AlignRight | Qt.AlignVCenter
        return Qt.AlignLeft | Qt.AlignVCenter  # ou une autre valeur par défaut pour l'alignement

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(self._data.index[section])
        return None

    def load(self, file_path):
        """Chargement du fichier csv et intégration du dataframe dans le modèle

        Args :
            file_path (str) : le chemin du fichier de données (csv, json, xlsx)

        Returns : None
        """
        # On charge le dataframe à partir du fichier csv
        # et même temps, on fige l'affichage
        self.is_group = False
        self.layoutAboutToBeChanged.emit()
        if file_path.endswith('.csv'):
            self._data = pd.read_csv(file_path)
        if file_path.endswith('.json'):
            self._data = pd.read_json(file_path)
        if file_path.endswith('.xlsx'):
            self._data = pd.read_excel(file_path)

        # On a converti en objet dateTime pour gérer correctement les dates
        self._data['Date'] = pd.to_datetime(self._data['Date'], format='%d/%m/%Y')
        # Juste la date pas les heures (ptdr)
        self._data_filter=self._data.copy(deep=True)
        self.layoutChanged.emit()
        self._data_original = self._data.copy(True)  # on copie même les données

        for index, name in enumerate(self._data.columns):
            self.setHeaderData(index, Qt.Horizontal, name)

    def save(self, file_path):
        """On sauve toutes les informations s
        auf les index

        Args :
            file_path (str) : chemin du fichier csv

        Returns : None
        """
        if file_path.endswith('.csv'):
            self._data_original.to_csv(file_path, index=False)

        elif file_path.endswith('.json'):
            self._data_original.to_json(file_path, index=False)

        elif file_path.endswith('.xlsx'):
            self._data_original.to_excel(file_path, index=False)
        else:
            self.errorOccurred.emit("Format non supporté")

    def addRow(self, row, parent=QModelIndex()):
        """
                Ajout d'une ligne dans le dataframe et le modèle à la fois

                Args :
                    row (dictionary) : données à insérer
                    parent (QModelIndex) : l'index de la cellule

                Returns : bool
                """
        self.beginInsertRows(parent, self.rowCount(parent), self.rowCount(parent))
        new_data = pd.DataFrame([row], columns=self._data.columns)
        self._data = pd.concat([self._data, new_data], ignore_index=True)
        self._data_original = self._data.copy(True)
        self.endInsertRows()

    def update(self, row_index, new_values):
        """
               Mise à jour d'une ligne dans le dataframe et le modèle

               Args :
                   row_index : l'index de la ligne
                   modify_value (dictionnaire) : nouvelle valeur (DataFrame) de la ligne dans le dataframe

               Returns : bool
               """
        # Vérifier que l'index de la ligne est valide
        if row_index < 0 or row_index >= self.rowCount():
            return False

        # Mettre à jour les valeurs dans le DataFrame
        for column_name, new_value in new_values.items():
            self._data.at[row_index, column_name] = new_value

        # Mettre à jour la vue
        top_left = self.index(row_index, 0)
        bottom_right = self.index(row_index, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right)
        self._data_original = self._data.copy(True)
        return True

    def removeRow(self, row, parent=QModelIndex()):
        """
        Suppression d'une ligne dans un DataFrame et dans le Modèle

        Args :
            row : numéro de la ligne dans un DataFrame
            parent : pointeur pour définir l'enregistrement sur lequel on pointe

        Returns : bool

        """
        self.beginRemoveRows(parent, row, row)  # Signaler le début de la suppression
        # Supprimer la ligne et on redéfinit les index
        self._data = self._data.drop(self._data.index[row], axis=0).reset_index(drop=True)
        self._data_original = self._data.copy(True)
        self.endRemoveRows()  # Signaler la fin de la suppression
        return True

    def sort(self, col, ascending=Qt.AscendingOrder):
        """ Tri du DataFrame en fonction de la colonne
            et on définit un ordre ascendant ou descendant.

        Args :
            col (int) : colonne
            ascending (bool, optional) : tri ascendant ou descendant

        Returns : None
        """

        if isinstance(col, int):  # Si 'col' est un index de colonne
            col = self._data.columns[col]  # Convertir l'index en nom de colonne

        sort = True if ascending == Qt.AscendingOrder else False

        self.layoutAboutToBeChanged.emit()  # Préparer la vue pour les changements
        # Trier les données et réinitialiser l'index
        self._data = self._data.sort_values(by=col, ascending=sort).reset_index(drop=True)
        self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def group_by(self, col):
        """
        Tri du DataFrame par group en fonction de la colonne

        Args :
            col (int) : index (ou nom de la colonne)

        Returns :
            le dataframe regroupé par la colonne sélectionnée et on affiche le prix par colonne
        """
        self._data = None
        self._data = self._data_original.copy(True)
        self.is_group = True
        if isinstance(col, int):  # Si 'col' est un index de colonne
            col = self._data.columns[col]  # Convertir l'index en nom de colonne

        self.layoutAboutToBeChanged.emit()
        self._data = self._data.groupby(col)['Prix'].sum().reset_index()
        self._data_filter = self._data.copy(deep=True)
        self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def filter(self, expression):
        """
        Filtre les données selon l'expression donnée.

        Args :
            expression (str) : Une expression conditionnelle pour filtrer les données, ex., 'Prix > 20'.

        """
        self.layoutAboutToBeChanged.emit()  # Préparer la vue pour les changements
        try:
            self._data = self._data_filter
            if len(expression) == 0:
                return
            # Appliquer le filtre
            self._data = self._data.query(expression)
            #self._data_filter = self._data.copy(deep=True)
        except Exception as e:
            self._data = self._data_original  # Restaurer les données originales en cas d'erreur
            self.errorOccurred.emit(f"Erreur lors du filtrage : {e}")
        finally:
            self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def get_data(self):
        """ Retourne le DataFrame inclut dans le modèle
        Args :

        Returns : le dataframe
        """
        return self._data

    def to_original(self):
        """
        Restaure et affiche les données originelles chargées lors de :
            - load_csv
            - constructeur

        Args :

        Return : None
        """
        self.is_group = False
        if self._data_original is not None:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data_original.copy(True)
            self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def per_month(self):
        """
            Affiche la vue en fonction des mois
        """
        self._data = None
        self._data = self._data_original.copy(True)
        self.is_group = True
        self.layoutAboutToBeChanged.emit()
        # Extraire le mois de la date
        self._data['Mois'] = self._data['Date'].dt.to_period('M')
        # Grouper par 'Mois' et calculer la somme des 'Prix'
        self._data = self._data.groupby('Mois')['Prix'].sum().reset_index()
        self._data_filter = self._data.copy(deep=True)
        self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def per_year(self):
        """
            Affiche la vue en fonction des années
        """
        self._data = None
        self._data = self._data_original.copy(True)
        self.is_group = True

        self.layoutAboutToBeChanged.emit()

        # Extraire l'année de la date
        self._data['Année'] = self._data['Date'].dt.to_period('Y')

        # Grouper par 'Année' et calculer la somme des 'Prix'
        self._data = self._data.groupby('Année')['Prix'].sum().reset_index()

        # Convertir 'Année' de Period à string pour un affichage plus convivial
        self._data['Année'] = self._data['Année'].astype(str)
        self._data_filter = self._data.copy(deep=True)

        self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def pivot(self, data, values, index, columns, agg="sum"):
        """ Pivot pour agencer et afficher les données de manière plus lisible

            Args :
                data (DataFrame) : DataFrame contenant le dataframe (optionnel)
                values (Series) : détermine les valeurs du DataFrame
                index (str) : nom de la colonne qui définit l'index de notre DataFrame
                columns (str) : nom de la colonne qui définit les colonnes de notre DataFrame
                agg (str) : fonction aggregation pour calculer à partir des valeurs
                par exemple la somme, la moyenne, le nombre ...

            Returns : None
        """
        self.layoutAboutToBeChanged.emit()
        if data is not None:
            data = self._data_original.copy(True)
        try:
            # Préparation des données
            data = pd.DataFrame(data)
            data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
            data['Année'] = data['Date'].dt.year
            # Application de la table pivot
            self._data = data.pivot_table(values=values, index=index, columns=columns, aggfunc=agg)
            # On rajoute la colonne Dépense annuelle
            self._data['Dépense annuelle '] = self._data.sum(axis=1)
            self._data_filter = self._data.copy(deep=True)
        except Exception as e:
            print("Error in processing pivot table:", e)
        self.layoutChanged.emit()  # Signaler que les modifications sont terminées

    def resume(self):
        self.layoutAboutToBeChanged.emit()
        self._data = self._data_original.copy(True)

        # self._data['Prix_Max'] = self._data.groupby('Catégorie')['Prix'].transform('max')
        # self._data['Prix_Min'] = self._data.groupby('Catégorie')['Prix'].transform('min')
        # self._data['Prix_Moyen'] = self._data.groupby('Catégorie')['Prix'].transform('mean')

        # Effectuer les calculs d'agrégation une seule fois et les stocker
        agg_data = self._data.groupby('Catégorie')['Prix'].agg(['max', 'min', 'mean'])
        agg_data.columns = ['Prix_Max', 'Prix_Min', 'Prix_Moyen']

        # Joindre les résultats d'agrégation avec les données originales sans duplication inutile
        self._data = self._data.join(agg_data, on='Catégorie')

        self._data_filter = self._data.copy(deep=True)

        self.layoutChanged.emit()  # Signaler que les modifications sont terminées

from PySide6.QtCore import QModelIndex, QAbstractItemModel, Qt
import pandas as pd


class PandasTreeModel(QAbstractItemModel):
    def __init__(self, data=None):
        super().__init__()
        self.df = data
        self.categories = None

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():  # Catégories
            if row < len(self.categories) and column == 0:
                return self.createIndex(row, column, self.categories.iloc[row])
            return QModelIndex()
        else:  # Items under categories
            category = parent.internalPointer()
            filtered_df = self.df[self.df['Catégorie'] == category['Catégorie']]
            if row < len(filtered_df):
                return self.createIndex(row, column, filtered_df.iloc[row])
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        item = index.internalPointer()
        if 'Total' in item:
            return QModelIndex()
        filtered_df = self.df[self.df['Catégorie'] == item['Catégorie']]
        if not filtered_df.empty:
            return self.createIndex(0, 0, {'Catégorie': item['Catégorie'], 'Total': True})
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():  # Root
            return len(self.categories)
        if 'Total' in parent.internalPointer():
            filtered_df = self.df[self.df['Catégorie'] == parent.internalPointer()['Catégorie']]
            return len(filtered_df)
        return 0

    def columnCount(self, parent=QModelIndex()):
        return 2  # For example, 'Libellé' and 'Prix'

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        item = index.internalPointer()
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return item['Libellé'] if 'Libellé' in item else item['Catégorie']
            elif index.column() == 1:
                return item['Prix'] if 'Prix' in item else None
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Libellé" if section == 0 else "Prix"
        return None

    def load_csv(self, path):
        self.df = pd.read_csv(path)
        self.categories = self.df.groupby('Catégorie').sum().reset_index()

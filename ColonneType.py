from enum import Enum, Flag


class ColonneType(Enum):
    SANS = 'Sans'
    DATE = 'Date'
    CATEGORIE = 'Catégorie'
    LIBELLE = 'Libellé'
    MOIS = 'Mois'
    ANNEE = 'Année'
    ANNEE_DETAILS = "Année en détail"
    RESUME = "Résumé"


class GraphType(Flag):
    NONE = 0
    BAR = 1
    LINE = 2
    POINT = 4
    PIE = 8


class FileFormatType(Enum):
    JSON = 'JSON'
    CSV = 'CSV'
    EXCEL = 'Excel'
    OTHER = 'Other'

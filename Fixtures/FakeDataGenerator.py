import csv
from faker import Faker
import random
from datetime import datetime, timedelta


class FakeDataGenerator:
    def __init__(self, locale='fr_FR'):
        self.fake = Faker(locale)
        self.categories = {
            "Nourriture": ["Pommes", "Pain", "Pâtes", "Fromage", "Pizza"],
            "Transport": ["Ticket de Métro", "Billet de Bus", "Taxi", "Location Voiture"],
            "Loisirs": ["Cinéma", "Concert", "Musée", "Parc", "Bibliothèque"],
            "Électronique": ["Smartphone", "Tablette", "PC Portable", "Casque Audio"],
            "Vêtements": ["T-shirt", "Pantalon", "Chaussures", "Veste"],
            "Santé": ["Médicaments", "Consultation médicale", "Vitamines", "Équipement de sport"],
            "Services": ["Coiffure", "Plomberie", "Nettoyage", "Conseil juridique"]
        }

    def generate_date(self):
        # Générer une date aléatoire dans les 2 dernières années
        start_date = datetime.now() - timedelta(days=730)
        random_date = start_date + timedelta(days=random.randint(0, 730))
        return random_date.strftime("%d/%m/%Y")

    def generate_price(self):
        # Générer un prix aléatoire entre 1.5 et 100 euros
        return round(random.uniform(1.5, 100), 2)

    def generate_entry(self):
        # Choisir une catégorie et un libellé aléatoires
        category = random.choice(list(self.categories.keys()))
        label = random.choice(self.categories[category])
        return [self.generate_date(), category, label, self.generate_price()]

    def generate_csv(self, filename, num_entries):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Catégorie", "Libellé", "Prix (€)"])
            for _ in range(num_entries):
                writer.writerow(self.generate_entry())


# Utilisation de la classe
if __name__ == "__main__":
    generator = FakeDataGenerator()
    generator.generate_csv("donnees.csv", 200)
    print("Fichier CSV généré avec succès.")

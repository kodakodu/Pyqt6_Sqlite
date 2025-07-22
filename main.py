import sys
from PyQt6.QtWidgets import QApplication, QWidget,QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel, QHBoxLayout, QDialog

from models.model_person import Person,init_db

Session = init_db()

class AddEditDialog(QDialog):
    def __init__(self, session, personne=None):
        super().__init__()
        self.session = session
        self.person =Person
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ajouter / Modifier une personne')
        self.layout = QVBoxLayout()

        # Champs Nom et Prénom
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()

        if self.person:
            self.nom_input.setText(self.person.name)
            self.prenom_input.setText(self.person.surname)

        self.layout.addWidget(QLabel('Nom:'))
        self.layout.addWidget(self.nom_input)
        self.layout.addWidget(QLabel('Prénom:'))
        self.layout.addWidget(self.prenom_input)

        # Bouton Enregistrer
        self.btn_save = QPushButton('Enregistrer')
        self.btn_save.clicked.connect(self.save_personne)
        self.layout.addWidget(self.btn_save)

        self.setLayout(self.layout)

    def save_personne(self):
        name = self.nom_input.text()
        surname = self.prenom_input.text()
        if not name or not surname:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')
            return

        if self.person:
            self.person.name = name
            self.person.surname = surname
        else:
            nouvelle_personne = Person(name=name, surname=surname)
            self.session.add(nouvelle_personne)

        self.session.commit()
        self.accept()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('CRUD PyQt6 avec SQLAlchemy')
        self.layout = QVBoxLayout()

        # Tableau pour afficher les personnes
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nom', 'Prénom'])
        self.layout.addWidget(self.table)

        # Boutons
        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton('Ajouter')
        self.btn_edit = QPushButton('Modifier')
        self.btn_delete = QPushButton('Supprimer')

        self.btn_add.clicked.connect(self.add_personne)
        self.btn_edit.clicked.connect(self.edit_personne)
        self.btn_delete.clicked.connect(self.delete_personne)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        personnes = self.session.query(Person).all()
        for p in personnes:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(p.id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(p.nom))
            self.table.setItem(row_position, 2, QTableWidgetItem(p.prenom))

    def add_personne(self):
        dialog = AddEditDialog(self.session)
        if dialog.exec():
            self.load_data()

    def get_selected_personne(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une ligne.')
            return None
        row = selected_items[0].row()
        personne_id = int(self.table.item(row, 0).text())
        return self
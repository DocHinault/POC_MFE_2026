"""Backend database - Import depuis racine (migration en cours)"""
import sys
import os

# Ajouter la racine au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importer depuis l'ancien emplacement
from backend_database import *

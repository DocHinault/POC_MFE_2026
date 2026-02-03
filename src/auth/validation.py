"""Services d'authentification - Import depuis racine"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from auth import *

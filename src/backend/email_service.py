"""Backend email - Import depuis racine (migration en cours)"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend_email import *

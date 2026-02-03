"""Page de liaison des réseaux sociaux - Import depuis racine"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from pages.page_social_linking import page_social_linking

__all__ = ['page_social_linking']

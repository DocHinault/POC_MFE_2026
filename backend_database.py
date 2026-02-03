"""
Service d'accès aux données Google Sheets + fallback cache local
"""

import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from typing import List, Optional, Tuple, Dict
import os
import json


class LocalFileDatabase:
    """Fallback: Sauvegarde locale en JSON si Google Sheets n'est pas disponible"""
    
    def __init__(self, db_file: str = 'local_db.json'):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> dict:
        """Charge la base de données locale"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return {'clients': {}}
        return {'clients': {}}
    
    def _save(self):
        """Sauvegarde la base de données locale"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def find_client_by_email(self, email: str) -> Optional[Tuple[int, List]]:
        """Trouve un client par email"""
        email_lower = email.lower()
        for client_id, client_data in self.data.get('clients', {}).items():
            if client_data.get('email', '').lower() == email_lower:
                return (1, [client_id])
        return None
    
    def add_client(self, id_client: str, email: str, password_hash: str,
                   id_fb: str, id_insta: str, nom_entreprise: str,
                   secteur: str, created_at: str) -> bool:
        """Ajoute un client"""
        self.data['clients'][id_client] = {
            'email': email,
            'password_hash': password_hash,
            'id_fb': id_fb,
            'id_insta': id_insta,
            'nom_entreprise': nom_entreprise,
            'secteur': secteur,
            'created_at': created_at
        }
        self._save()
        return True
    
    def get_client_by_email(self, email: str) -> Optional[dict]:
        """Récupère les données complètes d'un client"""
        email_lower = email.lower()
        for client_id, client_data in self.data.get('clients', {}).items():
            if client_data.get('email', '').lower() == email_lower:
                return {
                    'id_client': client_id,
                    'email': client_data.get('email', ''),
                    'password_hash': client_data.get('password_hash', ''),
                    'id_fb': client_data.get('id_fb', ''),
                    'id_insta': client_data.get('id_insta', ''),
                    'nom_entreprise': client_data.get('nom_entreprise', ''),
                    'secteur': client_data.get('secteur', ''),
                    'created_at': client_data.get('created_at', '')
                }
        return None
    
    def get_client_by_id(self, client_id: str) -> Optional[dict]:
        """Récupère les données complètes d'un client par ID"""
        if client_id in self.data.get('clients', {}):
            client_data = self.data['clients'][client_id]
            return {
                'id_client': client_id,
                'email': client_data.get('email', ''),
                'password_hash': client_data.get('password_hash', ''),
                'id_fb': client_data.get('id_fb', ''),
                'id_insta': client_data.get('id_insta', ''),
                'nom_entreprise': client_data.get('nom_entreprise', ''),
                'secteur': client_data.get('secteur', ''),
                'created_at': client_data.get('created_at', '')
            }
        return None
    
    def update_client(self, client_data: dict) -> bool:
        """Met à jour les données d'un client"""
        client_id = client_data.get('id_client')
        if not client_id or client_id not in self.data.get('clients', {}):
            return False
        
        # Mettre à jour les champs
        self.data['clients'][client_id].update({
            'email': client_data.get('email', self.data['clients'][client_id].get('email')),
            'password_hash': client_data.get('password_hash', self.data['clients'][client_id].get('password_hash')),
            'id_fb': client_data.get('id_fb', self.data['clients'][client_id].get('id_fb')),
            'id_insta': client_data.get('id_insta', self.data['clients'][client_id].get('id_insta')),
            'nom_entreprise': client_data.get('nom_entreprise', self.data['clients'][client_id].get('nom_entreprise')),
            'secteur': client_data.get('secteur', self.data['clients'][client_id].get('secteur')),
        })
        self._save()
        return True



class SheetDatabase:
    """Gère l'accès à la Google Sheet pour les clients"""
    
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 
             'https://www.googleapis.com/auth/drive']
    
    def __init__(self, sheet_id: str, credentials_json_path: Optional[str] = None):
        """
        Initialise la connexion à Google Sheets
        
        Args:
            sheet_id: ID de la Google Sheet
            credentials_json_path: Chemin vers le fichier credentials JSON (optionnel)
        """
        self.sheet_id = sheet_id
        self.sheet = None
        self.clients_sheet = None
        
        # Charger les credentials
        if credentials_json_path and os.path.exists(credentials_json_path):
            credentials = Credentials.from_service_account_file(
                credentials_json_path,
                scopes=self.SCOPE
            )
            print(f"✅ Credentials chargés depuis {credentials_json_path}")
        else:
            # Essayer de charger depuis GOOGLE_APPLICATION_CREDENTIALS
            creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if creds_path and os.path.exists(creds_path):
                credentials = Credentials.from_service_account_file(
                    creds_path,
                    scopes=self.SCOPE
                )
                print(f"✅ Credentials chargés depuis {creds_path}")
            else:
                raise ValueError("Pas de credentials Google trouvés. Vérifiez GOOGLE_APPLICATION_CREDENTIALS dans .env")
        
        # Créer le client gspread
        self.gc = gspread.authorize(credentials)
        self.sheet = self.gc.open_by_key(sheet_id)
        self._init_sheet()
    
    def _init_sheet(self):
        """Initialise les feuilles nécessaires"""
        try:
            self.clients_sheet = self.sheet.worksheet('CLIENTS')
        except gspread.WorksheetNotFound:
            # Créer la feuille si elle n'existe pas
            self.clients_sheet = self.sheet.add_worksheet('CLIENTS', 100, 8)
            self._add_headers()
    
    def _add_headers(self):
        """Ajoute les en-têtes à la feuille CLIENTS"""
        headers = ['ID_CLIENT', 'EMAIL', 'MDP', 'ID_FB', 'ID_INSTA', 'NOM_ENTREPRISE', 'SECTEUR', 'CREE_LE']
        self.clients_sheet.insert_row(headers, 1)
    
    def find_client_by_email(self, email: str) -> Optional[Tuple[int, List]]:
        """
        Trouve un client par email
        
        Retourne: (row_index, row_values) ou None
        """
        try:
            all_values = self.clients_sheet.get_all_values()
            email_lower = email.lower()
            
            for idx, row in enumerate(all_values[1:], start=2):  # Commencer à la ligne 2 (après headers)
                if len(row) > 1 and row[1].lower() == email_lower:
                    return idx, row
            
            return None
        except Exception as e:
            print(f"Erreur lors de la recherche client: {e}")
            return None
    
    def add_client(self, id_client: str, email: str, password_hash: str, 
                   id_fb: str, id_insta: str, nom_entreprise: str, 
                   secteur: str, created_at: str) -> bool:
        """
        Ajoute un client à la feuille
        """
        try:
            row = [id_client, email, password_hash, id_fb, id_insta, nom_entreprise, secteur, created_at]
            self.clients_sheet.append_row(row)
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du client: {e}")
            return False
    
    def get_client_by_email(self, email: str) -> Optional[dict]:
        """
        Récupère les données complètes d'un client
        """
        result = self.find_client_by_email(email)
        if not result:
            return None
        
        idx, row = result
        if len(row) < 8:
            return None
        
        return {
            'id_client': row[0],
            'email': row[1],
            'password_hash': row[2],
            'id_fb': row[3],
            'id_insta': row[4],
            'nom_entreprise': row[5],
            'secteur': row[6],
            'created_at': row[7]
        }
    
    def get_client_by_id(self, client_id: str) -> Optional[dict]:
        """Récupère les données complètes d'un client par ID"""
        try:
            all_values = self.clients_sheet.get_all_values()
            
            for idx, row in enumerate(all_values[1:], start=2):  # Commencer à la ligne 2 (après headers)
                if len(row) > 0 and row[0] == client_id:
                    if len(row) < 8:
                        return None
                    
                    return {
                        'id_client': row[0],
                        'email': row[1],
                        'password_hash': row[2],
                        'id_fb': row[3],
                        'id_insta': row[4],
                        'nom_entreprise': row[5],
                        'secteur': row[6],
                        'created_at': row[7]
                    }
            
            return None
        except Exception as e:
            print(f"Erreur lors de la recherche client par ID: {e}")
            return None
    
    def update_client(self, client_data: dict) -> bool:
        """Met à jour les données d'un client"""
        try:
            client_id = client_data.get('id_client')
            if not client_id:
                return False
            
            all_values = self.clients_sheet.get_all_values()
            
            for idx, row in enumerate(all_values[1:], start=2):  # Commencer à la ligne 2 (après headers)
                if len(row) > 0 and row[0] == client_id:
                    # Préparer la nouvelle ligne
                    new_row = [
                        client_data.get('id_client', row[0]),
                        client_data.get('email', row[1]),
                        client_data.get('password_hash', row[2]),
                        client_data.get('id_fb', row[3]),
                        client_data.get('id_insta', row[4]),
                        client_data.get('nom_entreprise', row[5]),
                        client_data.get('secteur', row[6]),
                        row[7]  # Garder la date de création
                    ]
                    
                    # Mettre à jour la ligne
                    self.clients_sheet.delete_rows(idx, 1)
                    self.clients_sheet.insert_row(new_row, idx)
                    return True
            
            return False
        except Exception as e:
            print(f"Erreur lors de la mise à jour du client: {e}")
            return False


# Instance globale si Google Sheets est configuré
_db = None


def init_database(sheet_id: str, credentials_json_path: Optional[str] = None):
    """
    Initialise la base de données
    Utilise Google Sheets si possible, sinon utilise un cache local
    """
    global _db
    try:
        _db = SheetDatabase(sheet_id, credentials_json_path)
        print(f"✅ Base de données Google Sheets initialisée")
    except Exception as e:
        print(f"⚠️ Erreur Google Sheets: {e}")
        print("   Utilisation du cache local (données non synchronisées avec Google Sheets)")
        _db = LocalFileDatabase('local_db.json')
    return _db


def migrate_local_to_sheet(local_db: LocalFileDatabase, sheet_db: 'SheetDatabase') -> int:
    """Migre les entrées de la base locale vers la Google Sheet.
    Retourne le nombre d'entrées migrées.
    """
    migrated = 0
    clients = local_db.data.get('clients', {})
    for cid, c in clients.items():
        try:
            if not sheet_db.find_client_by_email(c.get('email')):
                ok = sheet_db.add_client(
                    id_client=cid,
                    email=c.get('email'),
                    password_hash=c.get('password_hash'),
                    id_fb=c.get('id_fb', ''),
                    id_insta=c.get('id_insta', ''),
                    nom_entreprise=c.get('nom_entreprise', ''),
                    secteur=c.get('secteur', ''),
                    created_at=c.get('created_at', '')
                )
                if ok:
                    migrated += 1
        except Exception as e:
            print(f"Erreur lors de la migration du client {cid}: {e}")
    return migrated


def get_database():
    """
    Récupère l'instance de la base de données
    Si aucune n'est initialisée, crée une base de données locale.
    Si des credentials Google existent et que la base actuelle est locale,
    tente une ré-initialisation vers Google Sheets puis migre les données locales.
    """
    global _db
    # Si non initialisé, créer local
    if _db is None:
        _db = LocalFileDatabase('local_db.json')
        print("💾 Utilisation de la base de données locale (local_db.json)")

    # Si on a une base locale mais que des credentials+sheet_id existent, tenter ré-init
    try:
        from os import path, getenv
        if isinstance(_db, LocalFileDatabase):
            creds_path = getenv('GOOGLE_APPLICATION_CREDENTIALS') or 'credentials.json'
            sheet_id = getenv('GOOGLE_SHEETS_ID')
            if creds_path and sheet_id and path.exists(creds_path):
                try:
                    sheet_db = SheetDatabase(sheet_id, creds_path)
                    print("🔄 Passage automatique vers Google Sheets détecté")
                    # Migrer les données locales
                    migrated = migrate_local_to_sheet(_db, sheet_db)
                    if migrated:
                        print(f"✅ Migrated {migrated} local clients to Google Sheets")
                    _db = sheet_db
                except Exception as e:
                    print(f"⚠️ Impossible de basculer vers Google Sheets: {e}")
    except Exception:
        pass

    return _db

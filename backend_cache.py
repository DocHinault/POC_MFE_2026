"""
Service de cache en mémoire avec TTL
"""

import time
from typing import Any, Optional
from datetime import datetime, timedelta


class CacheEntry:
    """Une entrée de cache avec TTL"""
    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expires_at = time.time() + ttl_seconds
    
    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class MemoryCache:
    """Cache en mémoire simple avec TTL"""
    
    def __init__(self):
        self.data = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if key not in self.data:
            return None
        
        entry = self.data[key]
        if entry.is_expired():
            del self.data[key]
            return None
        
        return entry.value
    
    def put(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Ajoute une valeur au cache"""
        self.data[key] = CacheEntry(value, ttl_seconds)
    
    def remove(self, key: str) -> None:
        """Supprime une valeur du cache"""
        if key in self.data:
            del self.data[key]
    
    def clear_expired(self) -> None:
        """Supprime toutes les entrées expirées"""
        expired_keys = [k for k, v in self.data.items() if v.is_expired()]
        for key in expired_keys:
            del self.data[key]


# Instance globale du cache
_cache = MemoryCache()


def get(key: str) -> Optional[Any]:
    """Récupère du cache"""
    return _cache.get(key)


def put(key: str, value: Any, ttl_seconds: int) -> None:
    """Ajoute au cache"""
    _cache.put(key, value, ttl_seconds)


def remove(key: str) -> None:
    """Supprime du cache"""
    _cache.remove(key)


def clear_expired() -> None:
    """Nettoie les entrées expirées"""
    _cache.clear_expired()

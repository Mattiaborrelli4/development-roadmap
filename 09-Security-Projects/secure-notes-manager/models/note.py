"""Modelli dati per il Secure Notes Manager."""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


@dataclass
class Note:
    """Rappresenta una nota crittografata."""
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str
    tags: Optional[list[str]] = None

    def __post_init__(self):
        """Converte le tag in lista se None."""
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> dict:
        """Converte la nota in dizionario."""
        return asdict(self)

    def to_json(self) -> str:
        """Converte la nota in JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        """Crea una nota da un dizionario."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'Note':
        """Crea una nota da una stringa JSON."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def update_content(self, content: str):
        """Aggiorna il contenuto e la data di modifica."""
        self.content = content
        self.updated_at = datetime.now().isoformat()

    def add_tag(self, tag: str):
        """Aggiunge un tag alla nota."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Rimuove un tag dalla nota."""
        if tag in self.tags:
            self.tags.remove(tag)

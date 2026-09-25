from dataclasses import dataclass, field
from app.domain.errors import ValidationError

@dataclass
class Ticket:
    id: int = 1
    requester_id: int = 101
    assigned_tech_id: int | None = None
    _tags: list[str] = field(default_factory=list, init=False, repr=False)

    @property
    def tags(self) -> tuple[str, ...]:
        return tuple(self._tags)

    def add_tag(self, tag: str) -> None:
        if not isinstance(tag, str):
            raise ValidationError("La etiqueta debe ser una cadena de texto.")
        
        normalized_tag = tag.strip().lower()
        
        if not normalized_tag:
            raise ValidationError("La etiqueta no puede estar vacía o contener solo espacios.")
        
        if normalized_tag not in self._tags:
            self._tags.append(normalized_tag)
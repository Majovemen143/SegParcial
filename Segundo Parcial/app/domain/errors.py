class DomainError(Exception):
    """Excepción base del dominio."""
    pass

class ValidationError(DomainError):
    """Excepción para errores de validación de datos."""
    pass

class DuplicateAssignmentError(DomainError):
    """Excepción para reasignación al mismo técnico."""
    pass

class TicketNotFoundError(DomainError):
    """Excepción cuando un ticket no existe."""
    pass
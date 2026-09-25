import pytest
from app.models.entities import Ticket
from app.domain.errors import ValidationError, DuplicateAssignmentError, TicketNotFoundError
from app.services.notifications import WebhookNotifier
from app.services.tickets import TicketService

class DummyUser:
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email

class DummyUserService:
    def __init__(self):
        self.users = {
            101: DummyUser(101, "cliente@test.com"),
            50: DummyUser(50, "tech1@test.com"),
            51: DummyUser(51, "tech2@test.com")
        }
    def require(self, user_id):
        return self.users[user_id]

class DummyTicketRepo:
    def __init__(self):
        self.tickets = {1: Ticket(id=1, requester_id=101, assigned_tech_id=None)}
    def get(self, ticket_id):
        return self.tickets.get(ticket_id)

def test_tags_normalizacion_y_duplicados():
    t = Ticket()
    t.add_tag("  URGENTE ")
    t.add_tag("urgente")
    assert t.tags == ("urgente",)

def test_tags_rechazo_espacios():
    t = Ticket()
    with pytest.raises(ValidationError):
        t.add_tag("   ")

def test_tags_independencia():
    t1, t2 = Ticket(), Ticket()
    t1.add_tag("redes")
    assert "redes" in t1.tags
    assert "redes" not in t2.tags

def test_tags_inmutabilidad_publica():
    t = Ticket()
    with pytest.raises(AttributeError):
        t.tags = ["nuevo"]

def test_watchers_y_asignacion_webhook():
    webhook = WebhookNotifier()
    service = TicketService(DummyTicketRepo(), DummyUserService(), webhook)
    
    watchers = service.watchers(1)
    assert len(watchers) == 1
    
    service.assign(1, 50)
    assert len(webhook.sent_payloads) == 1
    assert webhook.sent_payloads[0]["recipient"] == "tech1@test.com"

    with pytest.raises(DuplicateAssignmentError):
        service.assign(1, 50)

if __name__ == "__main__":
    pytest.main([__file__])
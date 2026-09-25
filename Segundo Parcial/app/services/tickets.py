from app.domain.errors import TicketNotFoundError, DuplicateAssignmentError
from app.services.notifications import Notifier

class TicketService:
    def __init__(self, ticket_repo, user_service, notifier: Notifier):
        self._tickets = ticket_repo
        self._users = user_service
        self.notifier = notifier

    def require(self, ticket_id: int):
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(f"Ticket {ticket_id} no encontrado.")
        return ticket

    def watchers(self, ticket_id: int) -> list:
        ticket = self.require(ticket_id)
        
        watchers_list = []
        seen_user_ids = set()

        requester = self._users.require(ticket.requester_id)
        watchers_list.append(requester)
        seen_user_ids.add(requester.id)

        if ticket.assigned_tech_id:
            if ticket.assigned_tech_id not in seen_user_ids:
                tech = self._users.require(ticket.assigned_tech_id)
                watchers_list.append(tech)
                seen_user_ids.add(tech.id)

        return watchers_list

    def assign(self, ticket_id: int, tech_id: int) -> None:
        ticket = self.require(ticket_id)

        if ticket.assigned_tech_id == tech_id:
            raise DuplicateAssignmentError(f"El ticket {ticket_id} ya está asignado al técnico {tech_id}.")

        ticket.assigned_tech_id = tech_id
        tech = self._users.require(tech_id)
        self.notifier.send(tech.email, f"Se te ha asignado el ticket {ticket_id}")
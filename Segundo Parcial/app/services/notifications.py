from typing import Protocol

class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...

class WebhookNotifier:
    def __init__(self):
        self.sent_payloads: list[dict] = []

    def send(self, recipient: str, message: str) -> None:
        self.sent_payloads.append({
            "recipient": recipient,
            "message": message
        })
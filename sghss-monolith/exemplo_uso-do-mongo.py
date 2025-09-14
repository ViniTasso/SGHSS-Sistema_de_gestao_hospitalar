# Exemplo de como usar a conexão para salvar um log

from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class AuditLog(Document):
    user_id = StringField(required=True)
    action = StringField(required=True)
    resource = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'audit_logs'}

def log_event(user_id, action, resource):
    new_log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource
    )
    new_log.save()

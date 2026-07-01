from prometheus_client import Counter

# Criação de um contador no formato do Prometheus
# O 'labelnames' nos permite filtrar no Grafana (ex: quantas de texto vs áudio)
MESSAGES_RECEIVED = Counter(
    "whatsapp_messages_received_total",
    "Total de mensagens recebidas no webhook",
    ["message_type"]
)

MESSAGES_SENT = Counter(
    "whatsapp_messages_sent_total",
    "Total de mensagens enviadas pela IA",
    ["message_type"]
)
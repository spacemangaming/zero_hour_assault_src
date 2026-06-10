import requests

BOT_KEY = "8657640809:AAEUZLTpNXH7KUMYrssZqXlgO_QI84X-PWw"   # kendi bot token'iniz
ADMIN_IDS = ["7810113372"]   # birden fazla admin id buraya eklenebilir
API_ENDPOINT = f"https://api.telegram.org/bot{BOT_KEY}/sendMessage"

def make_request(endpoint, payload):
    try:
        response_data = requests.post(endpoint, data=payload)
        return response_data.text
    except Exception as err:
        return str(err)

def notify_admins(message_text):
    feedback = []
    for admin_uid in ADMIN_IDS:
        answer = make_request(API_ENDPOINT, {
            "chat_id": admin_uid,
            "text": message_text
        })
        feedback.append(answer)
    return feedback

# Örnek kullanım
print(notify_admins("🎫 Ticket #42: Kullanıcı @ali 'Oyuna giremiyorum' dedi."))

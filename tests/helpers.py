import datetime


class TgTestBot:
    def send_message(self, text: str, chat_id: str, reply_markup=None):
        print(text, chat_id, reply_markup)


def tournament_payload(members_ids=None, no_data=False, **extra_data):
    if no_data:
        return {
            'open_tournament_exists': False,
            'tournaments': []
        }

    tournament = {
        'id': 1,
        'members_count': len(members_ids or []),
        'name': 't1',
        'members_limit': 10,
        'member_cost': 1000,
        'duration': 5,
        'created_at': str(datetime.datetime(2023, 11, 11)),
        'starts_at': str(datetime.datetime(2023, 12, 11)),
    }

    members = []
    for member in members_ids or []:
        members.append({'tg_id': member, 'status': 'approved'})

    return {
            'open_tournament_exists': True,
            'tournaments': [tournament | extra_data]
        }

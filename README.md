### setup
1) python 3.10 and upper

```commandline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Launch project
1) generate locale `cd locales/ru/LC_MESSAGES && msgfmt app.po -o app.mo`
2) launch tgbot `python3 event_handlers.py`
3) launch flask server `flask --app main run --reload`

### Public api endpoints

#### POST /tgsend?token={token}
#### Body params:
1) chat_ids: list[int]
2) message: str

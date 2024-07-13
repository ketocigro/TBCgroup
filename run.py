from ext import app
from routes import (home, show_guitars, guitar_detail, show_basses, bass_detail,
    show_accessories, accessory_detail, show_keyboards, keyboard_detail, show_microphones,
    microphone_detail,login, register, add_item, logout, submit_comment, add_card, add_to_basket, view_basket, remove_from_basket)

app.run(host="0.0.0.0")

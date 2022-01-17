# copyright 2022 @Ansaku
# Telegram @AnkiSatya
# Instagram @satya_ask
import telebot
import requests
from telebot.types import InlineKeyboardButton

# Fillout Here The BotToken it gets from botfather further queries @AnkiSatya 0n telegram
bot = telebot.TeleBot('5090617847:AAGdVnas_9Mp2bkGwyWCIX1YRmtHRLntTQs')

while True:
    try:

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Buat email'))
        keyboard.add(InlineKeyboardButton(text='Refresh pesan'))
        keyboard.add(InlineKeyboardButton(text='Tentang'))


        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id,
                             'Hai Pengguna., Selamat datang di TempEmail Bot \nPenggunaan:\nUntuk Menghasilkan email klik tombol "Buat email"\nUntuk menyegarkan kotak masuk Anda, klik tombol "Refresh inbox". Setelah surat baru tiba, Anda akan melihat tombol dengan baris subjek, klik tombol read the message. \n\n Dev : @AnkiSatya',
                             reply_markup=keyboard)


        @bot.message_handler(content_types=['text'])
        def send_text(message):
            if message.text.lower() == 'buat email':
                email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
                ekeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                ekeyboard.add(InlineKeyboardButton(text='Buat email'))
                ekeyboard.add(InlineKeyboardButton(text='Refresh pesan\n[' + str(email) + "]"))
                ekeyboard.add(InlineKeyboardButton(text='Tentang'))
                bot.send_message(message.chat.id, "E-Mail Sementara Anda:")
                bot.send_message(message.chat.id, str(email), reply_markup=ekeyboard)
            elif message.text.lower() == 'refresh pesan':
                bot.send_message(message.chat.id, 'Pertama, buat email anda', reply_markup=keyboard)
            elif message.text.lower() == 'tentang':
                bot.send_message(message.chat.id,
                                 'Apa itu Email Semantara?\n- Itu adalah layanan email gratis yang memungkinkan untuk menerima email di alamat sementara yang akan dihancurkan sendiri setelah waktu tertentu berlalu. Itu juga dikenal dengan nama-nama seperti tempmail, 10minutemail, 10minmail, throwaway email, fake-mail , fake email generator, burner mail atau trash-mail\n\nBagaimana Email Sementara Menjadi Lebih Aman bagi Anda?\n- Menggunakan Email sementara memungkinkan Anda untuk sepenuhnya melindungi kotak surat asli Anda dari hilangnya informasi pribadi. Alamat email sementara Anda sepenuhnya anonim. Detail Anda: informasi tentang orang Anda dan pengguna yang berkomunikasi dengan Anda, alamat IP, alamat email dilindungi dan sepenuhnya dirahasiakan.\n\n➪ Nama Bot : TempMail Bot\n➪ Pembuat : @AnkiSatya\n➪ Language : Python \n➪ Donasi : https://saweria.co/ansaku')
            elif message.text.lower()[14] == "[":
                email = message.text.lower()[15:message.text.lower().find("]")]
                bkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                bkeyboard.add(InlineKeyboardButton(text='Refresh pesan\n[' + str(email) + "]"))
                bkeyboard.add(InlineKeyboardButton(text='Buat email'))
                try:
                    data = requests.get(
                        "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find(
                            "@")] + "&domain=" + email[email.find("@") + 1:]).json()
                    if 'id' in data[0]:
                        for i in range(len(data)):
                            id = data[i]['id']
                            subject = data[i]['subject']
                            fromm = data[i]['from']
                            date = data[i]['date']
                            if len(subject) > 15:
                                subject = str(subject[0:15]) + "..."
                            bkeyboard.add(InlineKeyboardButton(
                                text=str(subject) + "\n dari: " + fromm + " in " + "[id" + str(id) + "][" + str(
                                    email) + "]"))
                            bot.send_message(message.chat.id,
                                             "Subjek: " + subject + "\n Dari: " + fromm + "\n Tanggal:" + date,
                                             reply_markup=bkeyboard)
                            count = i + 1
                        bot.send_message(message.chat.id, "Di Sini " + str(
                            count) + " Pesan ditemukan\nKlik tombol di bawah untuk membaca pesan\n\n Info lebih lanjut @AnkiSatya")
                    else:
                        bot.send_message(message.chat.id, 'Tidak ditemukan', reply_markup=bkeyboard)
                except BaseException:
                    bot.send_message(message.chat.id, 'Tidak ada pesan yang diterima...', reply_markup=bkeyboard)
            elif message.text.lower().find("[id"):
                try:
                    data = message.text.lower()[message.text.lower().find("[id"):]
                    id = data[data.find("[") + 3:data.find(']')]
                    email = data[data.find("][") + 2:-1]
                    msg = requests.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find(
                        "@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + id).json()
                    bot.send_message(message.chat.id,
                                     'Pesan ✉️\n\n   Dari: ' + msg['from'] + "\n   Subjek: " + msg[
                                         'subject'] + "\n   Tanggal: " + msg[
                                         'date'] + "\n   Teks: " + msg['textBody'])
                except BaseException:
                    pass


        bot.polling(none_stop=True, interval=1, timeout=5000)
    except BaseException:
        pass
        
# Stay tuned for more : Telegram @AnkiSatya

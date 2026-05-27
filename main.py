import telebot
import random

# MASUKKAN TOKEN BOT ANDA DI SINI
TOKEN = "GANTI_DENGAN_TOKEN_BOT_ANDA_DARI_BOTFATHER"
bot = telebot.TeleBot(TOKEN)

# Penyimpanan data game sementara (di memori RAM)
game_data = {
    "is_started": False,
    "players": {}, # format: {user_id: {"name": name, "role": None, "alive": True}}
}

# Perintah untuk bergabung ke game di grup
@bot.message_handler(commands=['join'])
def join_game(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if user_id not in game_data["players"]:
        game_data["players"][user_id] = {"name": user_name, "role": None, "alive": True}
        bot.reply_to(message, f"✅ {user_name} berhasil bergabung ke game!")
    else:
        bot.reply_to(message, "Anda sudah bergabung!")

# Perintah untuk memulai game dan membagikan peran secara privat
@bot.message_handler(commands=['startgame'])
def start_game(message):
    if len(game_data["players"]) < 3:
        bot.reply_to(message, "Minimal butuh 3 pemain untuk memulai game!")
        return
        
    bot.reply_to(message, "Game dimulai! Membagikan peran rahasia ke PC masing-masing...")
    
    # Acak peran sederhana (1 Werewolf, 1 Seer, sisanya Villager)
    player_ids = list(game_data["players"].keys())
    roles = ["Werewolf", "Seer"] + ["Villager"] * (len(player_ids) - 2)
    random.shuffle(roles)
    
    # Kirim peran lewat PM (Pesan Privat)
    for i, p_id in enumerate(player_ids):
        game_data["players"][p_id]["role"] = roles[i]
        try:
            bot.send_message(p_id, f"🤫 Peran rahasia Anda adalah: *{roles[i]}*", parse_mode="Markdown")
        except:
            bot.send_message(message.chat.id, f"⚠️ Gagal mengirim peran ke {game_data['players'][p_id]['name']}. Pastikan sudah chat /start ke bot ini secara pribadi!")

# Menjalankan bot
bot.infinity_polling()

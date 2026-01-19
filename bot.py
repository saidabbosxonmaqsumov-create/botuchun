import os
import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiohttp import web
import sys

# Token va Owner ID endi Environment Variables orqali olinadi
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# /start buyrug‘i
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name or "-"
    username = f"@{message.from_user.username}" if message.from_user.username else "-"
    dm_link = f"https://t.me/{message.from_user.username}" if message.from_user.username else "❌ username yo'q"

    # Admin uchun xabar
    text = (
        f"🆕 <b>Yangi foydalanuvchi botni ishga tushirdi!</b>\n\n"
        f"👤 Ism: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 Foydalanuvchi ID: {user_id}\n"
        f"📩 Direct message: {dm_link}"
    )
    await bot.send_message(chat_id=OWNER_ID, text=text)

    # Foydalanuvchiga salom
    await message.answer("👋 Salom! Bu bot orqali Maksumovga xabar yuborishingiz mumkin.")

@dp.message(Command("info"))
async def info_handler(message: types.Message):
    info_text = (
        "✨ <b>Ma'lumot</b> ✨\n\n"
        "👤 <b>Maksumov</b>\n"
        "📅 <b>Yosh:</b> 20\n"
        "📍 <b>Shaxar:</b> Andijon\n"
        "🎓 <b>O'qish/Ish:</b> ADU\n"
        "🎯 <b>Qiziqishlar:</b> Dasturlash, IT loyihalar, Startaplar\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🌐 <b>Social:</b>\n\n"
        "✈️ <b>Telegram:</b> @maaksumov\n"
        "📸 <b>Instagram:</b> https://www.instagram.com/maksumov.s.k\n"
        "📩 <i>Menga shu bot orqali ham yozishingiz mumkin!</i>"
    )
    
    await message.answer(info_text)

# Oddiy xabarlarni forward qilish
@dp.message()
async def forward_handler(message: types.Message):
    # Agar admin reply qilib javob yozsa
    if message.from_user.id == OWNER_ID and message.reply_to_message:
        match = re.search(r"Foydalanuvchi ID: (\d+)", message.reply_to_message.text)
        if match:
            user_id = int(match.group(1))
            await bot.send_message(chat_id=user_id, text=f"👤 Maksumov javobi:\n\n{message.text}")
            await message.answer("✅ Javob foydalanuvchiga yuborildi")
        else:
            await message.answer("❌ Foydalanuvchi ID topilmadi")
        return

    # Oddiy foydalanuvchi xabar yuborsa
    user_id = message.from_user.id
    full_name = message.from_user.full_name or "-"
    username = f"@{message.from_user.username}" if message.from_user.username else "-"

    text = (
        f"📩 Yangi xabar:\n\n"
        f"👤 Ism: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 Foydalanuvchi ID: {user_id}\n\n"
        f"✉️ Xabar:\n{message.text}"
    )

    await bot.send_message(chat_id=OWNER_ID, text=text)
    await message.answer("✅ Xabaringiz yuborildi, Maksumov onlayn bo'lishi bilanoq javob beradi.")

async def start_server():
    routes = web.RouteTableDef()

    @routes.get("/")
    async def index(request):
        return web.Response(text="Bot is running!")

    app = web.Application()
    app.add_routes(routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Server starting on port {port}")

async def main():
    await start_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

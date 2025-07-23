
import os
import logging
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ChatMemberHandler,
)
from telegram.constants import ChatMemberStatus
from collections import defaultdict
from dotenv import load_dotenv
import re
import asyncio

load_dotenv()
TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

GROSERIAS = ['maldito', 'mardito', 'idiota', 'estúpido', 'imbécil']

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

advertencias = defaultdict(int)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy TlgBot, estoy activo y listo para ayudarte.")

async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        bienvenida_texto = (
            f"Hola {user.mention_html()} y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. "
            "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:

"
            "📌 Reglas:
"
            "• Prohibido dar precios en público.
"
            "• Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
"
            "• Nada de spam, promociones o enlaces sin autorización.
"
            "• Evita mensajes repetitivos, cadenas o contenido no relacionado.
"
            "• Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.

"
            "📎 Comandos útiles:
"
            "/reglas – Reglas del grupo
"
            "/staff – Ver administradores
"
            "/ayuda – Pedir ayuda a los administradores

"
            "¡Bienvenid@ y disfruta tu estadía!"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bienvenida_texto, parse_mode='HTML')

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "📌 Reglas del grupo:
"
        "• Prohibido dar precios en público.
"
        "• Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
"
        "• Nada de spam, promociones o enlaces sin autorización.
"
        "• Evita mensajes repetitivos, cadenas o contenido no relacionado.
"
        "• Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos."
    )
    await update.message.reply_text(texto)

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await context.bot.get_chat_administrators(chat_id=update.effective_chat.id)
    texto = "👮 Lista de administradores del grupo:

"
    for admin in chat_admins:
        user = admin.user
        if user.username:
            texto += f"• <a href='https://t.me/{user.username}'>{user.full_name}</a>
"
        else:
            texto += f"• {user.full_name} (sin @usuario)
"
    await update.message.reply_text(texto, parse_mode='HTML')

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mensaje = f"📣 El usuario {user.mention_html()} ha solicitado ayuda en el grupo."
    await update.message.reply_text("✅ Hemos notificado a los administradores. Pronto te ayudarán.", parse_mode='HTML')
    admins = await context.bot.get_chat_administrators(chat_id=update.effective_chat.id)
    for admin in admins:
        if admin.user.id != user.id:
            try:
                await context.bot.send_message(chat_id=admin.user.id, text=mensaje, parse_mode='HTML')
            except:
                pass

async def filtro_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()
    user_id = update.effective_user.id
    user_mention = update.effective_user.mention_html()
    chat_id = update.effective_chat.id

    if any(palabra in mensaje for palabra in GROSERIAS) or "http" in mensaje or "t.me/" in mensaje:
        advertencias[user_id] += 1
        conteo = advertencias[user_id]
        await update.message.reply_text(f"⚠️ {user_mention}, advertencia {conteo}/3. Si continúas, serás silenciado.", parse_mode='HTML')

        if conteo == 2:
            admins = await context.bot.get_chat_administrators(chat_id=chat_id)
            for admin in admins:
                try:
                    await context.bot.send_message(chat_id=admin.user.id, text=f"⚠️ El usuario {user_mention} ya tiene 2 advertencias.", parse_mode='HTML')
                except:
                    pass
        elif conteo >= 3:
            await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"🚫 {user_mention} ha sido silenciado por 5 minutos.", parse_mode='HTML')
            await asyncio.sleep(300)
            await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=ChatPermissions(can_send_messages=True))
            advertencias[user_id] = 0

async def menciones_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.entities:
        admins = await context.bot.get_chat_administrators(chat_id=update.effective_chat.id)
        mencionados = [update.message.parse_entity(ent) for ent in update.message.entities if ent.type == 'mention']
        for mencionado in mencionados:
            for admin in admins:
                if admin.user.username and f"@{admin.user.username.lower()}" == mencionado.lower():
                    try:
                        await context.bot.send_message(chat_id=admin.user.id, text=f"🔔 Fuiste mencionado en el grupo {update.effective_chat.title}.")
                    except:
                        pass

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reglas", reglas))
    app.add_handler(CommandHandler("staff", staff))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filtro_mensajes))
    app.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), menciones_admins))

    print("🤖 Bot en funcionamiento...")
    app.run_polling()

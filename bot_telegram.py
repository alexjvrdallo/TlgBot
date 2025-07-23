
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ChatMemberHandler
from telegram import Update, ChatPermissions
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes
import re
from collections import defaultdict
import datetime

# Token del bot
TOKEN = "7734679096:AAFbYiMa7RBYZ3kPqeAr-hxiSYg7UUwEieI"

# Lista de groserías
GROSERIAS = ["puta", "mierda", "pendejo", "cabron", "idiota", "imbecil", "malparido", "verga"]

# Diccionario de advertencias
advertencias = defaultdict(int)

# IDs de administradores
ADMIN_IDS = [123456789, 987654321]

def contiene_groseria(texto):
    texto = texto.lower()
    for palabra in GROSERIAS:
        if re.search(rf'\b{palabra}\b', texto):
            return True
    return False

def contiene_spam(texto):
    patrones_spam = [r"http[s]?://", r"www\.", r"\.com", r"\.net", r"\.org"]
    for patron in patrones_spam:
        if re.search(patron, texto, re.IGNORECASE):
            return True
    return False

async def manejar_infraccion(update: Update, context: ContextTypes.DEFAULT_TYPE, tipo="grosería"):
    usuario = update.effective_user
    chat_id = update.effective_chat.id
    user_id = usuario.id
    advertencias[user_id] += 1

    await update.message.delete()

    await update.message.reply_text(
        f"⚠️ @{usuario.username or usuario.first_name}, no está permitido usar {tipo}s.\n"
        f"Advertencia {advertencias[user_id]}/2. Si repites, serás silenciado por 5 minutos."
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"👮 Alerta: @{usuario.username or usuario.first_name} usó una {tipo} en el grupo {update.effective_chat.title}.\n"
                     f"Mensaje: {update.message.text}"
            )
        except:
            pass

    if advertencias[user_id] >= 2:
        advertencias[user_id] = 0
        mute_duracion = datetime.timedelta(minutes=5)
        hasta = datetime.datetime.now() + mute_duracion
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=hasta
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔇 @{usuario.username or usuario.first_name} ha sido silenciado por 5 minutos por reincidir."
        )

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    texto = update.message.text

    if contiene_groseria(texto):
        await manejar_infraccion(update, context, tipo="grosería")
    elif contiene_spam(texto):
        await manejar_infraccion(update, context, tipo="spam")

async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status == ChatMemberStatus.MEMBER:
        nombre = result.new_chat_member.user.first_name
        mensaje = (
            f"👋 ¡Bienvenido/a al grupo, {nombre}!\n\n"
            f"📜 *Reglas del grupo:*\n"
            f"1️⃣ No decir malas palabras\n"
            f"2️⃣ No Spam (de ningún tipo)\n"
            f"3️⃣ No hablar de precios en ningún grupo\n\n"
            f"✅ ¡Esperamos que disfrutes y respetes las normas!"
        )
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=mensaje,
            parse_mode="Markdown"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(ChatMemberHandler(bienvenida, ChatMemberHandler.CHAT_MEMBER))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))
app.run_polling()

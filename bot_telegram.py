import logging
    from aiogram import Bot, Dispatcher, executor, types
    from aiogram.types import ChatMemberUpdated, ChatPermissions
    import os

    API_TOKEN = os.getenv("API_TOKEN")
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN, parse_mode="Markdown")
    dp = Dispatcher(bot)

    # Diccionario de advertencias por usuario
    warnings = {}

    # Palabras prohibidas
    bad_words = ["grosería1", "grosería2", "spam", "maldición", "precio", "http", "https"]

    reglas_texto = "*Reglas del grupo:*
" \
                   "1. Prohibido dar precios en público.
" \
                   "2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
" \
                   "3. Nada de spam, promociones o enlaces sin autorización.
" \
                   "4. Evita mensajes repetitivos, cadenas o contenido no relacionado.
" \
                   "5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos."

    bienvenida_texto = "*Hola y gracias por unirte a nuestra comunidad.*
" \
                       "Estamos muy contentos de tenerte aquí.

" \
                       "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos.

" \
                       "Usa /reglas para ver las normas del grupo.
" \
                       "Usa /staff para conocer a los administradores.
" \
                       "Si necesitas ayuda, escribe /ayuda y se notificará a los administradores."

    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        await message.answer("¡Hola! Usa /reglas para ver las normas del grupo.")

    @dp.message_handler(commands=["reglas"])
    async def cmd_reglas(message: types.Message):
        await message.reply(reglas_texto)

    @dp.message_handler(commands=["ayuda"])
    async def cmd_ayuda(message: types.Message):
        admins = await bot.get_chat_administrators(message.chat.id)
        for admin in admins:
            try:
                await bot.send_message(admin.user.id, f"El usuario @{message.from_user.username or message.from_user.full_name} pidió ayuda en el grupo *{message.chat.title}*.")
            except:
                continue
        await message.reply("Se ha notificado a los administradores. ¡Pronto te ayudarán!")

    @dp.message_handler(commands=["staff"])
    async def cmd_staff(message: types.Message):
        admins = await bot.get_chat_administrators(message.chat.id)
        texto = "*Administradores del grupo:*

"
        for admin in admins:
            user = admin.user
            if user.username:
                texto += f"• [{user.first_name}](https://t.me/{user.username})
"
            else:
                texto += f"• {user.first_name} (ID: `{user.id}`)
"
        texto += "
Puedes contactarlos tocando su nombre."
        await message.reply(texto, parse_mode="Markdown")

    @dp.chat_member_handler()
    async def welcome_new_member(update: ChatMemberUpdated):
        if update.new_chat_member.status == "member":
            await bot.send_message(update.chat.id, bienvenida_texto)

    @dp.message_handler()
    async def filtro_mensajes(message: types.Message):
        texto = message.text.lower()
        if any(palabra in texto for palabra in bad_words):
            uid = message.from_user.id
            warnings[uid] = warnings.get(uid, 0) + 1

            if warnings[uid] == 2:
                admins = await bot.get_chat_administrators(message.chat.id)
                for admin in admins:
                    try:
                        await bot.send_message(admin.user.id, f"El usuario @{message.from_user.username or message.from_user.full_name} recibió su segunda advertencia en *{message.chat.title}*.")
                    except:
                        continue

            if warnings[uid] >= 3:
                try:
                    await message.chat.restrict(uid, ChatPermissions(can_send_messages=False), until_date=300)
                    await message.reply("Has sido silenciado por 5 minutos por violar repetidamente las reglas.")
                except:
                    pass
            else:
                await message.reply(f"Advertencia {warnings[uid]}/3: ese contenido no está permitido.")

    if __name__ == "__main__":
        executor.start_polling(dp, skip_updates=True)
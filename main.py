from keep_alive import keep_alive
keep_alive()
# import
import datetime
import os
from discord.ext import commands
from discord import Intents
from telegram import Bot 



DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_IDS = ['2023014289', '2106774730']

voice_sessions = {}

intents = Intents.default()
intents.message_content = True  # Enable receiving message content in 

discord_bot = commands.Bot(command_prefix='!', intents=intents)
telegram_bot = Bot(token=TELEGRAM_TOKEN)

# telegram commands 


@discord_bot.event
async def on_ready():
		print('Bot is ready.')

# Events
@discord_bot.event
async def on_message(message):
		author_name = message.author.name
		server_name = message.guild.name
		channel_name = message.channel.name

		text = f'Ник: {author_name}\nСервер: {server_name}\nКанал: {channel_name}\nСообщение: {message.content}'

		if message.attachments:
				attachments = "\nВложения:"
				for attachment in message.attachments:
						attachments += f"\n- {attachment.url}"
				text += attachments

		for chat_id in TELEGRAM_CHAT_IDS:
				await telegram_bot.send_message(chat_id=chat_id, text=text)

		await discord_bot.process_commands(message)

		# Check for attachments
@discord_bot.event
async def on_message(message):
		if message.attachments:
				attachments = "\nВложения:"
				for attachment in message.attachments:
						attachments += f"\n- {attachment.url}"
				text += attachments

		for chat_id in TELEGRAM_CHAT_IDS:
				await telegram_bot.send_message(chat_id=chat_id, text=text)

		await discord_bot.process_commands(message)
	
# voice connect and disconnect
@discord_bot.event
async def on_voice_state_update(member, before, after):
		if before.channel is None and after.channel is not None:
				# Member joined a voice channel
				author_name = member.name
				server_name = member.guild.name
				channel_name = after.channel.name
				start_time = datetime.datetime.now()
				voice_sessions[member.id] = start_time
				text = f'Ник: {author_name}\nСервер: {server_name}\nКанал: {channel_name}\nПрисоединился к голосовому каналу в {start_time}'

				for chat_id in TELEGRAM_CHAT_IDS:
						await telegram_bot.send_message(chat_id=chat_id, text=text)

		elif before.channel is not None and after.channel is None:
				# Member left a voice channel
				start_time = voice_sessions.get(member.id)
				if start_time:
						end_time = datetime.datetime.now()
						duration = end_time - start_time
						del voice_sessions[member.id]
						duration_seconds = duration.total_seconds()
						duration_hours = int(duration_seconds // 3600)
						duration_minutes = int((duration_seconds % 3600) // 60)
						duration_seconds = duration_seconds % 60
						duration_formatted = f'{duration_hours}:{duration_minutes:02d}:{duration_seconds:.2f}'
						author_name = member.name
						server_name = member.guild.name
						channel_name = before.channel.name
						text = f'Ник: {author_name}\nСервер: {server_name}\nКанал: {channel_name}\nПокинул голосовой канал в {end_time}.\nПродолжительность: {duration_formatted}'

						for chat_id in TELEGRAM_CHAT_IDS:
								await telegram_bot.send_message(chat_id=chat_id, text=text)
@discord_bot.event
async def on_message(message):
		author_name = message.author.name
		server_name = message.guild.name
		channel_name = message.channel.name
		text = f'Ник: {author_name}\nСервер: {server_name}\nКанал: {channel_name}\nСообщение: {message.content}'

		if message.attachments:
				attachments = "\nВложения:"
				for attachment in message.attachments:
						attachments += f"\n- {attachment.url}"
				text += attachments

		for chat_id in TELEGRAM_CHAT_IDS:
				await telegram_bot.send_message(chat_id=chat_id, text=text)
				await discord_bot.process_commands(message)
# Commands

@discord_bot.command()
async def servers(ctx):
		bot = ctx.bot
		guilds = bot.guilds
		for guild in guilds:
				members = guild.members
				member_names = [member.name for member in members]
				text = f"Сервер: {guild.name}\nУчастники: {', '.join(member_names)}"
				await ctx.send(f'\n{text}\n')

discord_bot.run(DISCORD_TOKEN)

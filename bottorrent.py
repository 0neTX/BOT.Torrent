#!/usr/bin/env python3
LICENCIA = """
BOTTorrent - 3.3 :
Este programa es software GRATUITO: puedes redistribuirlo y/o modificar
bajo los términos de la Licencia Pública General GNU publicada por
la Free Software Foundation, ya sea la versión 3 de la Licencia, o
(a su elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil,
pero SIN NINGUNA GARANTÍA, ni RESPONSABILIDAD; sin siquiera la garantía implícita de
COMERCIABILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Ver el
Licencia pública general GNU para obtener más detalles <https://www.gnu.org/licenses/>.

El USUARIO de este programa, es el UNICO RESPONSABLE, de que el USO del mismo, 
se limita, al estricto cumplimiento, de cualquier LEY, aplicable.
"""
INSTALACION = """
BOTTorrent - 3.3 :
*** Guía para instalar el bot ***
BOT.torrent es un sencillo script, para un BOT de Telegram, escrito en Python. 
Su función, es descargar ficheros, reenviados al BOT, en un directorio de nuestra elección.
Este BOT está especialmente pensado, para ejecutarse en un NAS.
Instalación:
1: Crear nuestro BOT en Telegram y obtener su TOKEN (Guías multiples en la red)
2: Crear nuestra App en Telegram y obtener su api_id y api_hash. (Si no las tenemos)
--> https://my.telegram.org/auth (Guías multiples en la red)
3: Instalar python3, en nuestro NAS. (Si no lo tenemos ya instalado. No es necesario en DSM7)
4: Instalar pip en nuestro NAS, abriendo una sesión SSH, (Si no lo tenemos ya instalado) 
--> sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
--> sudo python3 get-pip.py
5: Instalar telethon --> sudo python3 -m pip install telethon
6: Instalar cryptg --> sudo python3 -m pip install cryptg
7: Copiar BOT.torrent.py, en nuestro NAS y editar las variables propias DE CADA USUARIO. 
8: Ejecutar BOT de forma interactiva --> python3 -u BOT.torrent.py (Por supuesto, se puede arrancar, también en background y de formar automatizada)
A disfrutar ;-)

DekkaR - 2021
"""
AYUDA = """BOT.Torrent - 3.3 :
/ayuda      : Esta pantalla.
/start      : LICENCIA GPL, de este programa.
/instalar   : Guía para instalar este programa.
/ID			: Devuelve ID de Telegram
/version    : Detalles de la ultima versión.
"""
VERSION = """BOT.Torrent - 3.3 :

- Soporte para la discriminación de ficheros ".dsf" y ".m4a", de Audio de Alta Resolución.
- Soporte para la discriminación de ficheros ".epub", de libros.
- Añadido el % de la descarga, en mensaje informativo. Aportación inicial, de Jonathan Salinas (https://t.me/jsavargas). Modificado (>100MB). 

- Carpeta de descarga temporal:
Ahora el bot, permite activar una carpeta de descarga temporal, en tiempo real.
La carpeta temporal se creará, tomando como raíz, los caminos definidos por el usuario, 
para música, libros y general. Los .torrent, NO se ven afectados por la carpeta temporal.

Forma de funcionamiento: 
Mediante el prefijo ">>" en la caja de texto, al reenviar una descarga al bot:

>>Nombre carpeta temporal

El bot descargará todos los ficheros, reenviados, a dicha carpeta.
"""
import os
import sys
import time
import asyncio
import cryptg
import re
# Imports Telethon
from telethon import TelegramClient, events
from telethon.tl import types
from telethon.utils import get_extension, get_peer_id, resolve_id
carpeta_tmp = ''
date_control = ''

'''
LOGGER
'''
import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
################# LOG

# Variables de cada usuario ######################
# This is a helper method to access environment variables or
# prompt the user to type them in the terminal if missing.
def get_env(name, message, cast=str):
    if name in os.environ:
        print("os.environ[name]",name,os.environ[name])
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)

# Define some variables so the code reads easier
session = os.environ.get('TG_SESSION', 'bottorrent_downloader')
api_id = get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_env('TG_API_HASH', 'Enter your API hash: ')
bot_token = get_env('TG_BOT_TOKEN', 'Enter your Telegram BOT token: ')
TG_AUTHORIZED_USER_ID = get_env('TG_AUTHORIZED_USER_ID', 'Enter your Telegram BOT token: ')
download_path = get_env('TG_DOWNLOAD_PATH', 'Enter full path to downloads directory: ')
download_path_torrent = os.getenv('TG_WATCH_PATH', "/var/watch") # Directorio bajo vigilancia de DSDownload u otro.
download_path_mp3 = get_env('TG_DOWNLOAD_PATH_MP3', 'Enter full path to downloads MP3: ')
download_path_pdf = get_env('TG_DOWNLOAD_PATH_PDF', 'Enter full path to downloads PDF: ')

logger.info('TG_API_ID: %s',api_id)
logger.info('TG_API_HASH: %s',api_hash)
logger.info('TG_BOT_TOKEN: %s',bot_token)
logger.info('TG_DOWNLOAD_PATH: %s',download_path)
logger.info('TG_WATCH_PATH: %s',download_path_torrent)
logger.info('TG_DOWNLOAD_PATH_MP3: %s',download_path_mp3)
logger.info('TG_DOWNLOAD_PATH_PDF: %s',download_path_pdf)
logger.info('TG_AUTHORIZED_USER_ID: %s',TG_AUTHORIZED_USER_ID)

#api_id = 161 # Vuestro api_id. Cambiar
#api_hash = '3ef04ad'
#bot_token = '3945:09m-p4'
#download_path = '/download'
#download_path_torrent = '/volume1/vuestros directorios' # Directorio bajo vigilancia de DSDownload u otro.
#usuarios = {6537361:'yo'} # <--- IDs de usuario autorizados. Los mismos de la versión 2.1. Cambiar
usuarios = list(map(int, TG_AUTHORIZED_USER_ID.replace(" ", "").split(','))) 
logger.info('TG_AUTHORIZED_USER_ID: %s',usuarios)
##################################################

# Cola de descargas temporales.
queue = asyncio.Queue()
number_of_parallel_downloads = int(os.environ.get('TG_MAX_PARALLEL',1))
maximum_seconds_per_download = int(os.environ.get('TG_DL_TIMEOUT',3600))

# Directorio temporal
if not os.path.exists(download_path):
	os.makedirs(download_path, exist_ok = True)
if not os.path.exists(download_path_torrent):
	os.makedirs(download_path_torrent, exist_ok = True)
if not os.path.exists(download_path_mp3):
	os.makedirs(download_path_mp3, exist_ok = True)
if not os.path.exists(download_path_pdf):	
	os.makedirs(download_path_pdf, exist_ok = True)
tmp_path = os.path.join(download_path,'tmp')
if not os.path.exists(tmp_path):
	os.makedirs(tmp_path, exist_ok = True)


#Envío de msg directo al primer usuario:
async def msg_dir(msg):
	for id in usuarios:
		id_user = id
		break
	await client.send_message(id_user, msg)
	return True

# Impresión del % de descarga.
async def callback(current, total, file_path, message):
	value = (current / total) * 100
	dec = str(abs(value) - abs(int(value)))[2:4]
	value = int(value)
	try:
		if total > 102400 and dec == '00' and value != 100 and  value != 0 and value % 2 == 0:
			await message.edit('Descargando ... {}%'.format(value))
	finally:
		current

async def worker(name):
	while True:
		# Esperando una unidad de trabajo.
		queue_item = await queue.get()
		update = queue_item[0]
		message = queue_item[1]
		carpeta_tmp = queue_item[2] if queue_item[2] else ''
		id_user , peer_type = resolve_id(get_peer_id(update.message.peer_id))
		# Comprobación de usuario
		if id_user not in usuarios:
			logger.info('USUARIO: %s NO AUTORIZADO', message.peer_id.user_id) 
			print('Usuario ', message.peer_id.user_id, ' no autorizado.')
			break
		###
		#if carpeta_tmp: time.sleep(2)
		file_path = tmp_path;
		file_name = 'Fichero ...';
		if isinstance(update.message.media, types.MessageMediaPhoto): 
			file_name = '{}{}'.format(update.message.media.photo.id, get_extension(update.message.media))
			file_path = os.path.join(file_path, file_name)
		else:
			attributes = update.message.media.document.attributes
			for attr in attributes:
				if isinstance(attr, types.DocumentAttributeFilename):
					file_name = attr.file_name
					file_path = os.path.join(file_path, attr.file_name)
		await message.edit('Descargando ... ')
		mensaje = '[%s] Descarga de %s, iniciada por %s ...' % (time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()), file_name, message.peer_id.user_id)
		logger.info(mensaje + '\n')		
		try:
			loop = asyncio.get_event_loop()
			#task = loop.create_task(client.download_media(update.message, file_path))
			task = loop.create_task(client.download_media(update.message, file_path, progress_callback = lambda x, y: callback(x, y, file_path, message)))
			download_result = await asyncio.wait_for(task, timeout = maximum_seconds_per_download)
			end_time = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
			end_time_short = time.strftime('%H:%M', time.localtime())
			filename = os.path.split(download_result)[1]
			# Ficheros .mp3, .flac y .dsf
			if filename.endswith('.mp3') or filename.endswith('.flac') or filename.endswith('.dsf') or filename.endswith('.m4a'):
				if carpeta_tmp:
					tmp = os.path.join(download_path_mp3, carpeta_tmp)
					os.makedirs(tmp, exist_ok = True)
					final_path = os.path.join(tmp, filename)
				else:
					final_path = os.path.join(download_path_mp3, filename)
			# Ficheros .pdf, .cbr y .epub
			elif filename.endswith('.pdf') or filename.endswith('.cbr') or filename.endswith('.epub'): 
				if carpeta_tmp:
					tmp = os.path.join(download_path_pdf, carpeta_tmp)
					os.makedirs(tmp, exist_ok = True)
					final_path = os.path.join(tmp, filename)
				else:
					final_path = os.path.join(download_path_pdf, filename)
			# Ficheros .torrent
			elif filename.endswith('.torrent'): 
				final_path = os.path.join(download_path_torrent, filename)
			else:
				if carpeta_tmp:
					tmp = os.path.join(download_path, carpeta_tmp)
					os.makedirs(tmp, exist_ok = True)
					final_path = os.path.join(tmp, filename)
				else:
					final_path = os.path.join(download_path, filename)
			
			###### 	
			os.rename(download_result, final_path)
			######
			
			mensaje = '[%s] Descarga %s terminada. ' % (end_time, file_name)
			logger.info(mensaje + '\n')
			await message.edit('Descarga terminada %s' % (end_time_short))
		except asyncio.TimeoutError:
			print('[%s] Tiempo excedido en %s' % (time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())), file_name)
			await message.edit('Error!')
			message = await update.reply('ERROR: Tiempo excedido descargando este fichero')
		except Exception as e:
			logger.critical(e)
			print('[EXCEPCION]: %s' % (str(e)))
			print('[%s] Excepcion %s' % (file_name, time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())))
			await message.edit('Error!')
			message = await update.reply('ERROR: %s descargando : %s' % (e.__class__.__name__, str(e)))

		# Unidad de trabajo terminada.
		queue.task_done()

client = TelegramClient(session, api_id, api_hash, proxy = None, request_retries = 10, flood_sleep_threshold = 120)

@events.register(events.NewMessage)
async def handler(update):
	global carpeta_tmp
	global date_control
	id_user, peer_type = resolve_id(get_peer_id(update.message.peer_id))
	
	if update.message.media is not None and id_user in usuarios:
		if date_control != update.message.date  and  update.message.message[0:2] != '>>': carpeta_tmp = ''
		file_name = 'sin nombre';
		if isinstance(update.message.media, types.MessageMediaPhoto): 
			file_name = '{}{}'.format(update.message.media.photo.id, get_extension(update.message.media))
		else:
			attributes = update.message.media.document.attributes
			for attr in attributes:
				if isinstance(attr, types.DocumentAttributeFilename):
					file_name = attr.file_name
		message = await update.reply('En cola...')
		await queue.put([update, message, carpeta_tmp])
		mensaje = '[%s] Descarga en cola %s' % (time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()), file_name)
		logger.info(mensaje + '\n')		
	elif update.message.message and id_user in usuarios:
		if update.message.message == '/ayuda':
			message = await update.reply(AYUDA) 
			await queue.put([update, message, carpeta_tmp])
		elif update.message.message == '/start': 
			message = await update.reply(LICENCIA)
			await queue.put([update, message, carpeta_tmp])
		elif update.message.message == '/instalar': 
			message = await update.reply(INSTALACION)
			await queue.put([update, message, carpeta_tmp])
		elif update.message.message == '/version': 
			message = await update.reply(VERSION)
			await queue.put([update, message, carpeta_tmp])
		elif update.message.message[0:2] == '>>':
			tmp = re.sub(r'[^A-Za-z0-9 -!\[\]\(\)]+', ' ', update.message.message.replace('>', '').strip())
			if tmp:
				message = await update.reply('Carpeta temporal [ %s ] activada.' % tmp)
				carpeta_tmp = tmp
				date_control = update.message.date
				logger.info('Carpeta temporal [ %s ] activada.', tmp)
				await queue.put([update, message, carpeta_tmp])
		
		else:
			time.sleep(1)
			message = await update.reply('Eco del BOT: ' + update.message.message)
			await queue.put([update, message, carpeta_tmp])
			print('Eco del BOT: ' + update.message.message)
	
	# Comprobación de usuario
	if id_user not in usuarios:
		logger.info('USUARIO: %s NO AUTORIZADO', id_user) 
		print('Usuario ', id_user, ' no autorizado.')
	# ID de usuario
	if update.message.message in ('/ID', '/id'):
		print('ID de Telegram :', id_user)
		message = await update.reply('ID de Telegram :' + id_user)
		await queue.put([update, message, carpeta_tmp])

try:
	# Crear cola de procesos concurrentes.
	tasks = []
	for i in range(number_of_parallel_downloads):
		loop = asyncio.get_event_loop()
		task = loop.create_task(worker(f'worker-{i}'))
		tasks.append(task)

	# Arrancamos bot con token
	client.start(bot_token = str(bot_token))
	client.add_event_handler(handler)

	# Pulsa Ctrl+C para detener
	loop.run_until_complete(msg_dir("BotTorrent on line"))
	logger.info("********** BotTorrent Start **********")


	# Pulsa Ctrl+C para detener
	print('Arranque correcto!! (Pulsa Ctrl+C para detener)')
	client.run_until_disconnected()
	
finally:
	# Cerrando trabajos.
	for task in tasks:
		task.cancel()
	# Cola cerrada
	# Stop Telethon
	client.disconnect()
	print(' Parado!!! ')
	
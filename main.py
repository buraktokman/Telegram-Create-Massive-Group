#!/usr/bin/env python3
# -*- coding: utf-8 -*

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

'''
https://my.telegram.org/apps
https://python.gotrained.com/adding-telegram-members-to-your-groups-telethon-python/#Choose_a_Group_to_Add_Members
'''

CONFIG = {'app_id': '',
			'app_hash': '',
			'phone': ''}


def main():
	global CONFIG

	client = TelegramClient(CONFIG['phone'],
							CONFIG['app_id'],
							CONFIG['app_hash'])
	client.connect()

	if not client.is_user_authorized():
		client.send_code_request(CONFIG['phone'])
		client.sign_in(CONFIG['phone'], input('Enter the code: '))


	chats = []
	last_date = None
	chunk_size = 200
	groups=[]

	result = client(GetDialogsRequest(
							 offset_date=last_date,
							 offset_id=0,
							 offset_peer=InputPeerEmpty(),
							 limit=chunk_size,
							 hash = 0
						 ))
	chats.extend(result.chats)

	for chat in chats:
		try:
			if chat.megagroup== True:
				groups.append(chat)
		except:
			continue

	print('Choose a group to scrape members from:')
	i=0
	for g in groups:
		print(str(i) + '- ' + g.title)
		i+=1

	# g_index = input("Enter a Number: ")
	g_index = 0
	target_group=groups[int(g_index)]

	print('Fetching Members...')
	all_participants = []
	all_participants = client.get_participants(target_group, aggressive=True)


	available_members = 0
	for user in all_participants:
		# print(dir(user))
		# print(user.todict())

		if user.username:
			username= user.username
		else:
			username= ""
		if user.first_name:
			first_name= user.first_name
		else:
			first_name= ""
		if user.last_name:
			last_name= user.last_name
		else:
			last_name= ""
		name= (first_name + ' ' + last_name).strip()

		if user.username is not None or user.phone is not None:
			print(f'username: {user.username}\tphone: {user.phone}\tname: {name}')
			available_members += 1

	print(f'{available_members}/{len(all_participants)}')
		# print('------')

	# print('Saving In file...')
	# with open("members.csv","w",encoding='UTF-8') as f:
	#     writer = csv.writer(f,delimiter=",",lineterminator="\n")
	#     writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
	#     for user in all_participants:
	#         if user.username:
	#             username= user.username
	#         else:
	#             username= ""
	#         if user.first_name:
	#             first_name= user.first_name
	#         else:
	#             first_name= ""
	#         if user.last_name:
	#             last_name= user.last_name
	#         else:
	#             last_name= ""
	#         name= (first_name + ' ' + last_name).strip()
	#         writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
	# print('Members scraped successfully.')

if __name__ == '__main__':
	main()
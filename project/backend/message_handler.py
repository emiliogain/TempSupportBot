chatlist = dict()


import asyncio
from .scenario import States, fsm
from .actions.actions_manager import ActionManager

user_db = dict()
last_user_id = 1000000
user_state_db = dict()
#chatlist = dict()
class MessageHandler:

	async def new_user()-> int:
		_last_user_id =1000000
		while True :
			_last_user_id = _last_user_id + 1
			last_user_id = _last_user_id
			user_id = last_user_id
			try:
				check_user = user_db[user_id]
			except:
				user_db[user_id] = 1
				user_state_db[user_id] = States.START
				chatlist[user_id] = []
				break


		return last_user_id

	async def new_message(user_id: int, message : str ):
		current_state = user_state_db[user_id]

		fsm.machine.set_state(current_state)

		print("message",message, "  State", current_state)
		if current_state == States.WAIT_QUERY:
			user_state_db[user_id] = States.GET_QUERY
			fsm.machine.set_state(States.GET_QUERY)

		print("  State", user_state_db[user_id])
		while True:

			current_state = user_state_db[user_id]
			
			action =  await ActionManager.get_action(current_state)
			transiotion = await action.handle_transition(user_id, message)
			
			
			print(action, transiotion)
			if transiotion == None :
				return chatlist[user_id]
				user_state_db[user_id] = fsm.state
				break
			fsm.trigger(transiotion)
			user_state_db[user_id] = fsm.state

	async def new_chat(user_id: int):

		fsm.machine.set_state(States.NEW_CHAT)
		user_state_db[user_id] = States.NEW_CHAT
		message = 'начата новая тема'
		while True:

			current_state = user_state_db[user_id]
			
			action =  await ActionManager.get_action(current_state)
			transiotion = await action.handle_transition(user_id, message)
			
			
			print(action, transiotion)
			if transiotion == None :
				return message
				user_state_db[user_id] = fsm.state
				break
			fsm.trigger(transiotion)
			user_state_db[user_id] = fsm.state
		


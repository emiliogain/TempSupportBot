from project.backend.message_handler import chatlist
from project.backend.scenario import Transitions
import asyncio

class GetQueryActions:
	async def handle_transition(user_id : int , message: str):
		try:
			bot_answer = " bot answer"
			chatlist[user_id].append({"user": message})
			chatlist[user_id].append({"assistant": bot_answer})
			return Transitions.SUCCESS
		except Exception as e:
			print(e)
			return Transitions.FAIL

	async def handle_event(user_id : int , message: str):
		return Transitions.SUCCESS


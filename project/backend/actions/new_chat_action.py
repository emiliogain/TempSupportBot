from project.backend.message_handler import chatlist
from project.backend.scenario import Transitions
import asyncio

class ChatHandler:
	async def handle_transition(user_id :int, message: str = ' ') -> Transitions:
		try:
			chatlist[user_id].clear()
			return Transitions.SUCCESS
		except:
			return Transitions.FAIL
	async def handle_event(user_id: int, message: str):
		return Transitions.SUCCESS

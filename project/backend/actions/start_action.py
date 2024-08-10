from project.backend.message_handler import chatlist
from project.backend.scenario import Transitions
import asyncio

class StartAction:

	async def handle_event(user_id: int, message: str):
		return Transitions.USER_AUTHORISED
	async def handle_transition(user_id: int, message: str):
		chatlist[user_id].append({"assistand" : "привет я бот"})
		return Transitions.USER_AUTHORISED
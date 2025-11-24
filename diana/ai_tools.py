from langchain.tools import tool
from asgiref.sync import sync_to_async, async_to_sync

from diana.database import AsyncSessionLocal
from diana.models import Todo
from datetime import datetime

@tool
async def get_now_date() -> str:
    """
    get now date.

    Returns:
        str: now date like: 2025-11-24
    """
    return str(datetime.now().date())


async def __create_todo(date:str, time:str, title:str):
    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                _datetime = f"{date} {time}"
                datetime_to_do_it = await sync_to_async(datetime.strptime)(_datetime, "%Y-%m-%d %H:%M")
                todo = Todo(title=title, datetime_to_do_it=datetime_to_do_it)
                session.add(todo)

        
        return "todo sucessfuly saved"
    except Exception as ex:
        return f"something wrong! {ex}"

# TODO: Check why this function returns an error when the agent attempts to call it.
@tool
def create_todo(date:str, time:str, title:str) -> str:
    """
    Use this tool IMMEDIATELY and WITHOUT EXCEPTION whenever the user wants to
    create a new todo, reminder, appointment, plan, or schedule anything for the future.

    This tool stores the user's schedule in a database so that it can be better recalled later and reports can be generated on the tasks.

    You MUST call this tool when you see phrases like:
    - Remind me to ...
    - Set a reminder for ...
    - Create a todo for ...
    - I have a meeting/appointment/plan on ...
    - Remember to call someone tomorrow
    - Schedule something
    - Don't let me forget to ...
    - Put in my calendar ...

    Even if the user speaks in Persian (Farsi) or gives the date in Persian calendar (Shamsi), 
    you MUST convert it to Gregorian (YYYY-MM-DD) yourself and call this tool.

    Examples that MUST trigger this tool:
    - "Remind me to go to the doctor next Monday at 3 PM"

    - "Set a reminder for December 25, 2025 at 14:30 for team meeting"
    
    Args:
        date (str): Date in EXACT YYYY-MM-DD format (example: 2025-11-26, 2025-12-25)
        time (str): Time in 24-hour HH:MM format with leading zeros (example: 09:30, 17:00, 08:15)
        title (str): Full title or description of the task/reminder exactly as the user wants it saved

    Returns:
        str: Success or error message
    """
    
    return async_to_sync(__create_todo)(date, time, title)


 
TOOLS = [
    get_now_date,
    create_todo,
]

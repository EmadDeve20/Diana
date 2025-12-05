from datetime import datetime

from langchain.tools import tool

from asgiref.sync import sync_to_async

from diana.database import AsyncSessionLocal
from diana.models import Todo


@tool
async def get_now_date() -> str:
    """
    get now date.
    Always use this tool when you want to save data in the DB or get information to the user.
    because this tool always wants to show always now datetime to keep you up to date.
    about year, month, and day.

    Returns:
        str: now date like: 2025-11-24
    """
    return str(datetime.now().date())


@tool
async def get_now_time() -> str:
    """
    Returns the current real-world time in HH:MM:SS format (local server time).

    You MUST call this tool every time you need to know the exact current time 
    in order to answer the user correctly or perform any time-based calculation.

    Always use this tool (never guess or use your training data time) in these situations:
    - User asks "What time is it?" or "What’s the time now?"
    - User wants scheduling, reminders, or delays ("Remind me in 2 hours", "Call me at 5 PM", "Do this tomorrow morning")
    - You need to calculate time differences ("How many minutes until 6 PM?", "Is it past 9 AM yet?")
    - User mentions relative time ("in an hour", "this evening", "tonight at 8")
    - Any task involving countdowns, deadlines, alarms, or calendar planning

    Important: Your internal knowledge of time is static and outdated. Always use this tool 
    to get the accurate, up-to-the-second current time.

    Returns:
        str: Current time in 24-hour format as "HH:MM:SS" (e.g., "14:35:27")
    """
    now_time = str(datetime.now().time()) 
    return now_time.split(".")[0]


# TODO: check this function why sometimes crushed!
# what is best practice to use SQLAlchemy to save data in this function?
@tool
async def create_todo(date:str, time:str, title:str) -> str:
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
    while True:
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


TOOLS = [
    get_now_date,
    get_now_time,
    create_todo,
]

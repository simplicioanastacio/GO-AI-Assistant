# marathon/marathon.py
from llama.llama_runner import ask_go

marathon_data = {}  # simple in-memory store; replace with DB later

def start_marathon(user_id, distance_km, goal_time_h, date):
    marathon_data[user_id] = {
        "goal_distance": distance_km,
        "goal_time": goal_time_h,
        "date": date
    }
    return "Marathon goal set."

def create_training_plan(user_id, fitness_level, days_per_week):
    if user_id not in marathon_data:
        return "Please start a marathon plan first."
    
    goal = marathon_data[user_id]
    prompt = f"""
    Create a {days_per_week}-day-per-week marathon training plan for a runner 
    aiming to run {goal['goal_distance']} km in {goal['goal_time']} hours by {goal['date']}.
    Fitness level: {fitness_level}.
    Provide a week-by-week schedule.
    """
    return ask_go(prompt)

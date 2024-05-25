from mongodb import conversation_db
from datetime import datetime, timezone
import uuid
from mongodb.create_user import get_user_name

def initialize_user(user_id):
    # Initialize a user in the database.
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if user:
        print(f"User '{user_id}' already exists.")
    else:
        new_user = {
            "user_id": user_id,
            "user_name": get_user_name(user_id),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "goals": [],
            "metadata": {
                "language": "en",
                "context": {}
            }
        }
        collection.insert_one(new_user)

def create_goal(user_id, new_goal):
    # Create a new goal.
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if not user:
        initialize_user(user_id)

    goals = user.get("goals", [])
    goal_id = str(len(goals) + 1)
    new_goal_data = {
        "goal_id": goal_id,
        "goal": new_goal,
        "status": "Not Started",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "sub_goals": []
    }
    goals.append(new_goal_data)
    collection.update_one({"user_id": user_id}, {"$set": {"goals": goals}})

def create_subgoal(user_id, goal_id, new_subgoal):
    # Create a new subgoal.
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if not user:
        print("User not found.")
        return

    goals = user.get("goals", [])
    goal = next((goal for goal in goals if goal["goal_id"] == goal_id), None)
    if not goal:
        print("Goal not found.")
        return

    sub_goals = goal.get("sub_goals", [])
    sub_goal_id = f"{goal_id}.{len(sub_goals) + 1}"
    new_subgoal_data = {
        "sub_goal_id": sub_goal_id,
        "sub_goal": new_subgoal,
        "status": "Not Started",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    sub_goals.append(new_subgoal_data)
    goal["sub_goals"] = sub_goals
    goal["updated_at"] = datetime.utcnow().isoformat() + "Z"
    collection.update_one({"user_id": user_id}, {"$set": {"goals": goals}})
    print(f"Subgoal added: {new_subgoal}")

def delete_goal(user_id, goal_id):
    # Delete a goal.
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if not user:
        print("User not found.")
        return

    goals = user.get("goals", [])
    goal = next((goal for goal in goals if goal["goal_id"] == goal_id), None)
    if goal:
        goals.remove(goal)
        collection.update_one({"user_id": user_id}, {"$set": {"goals": goals}})
        print(f"Goal removed: {goal['goal']}")
    else:
        print("Goal not found.")

def delete_subgoal(user_id, goal_id, sub_goal_id):
    # Delete a subgoal.
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if not user:
        print("User not found.")
        return

    goals = user.get("goals", [])
    goal = next((goal for goal in goals if goal["goal_id"] == goal_id), None)
    if goal:
        sub_goals = goal.get("sub_goals", [])
        sub_goal = next((sg for sg in sub_goals if sg["sub_goal_id"] == sub_goal_id), None)
        if sub_goal:
            sub_goals.remove(sub_goal)
            goal["sub_goals"] = sub_goals
            goal["updated_at"] = datetime.utcnow().isoformat() + "Z"
            collection.update_one({"user_id": user_id}, {"$set": {"goals": goals}})
            print(f"Subgoal removed: {sub_goal['sub_goal']}")
        else:
            print("Subgoal not found.")
    else:
        print("Goal not found.")

def update_goal(user_id, goal_id, updated_goal):
    """Update a goal."""
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if not user:
        print("User not found.")
        return

    goals = user.get("goals", [])
    goal = next((goal for goal in goals if goal["goal_id"] == goal_id), None)
    if goal:
        goal["goal"] = updated_goal
        goal["updated_at"] = datetime.utcnow().isoformat() + "Z"
        collection.update_one({"user_id": user_id}, {"$set": {"goals": goals}})
        print(f"Goal updated to: {updated_goal}")
    else:
        print("Goal not found.")

def update_subgoal(user_id, goal_id, sub_goal_id, updated_subgoal):
    """Update a subgoal."""
    collection = conversation_db['goals']
    user = collection.find_one({"user_id": user_id})
    if not user:
        print("User not found.")
        return

    goals = user.get("goals", [])
    goal = next((goal for goal in goals if goal["goal_id"] == goal_id), None)
    if goal:
        sub_goals = goal.get("sub_goals", [])
        sub_goal = next((sg for sg in sub_goals if sg["sub_goal_id"] == sub_goal_id), None)
        if sub_goal:
            sub_goal["sub_goal"] = updated_subgoal
            sub_goal["updated_at"] = datetime.utcnow().isoformat() + "Z"
            goal["updated_at"] = datetime.utcnow().isoformat() + "Z"
            collection.update_one({"user_id": user_id}, {"$set": {"goals": goals}})
            print(f"Subgoal updated to: {updated_subgoal}")
        else:
            print("Subgoal not found.")
    else:
        print("Goal not found.")

def list_goals(user_name):
    collection = conversation_db['goals']
    user = collection.find_one({"user_name": user_name})
    if user:
        return user['goals']
    print(f"Username {user_name} doesn't have any goals defined.")
    return 

def generate_conversation_json(conversation_id, user_name, messages):
    conversation_json = {
        "conversation_id": conversation_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages": messages,
        "metadata": {
            "user_name": user_name,
            "language": "en",
            "context": {}
        }
    }
    return conversation_json

def conversation_to_mongo(user_name, messages):

    # Create (or use existing) collection
    collection = conversation_db['conversations']

    # make a random UUID
    conversation_id = str(uuid.uuid4())

    # Insert the conversation into the collection
    collection.insert_one(generate_conversation_json(conversation_id, user_name, messages))

    # Create an index on the metadata.user_name field
    collection.create_index(user_name)

    print("Conversation inserted and index created.")


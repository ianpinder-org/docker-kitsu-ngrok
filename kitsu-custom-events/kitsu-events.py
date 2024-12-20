import os
import ast
import gazu
import json
import datetime
import messages

# variables
STANDARD_KITSU_URL = os.environ['STANDARD_KITSU_URL']
EVENTS_KITSU_URL = os.environ['EVENTS_KITSU_URL']
EVENTS_KITSU_LOGIN = os.environ['EVENTS_KITSU_LOGIN']
EVENTS_KITSU_PASSWORD = os.environ['EVENTS_KITSU_PASSWORD']
KITSU_EVENTS_TOKEN = os.getenv("KITSU_EVENTS_TOKEN")

# parse stringified array
excludeList = ast.literal_eval(os.environ['EVENTS_EXCLUDE_EVENTS'])
excludeList = [n.strip() for n in excludeList]

EVENTS_LANG = os.environ['EVENTS_LANG']

# init gazu
# gazu.client.set_host(STANDARD_KITSU_URL + "/api")
gazu.client.set_host(STANDARD_KITSU_URL)
gazu.log_in(EVENTS_KITSU_LOGIN, EVENTS_KITSU_PASSWORD)
# gazu.set_token (KITSU_EVENTS_TOKEN)
# gazu.set_event_host(EVENTS_KITSU_URL + "/socket.io")
gazu.set_event_host(EVENTS_KITSU_URL)

REVIEW_STATUS_CODE = "review"

def rtw(data):
    print("rtw (ready for work) started..")

    # debug
    print(json.dumps(data))

    # verify task is set to 'Done'
    done = gazu.task.get_task_status_by_short_name("done")
    if (data["new_task_status_id"] != done["id"]):
        return

    # get task info
    task = gazu.client.get("data/tasks/" + data["task_id"])
    
    # get entity task belongs to (to determine if it's shot or asset)
    entity = gazu.client.get("data/entities/" + task["entity_id"])

    # get all tasks associated with this entity
    tasksList = gazu.client.get("data/tasks?entity_id=" + entity["id"])
    #tasksList = gazu.task.get_task_by_entity(entity, task["task_type_id"])
    
    # red or blue pill
    forShots = "false"
    if (entity["type"] != "Asset"):
        forShots = "true"

    # get all task types for assets only
    taskTypesList = gazu.client.get("data/task-types?for_shots="+forShots)
    
    # sort the list of task types by 'priority' field
    sortedTaskTypesList = sorted(taskTypesList, key=lambda d: d['priority']) 

    # get id's of all task types
    IDs = []
    for elem in sortedTaskTypesList:
        IDs.append(elem["id"])
    
    # make array of excluded id's of task types
    toExcludeIDs = []
    for id in IDs:
        toExcludeIDs.append(id)
        if (id == task["task_type_id"]):
            break

    # exclude using list of id's to exclude
    for i in toExcludeIDs:
        if i in IDs:
            IDs.remove(i)

    # change status for 'next' task type
    rtw = gazu.task.get_task_status_by_short_name("rtw") # be sure to have a status in Kitsu with 'rtw' short name wich is: Ready to Work
    if (len(IDs) > 0):
        id = IDs[0]
        for task in tasksList:
            if (task["task_type_id"] == id):
                # Get fresh data for particular task
                if (task["task_status_id"] != done["id"]):
                    gazu.task.add_comment(task["id"], rtw, messages.say(EVENTS_LANG, "rtw_changed"))
                else:
                    return

def delta(data):
    print("delta (delta between plan / actual) started..")

    # verify task is set to 'Done'
    done = gazu.task.get_task_status_by_short_name("done")
    if (data["new_task_status_id"] != done["id"]):
        return
    
    # get task info
    task = gazu.client.get("data/tasks/" + data["task_id"])
    start_date = task["start_date"]
    due_date = task["due_date"]
    end_date = task["end_date"]

    if (start_date is None or due_date is None or end_date is None):
        return

    # datetime(year, month, day, hour, minute, second)
    start = datetime.datetime.strptime(task["start_date"], '%Y-%m-%dT%H:%M:%S')
    due = datetime.datetime.strptime(task["due_date"], '%Y-%m-%dT%H:%M:%S')
    end = datetime.datetime.strptime(task["end_date"], '%Y-%m-%dT%H:%M:%S')

    # returns a timedelta object
    plan_delta = due-start
    print('Difference: ', plan_delta)
    
    '''
    plan_minutes = plan_delta.total_seconds() / 60
    print('Total difference in minutes: ', plan_minutes)
    
    # returns the difference of the time of the day
    plan_hours = plan_delta.total_seconds() / 60 / 60
    print('Total difference in hours: ', plan_hours)

    # returns the difference of the time of the day
    plan_days = plan_delta.total_seconds() / 60 / 60 / 24
    print('Total difference in days: ', plan_days)
    '''

    fact_delta = end-start    

    if (fact_delta.total_seconds() > plan_delta.total_seconds()):
        done = gazu.task.get_task_status_by_short_name("done")
        late_diff = fact_delta - plan_delta
        late_diff_days = late_diff.total_seconds() / 60 / 60 / 24
        gazu.task.add_comment(task["id"], done, messages.say(EVENTS_LANG, "plan_short") + str(round(late_diff_days, 1)))
    else:
        done = gazu.task.get_task_status_by_short_name("done")
        late_diff =  plan_delta - fact_delta
        late_diff_days = late_diff.total_seconds() / 60 / 60 / 24
        gazu.task.add_comment(task["id"], done, messages.say(EVENTS_LANG, "plan_long") + str(round(late_diff_days, 1)))

def lock(data):
    print("lock (new new task if old unfinished) started..")

    # debug
    print(json.dumps(data))

    # skip if todo was reassigned (we ignore todo all the time)
    todo = gazu.task.get_task_status_by_short_name("todo")
    if (data["new_task_status_id"] == todo["id"]):
        return

    # get task info
    task = gazu.client.get("data/tasks/" + data["task_id"])
    
    # get entity task belongs to (to determine if it's shot or asset)
    entity = gazu.client.get("data/entities/" + task["entity_id"])

    # get all tasks associated with this entity
    tasksList = gazu.client.get("data/tasks?entity_id=" + entity["id"])

    # red or blue pill
    forShots = "false"
    if (entity["type"] != "Asset"):
        forShots = "true"

    # get all task types for assets only
    taskTypesList = gazu.client.get("data/task-types?for_shots="+forShots)
    
    # sort the list of task types by 'priority' field
    sortedTaskTypesList = sorted(taskTypesList, key=lambda d: d['priority']) 

    # get id's of all task types
    IDs = []
    for elem in sortedTaskTypesList:
        IDs.append(elem["id"])
    
    # exclude current task type form id's list
    toExcludeIDs = []
    for id in IDs:
        if (id == task["task_type_id"]):
            break
        toExcludeIDs.append(id)

    # parse past tasks to check if they are done
    done = gazu.task.get_task_status_by_short_name("done")    
    if (len(toExcludeIDs) > 0):
        for id in toExcludeIDs:
            for tsk in tasksList:
                if id == tsk["task_type_id"]:
                    if tsk["task_status_id"] != done["id"]:
                        gazu.task.add_comment(task["id"], todo, messages.say(EVENTS_LANG, "cant_skip"))

def new_preview_callback (data):
    print("\nNew preview uploaded..\n")
    print(json.dumps(data))

    try:

        task_id = data["task_id"]
        print (f"task_id: {task_id}")

        prev_comm_id = data["comment_id"]
        prev_comm = gazu.task.get_comment(prev_comm_id)

        print ("preview comment item data:")
        print (json.dumps(prev_comm))

        prev_comm_status_id = prev_comm["task_status_id"]
        review_status = gazu.task.get_task_status_by_short_name(REVIEW_STATUS_CODE) 


        if prev_comm_status_id == review_status["id"]:
            print ("Review status already correctly set for new preview")
            return

        gazu.task.add_comment(task_id, review_status, messages.say(EVENTS_LANG, "preview_update"))


    except Exception as e:
        print ("Error processing automatic status change for new preview")
        print (e)
        return
    

    

# main callback - collection of callbacks
def callbacks(data):

    print("Task status changed - placeholder function..")

    # debug
    print(json.dumps(data))

    # if "rtw" not in excludeList:
    #     rtw(data)

    # if "delta" not in excludeList:
    #     delta(data)

    # if "lock" not in excludeList:
    #     lock(data)

# main
if __name__ == "__main__":
    event_client = gazu.events.init(logger=True)
    gazu.events.add_listener(event_client, "task:status-changed", callbacks)
    gazu.events.add_listener(event_client, "preview-file:add-file", new_preview_callback)
    gazu.events.run_client(event_client)
# prompts for task planning

# prompt for multiple plan generation
def generate_task_plans_prompt(scene_graph, user_input):
    template = f"""
    Mission : 
    You're tasked with generating plans to follow user's instruction.

    Input : 
    1. You'll receive a user's instruction which is a task you have to conduct.
    2. You'll receive a scene graph represented as a Python dictionary. Each key represents a workspace, and the corresponding value is a list of objects currently associated with that workspace. 

    Rules :
    1. You should make excellent plans to conduct user's instruction.
    2. You must only include objects and workspaces in the given scene graph in your plans.
    3. The plans can include moving objects to proper workspace.
    4. Make sure you conduct a task planning that accurately follow user's instruction. 
    5. If the target location in the user's instruction is not in the input scene graph, aim for the location in the scene graph that is most similar to the target location.

    Output :
    1. You'll output a plan to conduct user's instruction in form of sentences.
    2. You have to make a sufficient number of plans to follow user's instruction.

    Example :
    Input : 
    [USER INSTRUCTION]
    Move the study materials on the desk and move all the objects away from couch.

    [Scene Graph]
    {{'counter' : ['book','pencil'],
    'couch' : ['remote controller','apple'],
    'couch_1' : ['toy']
    'table' : ['potted plant','bowl','spoon'],
    'desk' : ['laptop','pillow']}}

    Information analysis :
    1. Workspace identification : I can see workspaces 'counter', 'couch', 'table', 'desk' in the scene graph.
    2. Objects identification :
    (1) 'book', 'pencil' in workspace 'counter'
    (2) 'remote controller', 'apple' in workspace 'couch'
    (3) 'toy' in workspace' 'couch_1'
    (3) 'potted plant', 'bowl', 'spoon' in workspace 'table'
    (4) 'laptop', 'pillow' in workspace 'desk'

    Reasoning :
    There are two missions to solve. First is to move the study materials on the desk, and second is to move all the objects away from couch.
    I'll divide these two missions and make plans to solve it.
    
    First mission : move the study materials on the desk
    This is how i think to solve the mission.
    'book', 'pencil', 'laptop' are study materials in the scene. -> 'book' and 'pencil' are in 'counter' currently. -> I should move them to 'desk'.
    -> 'laptop' is a study material too. -> It is currently on 'desk' so it is in the right place. -> It doesn't have to me moved.

    Second mission : move all the objects away from couch.
    This is how i think to solve the mission.
    There are 'remote controller' and 'apple' in couch. -> They should be moved to other workspaces -> 'remote controller' should be moved to 'table' since someone would use it in the future.
    -> 'apple' should be moved to 'counter' since it's a food ingredient. -> 'toy' is in couch_1 and 'toy' should also be moved to other workspaces -> 'toy' should be moved to 'table' that someone would use it in the future. 

    Output :
    Plan1. 
    Step1. The 'book' and 'pencil' are study materials so i should move them on the 'desk'.  
    Step2. 'laptop' is fine to be on the 'desk' since 'desk' is a general place for a 'laptop'. 
    step3. 'remote controller' should be moved away from 'couch' following the user instruction. I should move it to 'table'.
    step4. 'apple' should be moved away from 'couch' following the user instruction. I should move it to 'counter'.
    step5. 'toy' should be moved away from 'couch_1' following the user instruction. I should move it to 'table'.
    
    Plan2. 
    ...
    [User] 
    Input : 
    [USER INSTRUCTION]
    {user_input}

    [Scene Graph]  
    {scene_graph}

    Output : 
    Plan1.
    Plan2.
    Plan3.
    ...
    """
    return template

# prompt for converting plans to sequence of codes(action functions)
def generate_sub_task_codes_prompt(scene_graph, user_input, plans):
    template = f"""
    Mission : 
    You're tasked with generating sequence of sub-tasks in form of python codes with the action functions you can use to conduct a task given by user.

    Input : 
    1. You'll receive a user's instructions of a task
    2. You'll receive a scene graph represented as a Python dictionary. Each key represents a workspace, and the corresponding value is a list of objects currently associated with that workspace. 
    3. You'll receive plans consisted of steps to conduct the task.

    Action function :
    1. GoTo(object) : 'object' parameter can be either the name of 'workspace' or 'object' in the scene graph. The robot agent will go in front of the 'object' or 'workspace'.
    2. Pickup_Object(object) : 'object' parameter is the name of 'object' in scene graph. You'll pick up the object.
    3. Put_Object(object) : 'object' parameter is the name of 'object' in scene graph. You should go to a 'workspace' or 'object' first, then you'll put the holding object at the 'workspace' or near the 'object'.

    Output :
    1. You'll generate sequence of sub-tasks using the action function for each step of each plan.
    2. Make sure that you only include the Action functions mentioned. 
    
    Example :
    Input : 
    [USER INSTRUCTION]
    Move the study materials on the desk and move all the objects away from couch.

    [Scene Graph]
    {{'counter' : ['book','pencil'],
    'couch' : ['remote controller','apple'],
    'table' : ['potted plant','bowl','spoon'],
    'desk' : ['laptop','pillow']}}

    [Plan]
    Plan1. 
    Step1. The 'book' and 'pencil' are better to be on the 'desk'. Also, they should be near to each other since they are often used together.  
    Step2. I think 'remote controller' is fine to be on the 'couch'. 
    Step3. An 'apple' should not be on the couch. It's better to be on a counter.
    Step4. 'potted plant' is fine to be on the 'table' but it maybe better to be on the 'desk'. 
    Step5. 'bowl' is fine to be on the 'table' but maybe better to be on the 'counter' since someone might use it on counter.
    Step6. 'spoon' should be on the 'counter' since it will be easier for someone to find it near a 'counter'. Also it is better to be placed next to 'bowl' since they are generally used together. 
    Step7. 'laptop' is fine to be on the 'desk' since 'desk' is a general place for a 'laptop'. 
    Step8. 'pillow' being on a 'desk' is totally wrong. It should be moved on the 'couch' 
    
    Plan2. 

    [Output]
    Plan1.
    Step1. [GoTo(book), Pickup_Object(book), GoTo(desk), Put_Object(book), GoTo(pencil), Pickup_Object(pencil), GoTo(desk), Put_Object(pencil)] 
    Step2. [] 
    Step3. [GoTo(apple), Pickup_Object(book), GoTo(desk), Put_Object(book), GoTo(pencil), Pickup_Object(pencil), GoTo(desk), Put_Object(pencil)].
    Step4. [GoTo(potted plant), Pickup_Object(potted_plant),GoTo(desk),Put_Object(potted_plant)]
    Step5. [GoTo(bowl), Pickup_Object(bowl),GoTo(counter),Put_Object(bowl)]
    Step6. [GoTo(spoon), Pickup_Object(spoon),GoTo(bowl),Put_Object(spoon)]
    Step7. []
    Step8. [GoTo(pillow), Pickup_Object(pillow),GoTo(couch),Put_Object(pillow)]

    Plan2.

    [User] 
    Input : 
    [USER INSTRUCTION]
    {user_input}

    [Scene Graph]  
    {scene_graph}

    [Plan] :
    {plans} 
    """
    return template    

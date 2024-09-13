# prompts for scene graph generation

def ask_workspace_once_prompt(object_name): 
    template = f"""
    Mission :
    You have to identify a given object's workspace in the given image.
    Workspaces are bigger sets that contains objects which are areas or surfaces in the scene.
    The area or surface that objects bottom are contacted with are usually the workspace of objects.

    For example, if an apple is on the table and the bottom of the apple is contacted with the table, the table is the workspace of the apple.
    Also, if a bottle is inside a cabinet, the cabinet is the workspace of the bottle.
    
    What is a workspace of {object_name} in the scene?
    """
    return template

    def ask_spatial_relationship_once_prompt(object_name): # 한 물체의 near objects를 query함 :
    template = f"""
    Mission :
    You have to describe spatial relationships of a given object with other objects you see in the scene.
    
    What do you see near {object_name} in the scene?
    """
    return template    


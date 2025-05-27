class Impossible(Exception):
    """Exception raised when an action is impossible to be performed.
    
    The reason is given as the excpetion message
    """

class QuitWithoutSaving(SystemExit):
    """Can be raised to exit the game without automatic saves"""

    
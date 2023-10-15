from evennia import Command
from evennia import DefaultCharacter

# Define the status traits or titles
STATUS_TRAITS = ["Acknowledged", "Confirmed", "Established", "Privileged", "Honored", "Disgraced"]

class CmdGrantStatus(Command):
    """
    Grant a status to a character.
    
    Usage:
        @grantstatus <player> = <status>
    """
    key = "@grantstatus"
    locks = "cmd:perm(Admin)"
    
    def func(self):
        char = self.caller.search(self.lhs)
        if not char:
            return
        
        status = self.rhs.capitalize()
        if status not in STATUS_TRAITS:
            self.caller.msg(f"Invalid status. Valid statuses are: {', '.join(STATUS_TRAITS)}.")
            return
        
        # Save the status to the character.
        char.db.status = status
        self.caller.msg(f"Granted {char.name} the status of {status}.")
        char.msg(f"You have been granted the status of {status}.")

class CmdRevokeStatus(Command):
    """
    Revoke a status from a character.
    
    Usage:
        @revokestatus <player> = <status>
    """
    key = "@revokestatus"
    locks = "cmd:perm(Admin)"
    
    def func(self):
        char = self.caller.search(self.lhs)
        if not char:
            return
        
        status = self.rhs.capitalize()
        if status != char.db.status:
            self.caller.msg(f"{char.name} doesn't have the status {status}.")
            return
        
        # Remove the status from the character.
        del char.db.status
        self.caller.msg(f"Revoked the status of {status} from {char.name}.")
        char.msg(f"Your status of {status} has been revoked.")

# Adding commands to the default command set.
#from evennia import default_cmds
#class CommandSet(default_cmds.MuxCommandSet):
    #def at_cmdset_creation(self):
        #super().at_cmdset_creation()
        #self.add(CmdGrantStatus())
        #self.add(CmdRevokeStatus())

from evennia import Command
from evennia import DefaultCharacter
from evennia.utils import evtable

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

# Define age categories
AGES = ["Fledgling", "Neonate", "Ancilla", "Elder"]

class CmdSetStatus(Command):
    key = "@setstatus"
    locks = "cmd:perm(Admin)"
    
    def func(self):
        char = self.caller.search(self.lhs)
        if not char:
            return

        try:
            points = int(self.rhs)
            if 1 <= points <= 100:
                char.db.status_points = points
                self.caller.msg(f"Set {char.name}'s status points to {points}.")
            else:
                self.caller.msg("Status points should be between 1 and 100.")
        except ValueError:
            self.caller.msg("You must provide a number for status points.")

class CmdSetAge(Command):
    key = "@setage"
    locks = "cmd:perm(Admin)"
    
    def func(self):
        char = self.caller.search(self.lhs)
        if not char:
            return
        
        age = self.rhs.capitalize()
        if age in AGES:
            char.db.age = age
            self.caller.msg(f"Set {char.name}'s age to {age}.")
        else:
            self.caller.msg(f"Invalid age. Valid ages are: {', '.join(AGES)}.")

class CmdSetTitle(Command):
    key = "@settitle"
    locks = "cmd:perm(Admin)"
    
    def func(self):
        char = self.caller.search(self.lhs)
        if not char:
            return
        
        title = self.rhs
        char.db.title = title
        self.caller.msg(f"Set {char.name}'s title to {title}.")

class CmdAdjustStatus(Command):
    key = "@adjuststatus"
    
    def func(self):
        target_char = self.caller.search(self.lhs)
        if not target_char:
            return

        points, reason = self.rhs.split("/", 1)
        try:
            points = int(points)
            if abs(points) > self.caller.db.status_points:
                self.caller.msg("You don't have enough status points to make this adjustment.")
                return
            target_char.db.status_points += points
            self.caller.msg(f"Adjusted {target_char.name}'s status by {points} points for: {reason}")
        except ValueError:
            self.caller.msg("You must provide a number for status points and a reason.")

class CmdViewStatus(Command):
    key = "@viewstatus"
    
    def func(self):
        table = evtable.EvTable("Name", "Age", "Title", "Status Points", width=80)
        for char in self.caller.location.contents:
            if char.has_account:  # Checks if the object is a character
                name = char.name
                age = char.db.age or "Unknown"
                title = char.db.title or "None"
                points = char.db.status_points or 0
                table.add_row(name, age, title, str(points))
        self.caller.msg(str(table))

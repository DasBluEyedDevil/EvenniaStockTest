from evennia import default_cmds
from .status_cmds import CmdGrantStatus, CmdRevokeStatus, CmdSetStatus, CmdSetAge, CmdSetTitle, CmdAdjustStatus, CmdViewStatus

class StatusCmdSet(StatusCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdGrantStatus())
        self.add(CmdRevokeStatus())
        self.add(CmdSetStatus())
        self.add(CmdSetAge())
        self.add(CmdSetTitle())
        self.add(CmdAdjustStatus())
        self.add(CmdViewStatus())

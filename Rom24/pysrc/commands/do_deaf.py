import logging
import state_checks

logger = logging.getLogger()

import merc
import interp


# RT deaf blocks out all shouts
def do_deaf(ch, argument):
    if state_checks.IS_SET(ch.comm, merc.COMM_DEAF):
        ch.send("You can now hear tells again.\n")
        state_checks.REMOVE_BIT(ch.comm, merc.COMM_DEAF)
    else:
        ch.send("From now on, you won't hear tells.\n")
        state_checks.SET_BIT(ch.comm, merc.COMM_DEAF)


interp.register_command(interp.cmd_type('deaf', do_deaf, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


__all__ = ["TerminalColorFormatter"]


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = tuple(range(8))

# The background is set with 40 plus the number of the color,
# and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace(
            "$BOLD",
            BOLD_SEQ
        )
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': WHITE,
    'ERROR': RED
}


class TerminalColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        text = super(TerminalColorFormatter, self).format(record)
        if record.levelname in COLORS:
            return COLOR_SEQ % (
                30 + COLORS[levelname]
            ) + text + RESET_SEQ
        else:
            return text


# vim: set tw=79 :

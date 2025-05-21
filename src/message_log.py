from typing import Iterable, List, Reversible, Tuple
import textwrap

import tcod

import colors

class Message: 
    def __init__(self, text: str, foreground_color: Tuple[int, int, int]):
        self.plain_text = text
        self.foreground_color = foreground_color
        self.count = 1

    @property
    def full_text(self) -> str:
        """The full text of this message, including the count if necessary."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text
    

class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
            self, text:str, foreground_color: Tuple[int, int, int] = colors.white, *, stack:bool = True,
    ) -> None:
        """Add a message to this log.
        'text' is the message text, foreground_color is the text color.
        If 'stack' is true, then the message can stack with a previous message of the same text."""
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count+=1
        else:
            self.messages.append(Message(text,foreground_color))
    
    def render(
            self, console:tcod.Console, x:int, y:int, width: int, height: int,
    ) -> None:
        """Render this log over a given area.
        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`.
        """

        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Return a wrapped text message"""
        for line in string.splitlines(): #handle newlines in messages
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )
    @classmethod
    def render_messages(
        cls, #TODO write this in big words
        console:tcod.Console,
        x:int,
        y:int,
        width:int,
        height:int,
        messages: Reversible[Message],
    ) -> None:
        """Render the messages provided.
        The messages are rendered starting at the last and working backwards, using Reversible
        """
        y_offset = height -1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x,y=y+y_offset, string=line, fg = message.foreground_color)
                y_offset-=1
                if y_offset < 0:
                    return
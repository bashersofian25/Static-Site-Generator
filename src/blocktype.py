from enum import Enum


class BlockType(Enum):
    PARAGRAPH="p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST= "ul" 
    ORDERED_LIST = "ol"
import re
import unicodedata

# Regex to match full emoji grapheme clusters:
# 1. Keycap sequences (e.g. 1️⃣, #️⃣, *️⃣)
# 2. Regional indicator pairs for country flags (e.g. 🇺🇸, 🇯🇵)
# 3. Tag sequences for subdivision flags (e.g. Scotland 🏴󠁧󠁢󠁳󠁣󠁴󠁿)
# 4. Emoji sequences including ZWJ chains, skin tone modifiers, and variation selectors
# 5. Characters with emoji presentation selector (\uFE0F)
_EMOJI_SEQUENCE_RE = re.compile(
    r"""
    # Keycap sequence
    [0-9#*]\uFE0F?\u20E3
    |
    # Regional indicator pair (Flags)
    [\U0001F1E6-\U0001F1FF]{2}
    |
    # Tag sequence (e.g. subdivision flags like Scotland)
    \U0001F3F4[\U000E0020-\U000E007E]+\U000E007F
    |
    # ZWJ sequence or modified emoji
    (?:
        [\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\U00002B55\U0000231A\U0000231B\U000023E9-\U000023EC\U000023F0\U000023F3\U000025FD\U000025FE\U0000203C\U00002049\U00002122\U00002139\U00002194-\U00002199\U000021A9\U000021AA\U00002934\U00002935\U00002B05-\U00002B07\U00002B1B\U00002B1C\U00003030\U0000303D\U00003297\U00003299]
        [\U0001F3FB-\U0001F3FF]?
        \uFE0F?
    )
    (?:
        \u200D
        (?:
            [\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\U00002B55\U0000231A\U0000231B\U000023E9-\U000023EC\U000023F0\U000023F3\U000025FD\U000025FE\U0000203C\U00002049\U00002122\U00002139\U00002194-\U00002199\U000021A9\U000021AA\U00002934\U00002935\U00002B05-\U00002B07\U00002B1B\U00002B1C\U00003030\U0000303D\U00003297\U00003299]
            [\U0001F3FB-\U0001F3FF]?
            \uFE0F?
        )
    )*
    |
    # Any symbol followed by emoji presentation selector VS16
    .\uFE0F
    """,
    re.VERBOSE,
)


class Table:
    """
    A simple ASCII table generator.

    Args:
        data (List[List[str|int]]): A 2D list representing table headers and rows.
    """

    def __init__(self, data):
        self.header = data[0]
        self.rows = data[1:]
        self.data = data
        for i, row in enumerate(self.rows):
            if len(row) != self.col_num:
                raise ValueError(
                    f"Row {i+1} has {len(row)} columns, expected {self.col_num}"
                )

    @property
    def col_num(self):
        """Number of columns"""
        return len(self.header)

    @property
    def col_width(self):
        "Width of each column"
        return [[self._len(str(d[i])) for d in self.data] for i in range(self.col_num)] 
    
    @staticmethod
    def _char_width(char: str) -> int:
        """Width of a single non-emoji code point."""
        cp = ord(char)
        # Skip zero-width characters (format chars, zero-width space/joiner, variation selectors)
        if cp in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF) or 0xFE00 <= cp <= 0xFE0F or 0x20E0 <= cp <= 0x20FF:
            return 0
        cat = unicodedata.category(char)
        # Combining marks and format control characters have 0 width
        if cat in ("Mn", "Me", "Cf"):
            return 0
        # Wide, fullwidth, and ambiguous characters occupy 2 columns
        if unicodedata.east_asian_width(char) in ("F", "W", "A"):
            return 2
        return 1

    def _len(self, text: str) -> int:
        """Visual display width of text taking emojis and multi-codepoint sequences into account."""
        width = 0
        last_end = 0
        for match in _EMOJI_SEQUENCE_RE.finditer(text):
            start, end = match.span()
            for char in text[last_end:start]:
                width += self._char_width(char)
            width += 2
            last_end = end

        for char in text[last_end:]:
            width += self._char_width(char)

        return width
    
    def _pad(self, text: str, width: int) -> str:
        "Pad text to visual width using spaces"
        visual_len = self._len(text)
        if visual_len >= width:
            return text
        return text + " " * (width - visual_len)
    
    def create(self) -> str:
        """Creates the table"""
        output = []
        col_widths = []
        width = self.col_num - 1
        
        for i in range(self.col_num):
            col_w = [self._len(str(d[i])) for d in self.data]
            mx_w = max(col_w)
            col_widths.append(mx_w)
            width += mx_w + 2

        output.append("+" + "-" * width + "+")
        
        cells = []
        for i, header in enumerate(self.header):
            cells.append(" " + self._pad(str(header), col_widths[i]) + " ")
        output.append("|" + "|".join(cells) + "|")
        
        output.append("|" + "-" * width + "|")

        for row in self.rows:
            cells = []
            for i, cell in enumerate(row):
                cells.append(" " + self._pad(str(cell), col_widths[i]) + " ")
            output.append("|" + "|".join(cells) + "|")

        output.append("+" + "-" * width + "+")
        return '\n'.join(output)

    def display(self):
        """Prints the table"""
        return print(self.create())


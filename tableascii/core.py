import unicodedata

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
    
    def _len(self, text: str) -> int:
        width = 0
        for char in text:
            cp = ord(char)
            # Skip zero-width characters (combining marks, variation selectors, ZWJ)
            if cp in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF) or 0xFE00 <= cp <= 0xFE0F or 0x20E0 <= cp <= 0x20FF:
                continue
            # Non-BMP characters (most emojis) are typically 2 columns wide
            if cp >= 0x10000:
                width += 2
            # Emoji and symbol blocks in BMP
            elif (0x2600 <= cp <= 0x27BF or
                  0x1F300 <= cp <= 0x1F9FF or
                  0x1FA00 <= cp <= 0x1FAFF):
                width += 2
            elif unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
                width += 2
            else:
                width += 1
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


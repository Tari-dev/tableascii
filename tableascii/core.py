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
        self.width = self.col_num - 1

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
            width += 2 if unicodedata.east_asian_width(char) in ('F', 'W', 'A') else 1
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
        
        for i in range(self.col_num):
            col_w = [self._len(str(d[i])) for d in self.data]
            mx_w = max(col_w)
            col_widths.append(mx_w)
            self.width += mx_w + 2

        output.append("+" + "-" * self.width + "+")
        
        cells = []
        for i, header in enumerate(self.header):
            cells.append(" " + self._pad(str(header), col_widths[i]) + " ")
        output.append("|" + "|".join(cells) + "|")
        
        output.append("|" + "-" * self.width + "|")

        for row in self.rows:
            cells = []
            for i, cell in enumerate(row):
                cells.append(" " + self._pad(str(cell), col_widths[i]) + " ")
            output.append("|" + "|".join(cells) + "|")

        output.append("+" + "-" * self.width + "+")
        return '\n'.join(output)

    def display(self):
        """Prints the table"""
        return print(self.create())


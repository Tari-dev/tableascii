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
        # self.columns = [[d[i] for d in data] for i in range(self.col_num)]
        self.width = self.col_num - 1

    @property
    def col_num(self):
        """Number of columns"""
        return len(self.header)

    @property
    def col_width(self):
        "Width of each column"
        return [[len(str(d[i])) for d in self.data] for i in range(self.col_num)]

    def create(self) -> str:
        """Creates the table"""
        output = []
        c = {}
        for i, col_w in enumerate(self.col_width):
            mx_w = max(col_w)
            c[f'c_{i+1}'] = mx_w
            self.width += mx_w + 2

        output.append("+" + "-" * self.width + "+")
        row_fmt = "| " + " | ".join(["{:<{c_%d}}" % (i + 1) for i in range(self.col_num)]) + " |"
        output.append(row_fmt.format(*self.header, **c))
        output.append("|" + "-" * self.width + "|")

        for row in self.rows:
            row_fmt = "| " + " | ".join(["{:<{c_%d}}" % (i + 1) for i in range(self.col_num)]) + " |"
            output.append(row_fmt.format(*row, **c))

        output.append("+" + "-" * self.width + "+")

        return '\n'.join(output)

    def display(self):
        """Prints the table"""
        return print(self.create())

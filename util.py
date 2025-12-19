BOX_HORIZONTAL = "─"
BOX_VERTICAL = "│"
BOX_DOWN_AND_RIGHT = "┌"
BOX_DOWN_AND_LEFT = "┐"
BOX_UP_AND_RIGHT = "└"
BOX_UP_AND_LEFT = "┘"
BOX_VERTICAL_AND_RIGHT = "├"
BOX_VERTICAL_AND_LEFT = "┤"
BOX_DOWN_AND_HORIZONTAL = "┬"
BOX_UP_AND_HORIZONTAL = "┴"
BOX_VERTICAL_AND_HORIZONTAL = "┼"

def grid_str(values):
    string_values = [[str(cell) for cell in row] for row in values]
    rotated = zip(*string_values)
    column_widths = [max([max([len(w) for w in cell.split('\n')] + [0]) for cell in col]) for col in rotated]
    row_heights = [max([max([len(cell.split('\n'))]) for cell in row] + [0]) for row in string_values]
    string_builder = ''
    for i, row in enumerate(string_values):
        # Fill extra row things
        sub_rows = [['' for _ in row] for _ in range(row_heights[i])]
        for i2, cell in enumerate(row):
            sub_cells = cell.split('\n')
            for j2, s_cell in enumerate(sub_cells):
                sub_rows[j2][i2] = s_cell
        string_builder += '\n'.join([get_row_text(sub_row, column_widths) for sub_row in sub_rows]) + '\n'
        if i != len(string_values) - 1:
            string_builder += get_divider(column_widths) + '\n'
    return string_builder


def markdown_table(matrix):
    header_line = [':-:' for _ in matrix[0]]
    matrix.insert(1, header_line)
    cells = '\n'.join(['| ' + ' | '.join([str(cell) for cell in row]) + ' |' for row in matrix])
    return cells


def get_row_text(row, widths):
    return ' ' + f' {BOX_VERTICAL} '.join([cell.center(col_width) for cell, col_width in zip(row, widths)]) + ' '


def get_divider(widths):
    return BOX_HORIZONTAL + f'{BOX_HORIZONTAL}{BOX_VERTICAL_AND_HORIZONTAL}{BOX_HORIZONTAL}'.join(
        [BOX_HORIZONTAL * w for w in widths]) + BOX_HORIZONTAL


def print_adjacent(multiline_string1, multiline_string2):
    lines1 = multiline_string1.split('\n')
    lines2 = multiline_string2.split('\n')
    # Fill the lists
    max_height = max(len(lines1), len(lines2))
    lines1 += [''] * (max_height - len(lines1))
    lines2 += [''] * (max_height - len(lines2))

    max_length = max([len(line) for line in lines1])
    for l, r in zip(lines1, lines2):
        print(f'{l.ljust(max_length)} {r}')

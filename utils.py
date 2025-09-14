def read_file(file_path : str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def save_file(content: str, filename: str) -> None:
    with open(filename, "w") as file:
        file.write(content)


# Create a Markdown table from a 2D array (matrix) and a list of item names
# The table includes only the upper triangle and diagonal of the matrix (symmetric matrix)
def array_to_markdown_table(matrix : list[list[float]], items: list[str]) -> str:
    # Create the header row
    header = "|       | " + " | ".join([items[i].replace(".soil", "") + str((i+1)) for i in range(len(matrix[0]))]) + " |"
    
    # Create the separator row
    separator = "|-------|" + "|".join(["---"] * len(matrix[0])) + "|"
    
    # Create the data rows
    data_rows = list[str]()
    for i, row in enumerate(matrix):
        data_row = ["**" + items[i].replace(".soil", "") + str((i+1)) + "**"]  # Add row name
        for j, cell in enumerate(row):
            if j >= i:  # Include diagonal and upper triangle
                data_row.append("{:.6f}".format(cell))
            else:  # Leave lower triangle empty
                data_row.append("")
        data_row = "| " + " | ".join(data_row) + " |"
        data_rows.append(data_row)
    
    # Combine all rows into the final Markdown table
    markdown_table = "\n".join([header, separator] + data_rows)
    
    return markdown_table 
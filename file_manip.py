def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def read_from_file(filename) -> list:
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines) - 1):
            if lines[i][-1] == '\n':
                lines[i] = lines[i][:-1]
        if lines[-1][-1] == '\n': # If ends with a new line character, remove it and then just append '' to the returned list
            lines[-1] = lines[-1][:-1]
            lines.append('')
        return lines
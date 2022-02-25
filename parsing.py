import os
import sys

file_name = sys.argv[1]
file_arg = open(f"{file_name}")

counter = 0

variables_dict = {}

new_text = ''



def space_remove(line):
    line = ' '.join(line.split())

    return line


def var_announce(line,line_number, counter):
    global new_text

    line = line.replace("var", "")
    line = line.replace(":", "")
    line = "".join(line.split())

    var_name = line[:line.find('=') ]
    var_value = line[line.find('=') + 1:]
    variables_dict[var_name] = eval(var_value)

    new_text += "\t" * counter + f"{line}\n"

    return line_number + 1


def writing(line,line_number,counter):
    global new_text

    line = line.replace("write", "print")
    line = line.replace(":", "")

    new_text += "\t" * counter + f"{line}\n"

    return line_number + 1


def if_statement(line, line_number, counter):
    global new_text

    statement = line + ':'

    new_text += f"{statement}\n"

    if_body = []

    for j in range(line_number, len(file_list)):
        line = file_list[j]
        line = "".join(line.split())

        if len(line.strip()) == 0:
            continue

        if line[0] == "[":
            while line[-1] != "]":
                if_body.append(line)
                j += 1
                line = file_list[j]

            if_body.append(line)

            line_counter = 0

            if_body[0] = if_body[0].replace('[', '')
            if len(if_body[0] ) == 0:
                line_counter += 1
                del if_body[0]

            if_body[-1] = if_body[-1].replace(']', '')
            if len(if_body[-1] ) == 0:
                line_counter += 1
                del if_body[-1]


            for row_index, row in enumerate(if_body):
                check = syntax_check(row, row_index + line_number + line_counter, counter)
                if check == -1:
                    break
            if check == -1:
                return -1
            else:
                return j + 1

        else:
            print("Syntax error in if body")
            return -1


def for_loop(line,line_number, counter):
    global new_text

    var_name = line[line.index('(') + 1: line.index('=')]

    start_value = eval(line[line.index('=') + 1:line.index(':')])
    end_value = eval(line[line.index(var_name, 5) + len(var_name) + 1: line.rfind(":")])
    step = eval(line[line.rfind(":") + 1:line.index(")")])

    loop_statement = f"for {var_name} in range ({start_value},{end_value},{step}):"

    new_text += f"{loop_statement}\n"

    for_body = []

    for j in range(line_number, len(file_list)):
        line = file_list[j]

        if len(line.strip()) == 0:
            continue

        if line[0] == "[":
            while line[-1] != "]":
                for_body.append(line)
                j += 1
                line = file_list[j]

            for_body.append(line)

            line_counter = 0

            for_body[0] = for_body[0].replace('[', '')
            if len(for_body[0]) == 0:
                line_counter += 1
                del for_body[0]

            for_body[-1] = for_body[-1].replace(']', '')
            if len(for_body[-1]) == 0:
                line_counter += 1
                del for_body[-1]


            for row_index, row in enumerate(for_body):
                check = syntax_check(row, row_index + line_number + line_counter, counter)
                if check == -1:
                    break
            if check == -1:
                return -1
            else:
                return j + 1

        else:
            print("Syntax error in for body")
            return -1


def revalue(line,line_number,counter):
    global new_text

    new_text += "\t" * counter + f"{line}\n"

    return line_number + 1


def syntax_check(line, i, counter):

    if len(line.strip()) == 0:
        i += 1
        return  i

    if line[:3] == "var":
        if line[3] == " " and line.count("=") == 1 and line[-1] == ":":
            return var_announce(line,i,counter)

        else:
            print("Syntax error in variable announcement")
            return -1

    elif line[:5] == "write":
        line = ''.join(line.split())

        if line[5] == "(" and line[-2] == ")" and line[-1] == ":":
            return writing(line,i,counter)
        else:
            print("Syntax error in write function")
            return -1


    elif line[:2] == "if":
        line = ''.join(line.split())

        if line[2] == "(" and line[-1] == ")":
            counter += 1
            i += 1
            new_index = if_statement(line, i, counter)

            counter -= 1

            return new_index

        else:
            print("Syntax error in if statement")
            return -1


    elif line[:3] == "for":
        line = ''.join(line.split())

        if line[3] == "(" and line.count(':') == 2 and line[-1] == ")":
            counter += 1
            i += 1
            new_index = for_loop(line,i,counter)

            counter -= 1

            return new_index

        else:
            print("Syntax error in for loop")
            return -1


    elif line[:3] != "var" and line.count("=") == 1 and line[-1] == ":":
        line = ''.join(line.split())
        line = line.replace(":", "")

        name = line[:line.find('=')]
        value = line[line.find('=') + 1:len(line)]

        if name in variables_dict.keys():
            variables_dict[name] = eval(value)
            return revalue(line, i,counter)

        else:
            print("Announce variable first")
            return -1

    else:
        print("Syntax error")
        return -1


file_list = []

for line in file_arg:
    file_list.append(line.strip())

i = 0

file_open = True

while i < len(file_list):
    line = file_list[i]
    i = syntax_check(line, i, counter)

    if i == -1:
        file_open = False
        break

    else:
        continue


if file_open:
    python_file = open('python_script.cv', 'w+')
    python_file.write(new_text)
    python_file.seek(0)
    os.system('python python_script.cv')

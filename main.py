import line as track_line
import time

lines = {}

command_file = open('commands.txt', 'r')
commands = command_file.readlines()

commands = list(filter(lambda s: s[0] != "#", commands))

setup_command = commands.pop(0).split(" ")
for x in range(len(setup_command)):
	lines[setup_command[x].strip()] = track_line.Line(x)
	lines[setup_command[x].strip()].setup()


def parseCommand(command):
	if ":" in command:
		return [
			command.split(" ")[0],
			command.split(":")[0].replace(
				command.split(" ")[0], "").strip().split(" "),
			command.split(":")[1].strip().split(" ")
		]
	else:
		return [
			command.split(" ")[0],
			command.split(":")[0].replace(
				command.split(" ")[0], "").strip().split(" "),
			""
		]


while len(commands) > 0:
	n = 0
	while n < 5 and n < len(commands):
		parsed_command = parseCommand(commands[n])
		if commands[0].strip() == "step":
			commands.pop(0)
			lines[list(lines)[0]].doCommand("straight", lines)
			break

		elif commands[n].strip() == "step":
			break

		elif all([(com in lines) for com in parsed_command[1]]):
			if all([not lines[line_name].touched for line_name in parsed_command[1]]):
				lines[parsed_command[1][0]].doCommand(parsed_command, lines)
				commands.pop(n)

			else:
				n += 1

		else:
			n += 1

		for line in parsed_command[1]:
			if line in lines:
				lines[line].touched = True

	for line in lines:
		if not lines[line].touched:
			lines[line].doCommand(["straight"], lines)
		lines[line].touched = False

	top = max([lines[line].pen.ycor() for line in lines])
	for line in lines:
		lines[line].pen.goto(lines[line].pen.xcor(), top)

lines[list(lines)[0]].updateCanvas()

time.sleep(999)

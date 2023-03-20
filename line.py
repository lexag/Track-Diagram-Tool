from turtle import *
from PIL import EpsImagePlugin, Image
EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.54.0\bin'
import io

class Line:
	def __init__(self, order, step = 0):
		self.order = int(order)
		self.pen = Turtle(visible=False)
		self.pen.left(90)
		self.pen.speed(0)
		self.touched = False
		self.step = step
		self.pen.getscreen().tracer(0, 0)


	def setup(self, draw = False):
		if not draw:
			self.pen.penup()
		self.pen.goto(self.order * 10, self.step * 10)
		if not draw:
			self.pen.pendown()

	def doCommand(self, parsed_command, lines):
		self.step += 1
		match parsed_command[0]:
			case "start":
				self.pen.right(90)
				self.pen.forward(4)
				self.pen.back(8)
				self.pen.forward(4)
				self.pen.left(90)
				self.pen.forward(10)

			case "end":
				self.pen.forward(10)
				self.pen.right(90)
				self.pen.forward(4)
				self.pen.back(8)
				self.pen.forward(4)
				self.pen.left(90)
				del lines[parsed_command[1][0]]

			case "straight":
				self.pen.forward(10)

			case "split":
				nl = parsed_command[2][1]
				match parsed_command[2][0]:
					case "left":
						for line in lines:
							if lines[line].order < self.order:
								lines[line].scoot(-1)
						lines[nl] = Line(self.order - 1, step=self.step)
						

					case "right":
						for line in lines:
							if lines[line].order > self.order:
								lines[line].scoot(1)
						lines[nl] = Line(self.order + 1, step=self.step)
						
				lines[nl].pen.penup()
				lines[nl].pen.goto(self.pen.position())
				lines[nl].pen.pendown()
				lines[nl].pen.goto(
					lines[nl].pen.xcor(),
					self.pen.ycor() + 10
				)
				lines[nl].touched = True
				self.pen.forward(10)
			
			case "slip":
				clone = self.pen.clone()
				if lines[parsed_command[1][1]].order > self.order:
					clone.right(45)
					clone.forward(14.1421356)
					clone.left(45)
				else:
					clone.left(45)
					clone.forward(14.1421356)
					clone.right(45)
				clone.hideturtle()

			case "merge":
				self.pen.goto(
					lines[parsed_command[1][1]].pen.xcor(),
					self.pen.ycor() + 10)
				del lines[parsed_command[1][0]]

			case "name":
				lines[parsed_command[2][0]] = lines[parsed_command[1][0]]
				del lines[parsed_command[1][0]]



	def scoot(self, amount):
		self.order += amount
		self.pen.goto(self.pen.xcor() + amount * 10, self.pen.ycor() + 10)
		self.touched = True


	def updateCanvas(self):
		self.pen.getscreen().update()
		# ps = self.pen.getscreen().getcanvas().postscript(colormode="color", file="output.ps")
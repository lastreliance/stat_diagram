import turtle
from typing import List, Tuple, Union


class Diagram:
    offset: Tuple[int, int] = (-300, -280)
    screensize = (800, 650)
    size = (600, 500)
    max_points = 100
    with_points = True
    point_scale = 0.18

    # noinspection PyTypeChecker
    def __init__(self,
                 max_val: Union[float, None] = None,
                 min_val: Union[float, None] = None):
        self.certain_values = (max_val is not None), (min_val is not None)
        self.max_val = max_val
        self.min_val = min_val

        if all(self.certain_values):
            if max_val <= min_val:
                raise ValueError("max value should be greater than min value!")

        self.pen: turtle.Turtle = None
        self.window: turtle.Screen = None
        self.points: List[float] = list()
        self.active = False

    def init_screen(self):
        if self.active:
            return
        self.active = True
        self.pen = turtle.Turtle()
        self.window = turtle.Screen()
        self.window.title(f"Diagram {__name__}")
        self.window.tracer(0)
        self.window.setup(*Diagram.screensize)

    def add(self, point: float):
        if self.max_val is None:
            self.max_val = point
        if self.min_val is None:
            self.min_val = point

        if point > self.max_val and not self.certain_values[0]:
            self.max_val = point
        elif point < self.min_val and not self.certain_values[1]:
            self.min_val = point
        else:
            raise ValueError(f"\"point\" parameter should be in given range. ('min_val, max_val' params)\ngiven: "
                             f"min_val={self.min_val}, max_val={self.max_val}")

        if all(self.certain_values):
            self.points.append((point - self.min_val) / (self.max_val - self.min_val))
        else:
            self.points.append(point)

    def reweigh_points(self):
        diff = self.max_val - self.min_val
        for i in range(len(self.points)):
            self.points[i] = (self.points[i] - self.min_val) / diff

    def display(self):
        if not len(self.points):
            raise ValueError("No points to display")
        if not all(self.certain_values):
            self.reweigh_points()
        self.init_screen()
        self.pen.clear()
        self.draw_plane()
        self.draw_average()

        # setting up
        self.pen.width(2)
        self.pen.color("red")
        self.set_pos(0, Diagram.size[1] * self.points[0])
        self.pen.shape("circle")
        self.pen.shapesize(Diagram.point_scale, Diagram.point_scale)
        self.pen.stamp()
        self.pen.down()
        self.window.tracer(0)

        if len(self.points) > Diagram.max_points:
            index = int()
            step = (len(self.points) - 1) / Diagram.max_points
            x_cor_step = Diagram.size[0] / Diagram.max_points
            x_cor = x_cor_step
            for i in range(1, Diagram.max_points + 1):
                index += step
                self.goto(x_cor, Diagram.size[1] * self.points[round(index)])
                if Diagram.with_points:
                    self.pen.stamp()
                x_cor += x_cor_step
        else:
            step = Diagram.size[0] / (len(self.points) - 1)
            x_cor = step
            for point in self.points[1:]:
                self.goto(x_cor, Diagram.size[1] * point)
                if Diagram.with_points:
                    self.pen.stamp()
                x_cor += step

        self.window.update()

        # writing average below diagram
        self.set_pos(0, -30)
        self.pen.color('black')
        average = sum(self.points) / len(self.points)
        average = round(100 * average, 2)
        self.pen.write(f"Average: {average}")

        self.reset()

        self.window.mainloop()

    def draw_average(self):
        self.reset()
        self.pen.color("green")
        self.set_pos(0, Diagram.size[1] * self.points[0])
        average_points = list()

        if len(self.points) < Diagram.max_points:
            step = Diagram.size[0] / len(self.points)
            x_cor = step
            for i in range(1, len(self.points) + 1):
                y = sum(self.points[:i + 1]) / (i + 1)  # ((self.points[i] + self.points[i - 1]) / 2)
                average_points.append((x_cor, y * Diagram.size[1]))
                x_cor += step
        else:
            step = Diagram.size[0] / Diagram.max_points
            x_cor = step
            ind_step = (len(self.points) - 1) / Diagram.max_points
            index = ind_step
            for i in range(1, Diagram.max_points):
                point_ind = round(index)
                y = (self.points[point_ind] + self.points[point_ind - 1]) / 2
                average_points.append((x_cor, y * Diagram.size[1]))
                index += ind_step
                x_cor += step

        for x, y in average_points:
            self.goto(x, y)
            # self.pen.stamp()

    def goto(self, x: float, y: float):
        self.pen.goto(*self.coordinates(x, y))

    def set_pos(self, x, y):
        if self.pen.isdown():
            self.pen.up()
            self.goto(x, y)
            self.pen.down()
        else:
            self.goto(x, y)

    def reset(self):
        self.set_pos(0, 0)

    def draw_plane(self):
        self.init_screen()
        pen = self.pen
        height_share = 10
        width_share = 15

        def draw_line():
            heading = pen.heading()
            width = pen.width()
            line_color = pen.color()
            pen.setheading(0)
            pen.color("grey")
            pen.width(1)
            pen.back(5)
            pen.forward(Diagram.size[0] + 5)
            pen.back(Diagram.size[0])
            pen.setheading(heading)
            pen.width(width)
            pen.color(*line_color)

        def draw_mark():
            mark_length = 6

            pen.width(1)
            pen.left(90)
            pen.forward(mark_length / 2)
            pen.back(mark_length)
            pen.left(180)
            pen.back(mark_length / 2)
            pen.left(90)
            pen.width(2)

        self.reset()
        pen.shape("classic")
        pen.down()

        pen.setheading(90)
        pen.width(2)
        pen.color("black")
        pen.write(str(round(self.min_val, 2)) + " ", align="right")
        height = Diagram.size[1]
        step = height // height_share
        share = self.min_val
        for i in range(0, height, step):
            share += (self.max_val - self.min_val) / 10
            pen.forward(step)
            pen.write(str(round(share, 2)) + " ", align="right")

            draw_line()

        pen.forward(step / 2)
        pen.stamp()

        self.reset()

        pen.setheading(0)
        length = Diagram.size[0]

        step = length // width_share
        part = len(self.points) / width_share
        for i in range(0, length, step):
            pen.forward(step)
            pen.write(round(part), align="left")
            part += len(self.points) / width_share
            draw_mark()

        pen.setheading(90)
        pen.color("grey")
        pen.width(1)
        pen.forward(Diagram.size[1])
        pen.back(Diagram.size[1])
        pen.setheading(0)
        pen.color("black")
        pen.width(2)

        pen.forward(step / 2)
        pen.stamp()
        self.reset()

        self.window.update()

    def clear(self):
        self.pen.reset()

    @staticmethod
    def coordinates(x: float, y: float) -> Tuple[float, float]:
        x += Diagram.offset[0]
        y += Diagram.offset[1]
        return x, y

    def cancel(self):
        self.pen.clear()


if __name__ == "__main__":
    diagram = Diagram()
    diagram.display()
    diagram.window.mainloop()

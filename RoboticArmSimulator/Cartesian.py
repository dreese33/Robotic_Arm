from RoboticArmSimulator.Point import Point


class Cartesian:

    @staticmethod
    def computer_to_cartesian(computer_coordinate, shape_width, canvas) -> Point:
        if computer_coordinate.y >= 0:
            y_coordinate = int(canvas['height']) / 2 - computer_coordinate.y
        else:
            y_coordinate = int(canvas['height']) - computer_coordinate.y

        return Point(computer_coordinate.x - shape_width / 2, y_coordinate)

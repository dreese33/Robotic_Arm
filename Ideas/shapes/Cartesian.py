
class Cartesian:

    @staticmethod
    def computer_to_cartesian(computer_coordinate, canvas):
        if computer_coordinate[1] >= 0:
            y_coordinate = float(canvas['height']) / 2 - computer_coordinate[1]
        else:
            y_coordinate = float(canvas['height']) - computer_coordinate[1]

        return computer_coordinate[0] - float(canvas['width']) / 2, y_coordinate

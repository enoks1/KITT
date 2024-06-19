from functions import *

class localization:
    def __init__(self, recording):
        self.recording = recording

    def locate(self):
        locations = locate(self.recording).flatten()
        locations = (locations[0], locations[1])
        x = locations[0]
        y = locations[1]

        # # x
        # x_tmp = x - 0.08

        # x_error = 0.102181818
        # x_bound = x - x_error

        # # y
        # y_tmp = y

        # y_error = 0.110545455
        # y_bound = y - y_error

        # # bounds for x 
        # if x_bound > 2.4 and y_bound < 2.4:
        #     x_tmp = x_tmp - 0.05
        # else:
        #     x_tmp = x_tmp

        # if y_bound > 2.3:
        #     x_tmp = x_tmp + 0.06
        # else:
        #     x_tmp = x_tmp

        # # bounds for y
        # if x_bound < 3.4 and y < 1.4:
        #     y_tmp = y_tmp - 0.08
        # else:
        #     y_tmp = y_tmp

        # if x_bound > 3.4 and y < 1.4:
        #     y_tmp = y_tmp + 0.15
        # else:
        #     y_tmp = y_tmp

        return (x, y)
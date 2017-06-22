from random import shuffle, randint
from datetime import datetime


class OzoneData:
    def __init__(self, ):
        self.xx = [datetime.now().strftime("%H:%M:%S") for x in range(60)]
        yy = [48.0, ]
        for i in range(59):
            yy.append(yy[-1] + 0.5 * randint(-2, 2))
        self.yy = yy

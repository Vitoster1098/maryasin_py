class Relay:
    def __init__(self):
        self.deadzone = 0.2
        pass

    def getOutput(self, actual: float, setpoint: float):
        error = setpoint - actual
        if error >= self.deadzone:
            output = 10
        elif error >= -self.deadzone and error <= self.deadzone:
            output = 0
        else:
            output = 0
        return output


if __name__ == '__main__':
    rel = Relay()
    k = 1.0
    T = 1.0
    dt = 0.1
    u = 0
    r = 0
    y = 0
    y1 = 0

    print("Target\tOutput\tControl\tError")

    for i in range(100):
        if i == 20:
            r = 1

        u = rel.getOutput(y1, r)
        y1 = k * dt / T * u + (T - dt) / T * y
        y = y1
        print("%3.2f\t%3.2f\t%3.2f\t%3.2f" % (r, y1, u, (r-y1)))

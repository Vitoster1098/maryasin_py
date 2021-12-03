class Relay:
    def __init__(self):
        self.hister = 0.2
        pass

    def getOutput(self, actual: float, setpoint: float, diff: float):
        error = setpoint - actual
        if error >= self.hister:
            output = 10
        elif error >= -self.hister and error <= self.hister and diff > 0:
            output = 0
        elif error >= -self.hister and error <= self.hister and diff < 0:
            output = 10
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
    e = 0
    ep = 0
    d = 0
    print("Target\tOutput\tControl\tError")

    for i in range(100):
        if i == 20:
            r = 1
        e = r - y1
        d = (e-ep)/dt
        ep = e

        u = rel.getOutput(y1, r, d)
        y1 = k * dt / T * u + (T - dt) / T * y
        y = y1
        print("%3.2f\t%3.2f\t%3.2f\t%3.2f" % (r, y1, u, (r-y1)))

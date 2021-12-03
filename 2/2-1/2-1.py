class PReg:
    P = 0
    setpoint = 0

    def __init__(self, p):
        self.P = p

    def getOutput(self, actual: float, setpoint: float):
        error = setpoint - actual
        Poutput = self.P * error
        output = Poutput
        return output


if __name__ == '__main__':
    p = 10
    reg = PReg(p)
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
        u = reg.getOutput(y1, r)
        y1 = k * dt / T * u + (T - dt) / T * y
        y = y1
        print("%3.2f\t%3.2f\t%3.2f\t%3.2f" % (r, y1, u, (r - y1)))

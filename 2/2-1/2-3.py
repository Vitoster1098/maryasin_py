class PReg:
    P = 0
    D = 0
    setpoint = 0
    eastActual = 0
    maxOutput = 0
    minOutput = 0

    def __init__(self, p: float, d: float):
        self.P = p
        self.D = d

    def setOutputLimits(self, minimum: float, maximum: float):
        if maximum < minimum:
            return
        self.maxOutput = maximum
        self.minOutput = minimum

    def getOutput(self, actual: float, setpoint: float):
        error = setpoint - actual
        Poutput = error
        Doutput = self.D * (actual - self.eastActual)
        self.eastActual = actual
        output = self.P * (Poutput + Doutput)
        output = self.constrain(output, self.minOutput, self.maxOutput)
        return output

    def constrain(self, value: float, min: float, max: float):
        if value > max:
            return max
        if value < min:
            return min
        return value


if __name__ == '__main__':
    p = 10
    d = 0.2
    reg = PReg(p, d)
    reg.setOutputLimits(-1.8, 1.8)
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

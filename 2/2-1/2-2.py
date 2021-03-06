class PReg:
    P = 0
    I = 0
    setpoint = 0
    errorSum = 0
    maxOutput = 0
    minOutput = 0

    def __init__(self, p: float, i: float):
        self.P = p
        self.I = i

    def setOutputLimits(self, minimum: float, maximum: float):
        if maximum < minimum:
            return
        self.maxOutput = maximum
        self.minOutput = minimum

    def getOutput(self, actual: float, setpoint: float):
        error = setpoint - actual
        Poutput = error
        self.errorSum += error
        Ioutput = self.I * self.errorSum
        output = self.P * (Poutput + Ioutput)
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
    ti = 1
    reg = PReg(p, ti)
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

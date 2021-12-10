class DeltaPIDRegulator:
    P = 0
    I = 0
    D = 0
    Dt = 0

    maxOutput = 0
    minOutput = 0
    errorSum = 0
    maxError = 0
    lastOutput = 0
    lastError = 0
    last2Error = 0
    maxOutputRampRate = 0

    def __init__(self, p: float, ti: float, d: float, dt: float):
        self.P = p
        self.I = ti
        self.D = d
        self.Dt = dt

    def setOutputLimits(self, minimum, maximum):
        if maximum < minimum:
            return
        self.maxOutput = maximum
        self.minOutput = minimum

    def setMaxOutputRampRate(self, rate):
        self.maxOutputRampRate = rate

    def getOutput(self, actual, setpoint):
        error = setpoint - actual
        q0 = self.P + self.I * self.Dt + self.D / self.Dt
        q1 = -self.P - 2 * self.D / self.Dt
        q2 = self.D / self.Dt
        output = q0 * error + q1 * self.lastError * q2 * self.last2Error
        output = self.constrain(output, self.minOutput, self.maxOutput)
        if self.maxOutputRampRate != 0:
            output = self.constrain(output - self.lastOutput, self.lastOutput - self.maxOutputRampRate,
                                    self.lastOutput + self.maxOutputRampRate)

        self.last2Error = self.lastError
        self.lastError = error
        self.lastOutput = output
        return output

    def constrain(self, value, min, max):
        if value > max:
            return max
        if value < min:
            return min
        return value


if __name__ == '__main__':
    p = 10
    d = 0.2
    ti = 1
    dt = 0.1
    reg = DeltaPIDRegulator(p, ti, d, dt)
    reg.setOutputLimits(-1.8, 1.8)
    reg.setMaxOutputRampRate(1)
    k = 1.0
    T = 1.0
    u = 0
    up = 0
    r = 0
    y = 0
    y1 = 0
    print("Target\tOutput\tControl\tError")

    for i in range(100):
        if i == 20:
            r = 1
        u = up + reg.getOutput(y1, r)
        up = u
        y1 = k * dt / T * u + (T - dt) / T * y
        y = y1
        print("%3.2f\t%3.2f\t%3.2f\t%3.2f" % (r, y1, u, (r - y1)))

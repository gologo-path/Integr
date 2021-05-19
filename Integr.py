class Integr:

    def __init__(self, eval_str, start_x, step):
        self.start_x = start_x
        self.eval = eval_str
        self.h = step
        self.start_y = [self.eval_func(x) for x in self.start_x]

    def eval_func(self, x):
        return eval(self.eval.replace("x", "({})".format(x)))

    def rectangle(self):

        sum = 0
        for x in self.start_x[:-1]:
            sum += self.eval_func(x + (self.h / 2))

        return sum * self.h

    def trapezoid(self):
        sum1 = (self.eval_func(self.start_x[0]) + self.eval_func(self.start_x[-1])) / 2
        sum2 = 0
        for x in self.start_x[1:-1]:
            sum2 += self.eval_func(x)

        return (sum1 + sum2) * self.h

    def simpson(self):
        sum1 = (self.eval_func(self.start_x[0]) + self.eval_func(self.start_x[-1]))
        sum2 = 0
        sum3 = 0
        for i in range(1, len(self.start_x) - 1):
            if i % 2 == 0:
                sum3 += self.start_y[i]
            else:
                sum2 += self.start_y[i]

        return (self.h / 3) * (sum1 + (4 * sum2) + (2 * sum3))

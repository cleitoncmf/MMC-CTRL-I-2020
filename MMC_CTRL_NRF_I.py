from MMC import MMC
from SetterProperty import SetterProperty
from LINEARCTRL import LINEARCTRL

# Class which represents the current-controlled MMC considering inheritance
class MMC_CTRL_NRF_I:
    def __init__(self, Ci, Converter, s):
        self.s = s
        self.Controller = Ci
        self.MMC = Converter
        self.Yac = self.Yacs()
        self.Gicl = self.Gicls()

    def ControllerEffect(self):
        return (4 * self.s * self.MMC.Ceq * self.MMC.Vdc0 + 2 * self.MMC.S0 / (3 * self.MMC.Vdc0)) * self.Controller.TF

    def CharacteristicEq(self):
        return 4 * self.s * self.MMC.Ceq * ( self.MMC.Zs() + 2 * self.MMC.Zfs()) + self.ControllerEffect() + 1

    def Yacs(self):
        output = 8 * self.s * self.MMC.Ceq / self.CharacteristicEq()
        return self.__handleOutput__(output)

    def Gicls(self):
        output = self.ControllerEffect() / self.CharacteristicEq()
        return self.__handleOutput__(output)

    def __handleOutput__(
        self, out
    ):  # Check if the system is based on control or sympy packages and do the proper simplification
        if 'minreal' in dir(out):
            return out.minreal()
        elif 'simplify' in dir(out):
            return out.simplify()
        else:
            print(
                '\33[33m' +
                'Warning: s might not be neither an transfer-fucntion nor a symbolic-math object' + '\33[0m')
            return out

    @SetterProperty
    def Controller(self, value):
        if not isinstance(value, LINEARCTRL):
            raise TypeError('The controller must be a LINEARCTRL object')
        self.__dict__['Controller'] = value
    
    @SetterProperty
    def MMC(self, value):
        if not isinstance(value, MMC):
            raise TypeError('The Converter must be a MMC object')
        self.__dict__['MMC'] = value
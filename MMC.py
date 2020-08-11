# Class which represents the MMC
class MMC:
    def __init__(self, s,
                 L=19e-3,
                 Lf=20e-3,
                 R=1,
                 Rf=1,
                 C=9000e-6,
                 N=20,
                 Vdc0=150e3,
                 S0=100e6,
                 Cf=20e-6,
                 VLL=69e3):
        self.L = L
        self.Lf = Lf
        self.R = R
        self.Rf = Rf
        self.C = C
        self.N = N
        self.Ceq = C / N
        self.Vdc0 = Vdc0
        self.S0 = S0
        self.VLL = VLL
        self.s = s

    def getRatedPower(self):
        return self.S0

    def getRatedPowerInMVA(self):
        return self.S0 / 1e6

    def getRatedDCVoltage(self):
        return self.Vdc0

    def getRatedDCVoltageInKV(self):
        return self.Vdc0 / 1000

    def getRatedLineVoltage(self):
        return self.VLL

    def getRatedLineVoltageInKV(self):
        return self.VLL / 1000

    def getRatedLineCurrent(self):
        return self.S0 / (np.sqrt(3) * self.VLL)

    def getRatedLineCurrentInKA(self):
        return self.getRatedLineCurrent() / 1000

    def getRatedPhaseVoltage(self):
        return self.VLL / np.sqrt(3)

    def getRatedPhaseVoltageInKV(self):
        return set.getRatedPhaseVoltage() / 1000

    def getRatedPeakVoltage(self):
        return self.getRatedPhaseVoltage() * np.sqrt(2)

    def getRatedPeakVoltageInKV(self):
        return self.getRatedPeakVoltage() / 1000

    def getRatedPeakCurrent(self):
        return self.getRatedLineCurrent() * np.sqrt(2)

    def getRatedPeakCurrentInKA(self):
        return self.getRatedPeakCurrent() / 1000

    def Zs(self):  # Inner impedance of the mmc
        return self.L * self.s + self.R

    def Zfs(self):  # Inner impedance of the mmc
        return self.Lf * self.s + self.Rf

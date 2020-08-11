# Class for representing generic linear controllers
class LINEARCTRL:
    def __init__(self, type, s, **kwargs):


        self.s = s

        # Dictionary with the different control requirements and methods
        CTRL_TYPE_REQUIREMENTS = {
            'P': [{'kp'}, self.__ctrlP__],
            'R': [{'kr', 'd', 'w0'}, self.__ctrlR__],
            'PR': [{'kp', 'kr', 'd', 'w0'}, self.__ctrlPR__],
            'PI': [{'kp', 'ki'}, self.__ctrlPI__]
        }

        try:
            ctrlPAR = CTRL_TYPE_REQUIREMENTS[type]
            allowed_keys = ctrlPAR[0]
            self.type = type
        except:
            raise KeyError(type + ' is not a valid control type')

        self.__dict__.update(
            (k, v) for k, v in kwargs.items() if k in allowed_keys)
        self.__isRequirementsFulfilled__(requiredKeys=allowed_keys)
        self.__isThereUnecessaryArgs__(requiredKeys=allowed_keys, argsList=list(kwargs.keys()))

        # Difinition of the tranfer function
        ctrlParametersDict = {
            k: self.__getattribute__(k)
            for k in allowed_keys
        }
        self.TF = ctrlPAR[1](ctrlParametersDict)

    def __isRequirementsFulfilled__(self, requiredKeys):
        for item in requiredKeys:
            if item not in list(self.__dict__.keys()):
                raise TypeError('Argument ' + item + ' is missing')
        return True

    def __isThereUnecessaryArgs__(self, requiredKeys, argsList):
        output = False
        for item in argsList:
            if item not in requiredKeys and item != 'type':
                print('\33[33m' + 'Warning: ' + item + ' is not necessary' +'\33[0m')
                output = True
        return output

    def __ctrlP__(self, ctrlDict):
        return ctrlDict['kp'] + (
            self.s - self.s)  # Only for forcing the output be an TF object

    def __ctrlR__(self, ctrlDict):
        return ctrlDict['kr'] * self.s / (
            self.s**2 + 2 * ctrlDict['d'] * ctrlDict['w0'] * self.s + ctrlDict['w0']**2)

    def __ctrlPR__(self, ctrlDict):
        return ctrlDict['kp'] + self.__ctrlR__(ctrlDict)

    def __ctrlPI__(self, ctrlDict):
        return ctrlDict['kp'] + ctrlDict['ki'] / self.s
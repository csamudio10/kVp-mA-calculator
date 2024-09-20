import numpy as np
from lmfit import Model as lm_model


def exp_decay(t, A, k, B):
    return A * np.exp(-k * t) + B


class Machine:

    def __init__(self, kVp0,mA0,kVp,mA):
        self.kVp0 = kVp0
        self.mA0 = mA0
        self.kVp = kVp
        self.mA = mA
        
        
    def gen_points_for_mA(self, n_points: int = 20):
        kVp = [self.kVp0]
        mA = [self.mA0]
        
        for i in range(n_points):
            kVp_i = kVp[i] * 1.15
            kVp.append(kVp_i)

            mA_i = mA[i] * 0.5
            mA.append(mA_i)

        return np.array(kVp), np.array(mA)
    
    def gen_points_for_kVp(self, n_points: int = 20):
        kVp = [self.kVp0]
        mA = [self.mA0]

        for i in range(n_points):
            kVp_i = kVp[i] * 0.85
            kVp.append(kVp_i)

            mA_i = mA[i] * 2
            mA.append(mA_i)

        return np.array(kVp), np.array(mA)
    
    
    def create_model(self):
        self.model = lm_model(exp_decay)
        params = self.model.make_params(A=350, k=0.05, B=1)
        
        kVp, mA = self.gen_points_for_mA()
            # Fit the model to the data
        result = self.model.fit(mA, params, t=kVp)
        
        self.model_result =  result
        
        return result
    
    def extract_model_params(self):
        result = self.create_model()
        A = result.params['A'].value
        k = result.params['k'].value
        B = result.params['B'].value
        
        params = {"A" : A,
                  "k" : k,
                  "B" : B}
        
        self.params = params
        return A, k, B
    
    def print_model_params(self):
        return self.model_result.fit_report()
        

    def calc_new_point(self, variable: str, varaible_value: float):
        A = self.params["A"]
        k = self.params["k"]
        B = self.params["B"]
        
        if variable.lower() == 'ma':
            return A * np.exp(-k * varaible_value) + B
        
        if variable.lower() == 'kvp':
            return -np.log((varaible_value - B) / A) / k



if __name__ == '__main__':
    test = Machine(55,1.8,60,37)
    n_points = 20
    kVp0 = 55
    mA0 = 1.8
    kVp = 60  
    mA = 37 #dummy

    test.create_model()
    test.extract_model_params()
    a = test.calc_new_point('kVp',37)
    print(a)
# Módulo de tratamento nos dados

import pandas as pd
import numpy as np

PERIODS = ['10m', '30m', '1h', '12h', '1d', '7d', '15d', '30d', '60d', '90d']

# Classe
class FeatureDerivative:
    def __init__(self):
        pass

    def add_avg_feature(self, 
                        data, 
                        periods = None, 
                        denominator_col = '_pay_times', 
                        numerator_col = '_Sum_pay_amount',
                        output_col = '_Avg_pay_amount', ):

        if periods is None:
            periods = PERIODS
        tmp_data = data.copy()
        
        for period in periods:
            n_item = period + numerator_col
            d_item = period + denominator_col
            add_col = period + output_col
            tmp_data[add_col] = (tmp_data[n_item] / tmp_data[d_item]).replace([-np.inf, np.inf], 0).fillna(0)

        return tmp_data

    def add_prd_change_feature(self, 
                                data, 
                                periods = None, 
                                input_str = '_Avg_pay_amount', 
                                output_str = '_payment_increase', ):
        if periods is None:
            periods = PERIODS
        tmp_data = data.copy()
        
        for i in range(len(periods) - 1):
            s_cal = periods[i] + input_str
            e_cal = periods[i + 1] + input_str
            out_col = periods[i] + '_' + periods[i + 1] + output_str
            tmp_data[out_col] = tmp_data[e_cal] - tmp_data[s_cal]

        return tmp_data

    def avg_payment_derivative(self, 
                               data, 
                               periods = None, ):
        if periods is None:
            periods = PERIODS
            
        tmp_data = data.copy()

        tmp_data = self.add_avg_feature(tmp_data, periods)
        tmp_data = self.add_prd_change_feature(tmp_data, periods)
        avg_pay_cols = [d + '_Avg_pay_amount' for d in periods]
        tmp_data['max_Avg_pay_amount'] = tmp_data[avg_pay_cols].max(axis=1)

        return tmp_data



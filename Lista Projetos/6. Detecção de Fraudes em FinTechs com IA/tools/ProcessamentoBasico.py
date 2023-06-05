# Módulo de processamento básico de atributoos

import pandas as pd
import numpy as np


# Classe
class ProcessamentoBasico:
    def __init__(self):
        pass

    def fix_value_check(self, data):

        tmp_data = data.copy()

        if data.empty:
            return False

        fixed_value_check = tmp_data.count()
        fix_cols = fixed_value_check.index[fixed_value_check <= 1]

        return fix_cols.tolist()

    def missing_value_pct(self, data):

        tmp_data = data.copy()

        if tmp_data.empty:
            return False

        missing_rate_df = pd.DataFrame(tmp_data.isnull().mean(), columns=['missing_rate'])

        return missing_rate_df.sort_values(by='missing_rate', ascending=False)

    def add_missing_indicator_to_df(self, data, cols, adding_str='_ismissing'):

        tmp_data = data.copy()

        for col in cols:
            tmp_data[col + adding_str] = tmp_data[col].isnull().astype(int)

        return tmp_data

    def missing_odds_ratio(self, data, cols, flag_col):
 
        check_missing = {}
        tmp_data = data.copy()

        for col in cols:
            tmp_data['miss'] = tmp_data[col].isnull().astype(int)
            flag_pct = tmp_data.groupby('miss')[flag_col].mean()
            check_missing[col] = (flag_pct[0], flag_pct[1])

        check_df = pd.DataFrame.from_dict(check_missing, orient='index')
        check_df = check_df.rename(columns={0: 'not_missing', 1: 'missing'})
        check_df['odds_ratio'] = np.log(check_df['missing'] / check_df['not_missing'])

        return check_df.sort_values(by='odds_ratio', ascending=False)

    def feature_type_identifier(self, data, itype='Object'):

        tmp_data = data.copy()
        types = tmp_data.dtypes

        return types.index[types == itype].tolist()

    def get_categorical_dummy_variable(self, data, cols):

        tmp_data = data.copy()
        dummy_cols = list()
        dummy_data = list()

        for col in cols:
            dummies = pd.get_dummies(tmp_data[col], prefix=col)
            dummy_data.append(dummies)
            del tmp_data[col]
            dummy_cols = dummy_cols + dummies.columns.tolist()

        dummy_df = pd.concat(dummy_data, axis=1)
        res_df = pd.concat([dummy_df, tmp_data], axis=1)

        return {'data': res_df, 'dummy_cols': dummy_cols}


if __name__ == '__main__':

    test = ProcessamentoBasico()

    df = pd.DataFrame({'x': 1, "y": 2}, index=[0])

    t = test.fix_value_check(df)
    
    print(t)

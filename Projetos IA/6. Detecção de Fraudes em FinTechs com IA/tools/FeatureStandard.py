# Módulo para padronizar os dados

# Imports
import numpy as np
import pandas as pd


def mean_std(array):
    return np.mean(array), np.std(array)


def linear_std(array):
    min = np.min(array)
    max = np.max(array)
    return (array - min) / (max - min)


def norm_std(array):
    mean = np.mean(array)
    std = np.std(array)
    return (array - mean) / std


def get_outlier_features(data, 
                         feature_list, 
                         percentiles = (0.1, 0.99),  
                         expand = False):

    df = data.copy()
    lower = percentiles[0]
    upper = percentiles[1]
    quantile_df = df[feature_list].quantile([lower, upper], numeric_only=False)
    outlier_feature = list()

    for feature in feature_list:
        l = quantile_df[feature][lower]
        u = quantile_df[feature][upper]
        if expand:
            d = u - l
            u, l = u + 1.5 * d, l - 1.5 * d
        out_counts = sum((df[feature]<l)|(u<df[feature]))
        if out_counts:
            outlier_feature.append(feature)
            
    return outlier_feature


def outlier_effect(data, 
                   outlier_cols, 
                   flag_col, 
                   percentiles = (1, 99), 
                   expand = False):

    outlier_effect_dict = dict()
    df = data.copy()

    for col in outlier_cols:
        lower, upper = np.percentile(df[col], percentiles[0]), np.percentile(df[col], percentiles[1])
        if expand:
            d = upper - lower
            upper, lower = upper + 1.5 * d, lower - 1.5 * d
        lower_sample, middle_sample, upper_sample = df[df[col] < lower], df[(df[col] >= lower) & (df[col] <= upper)], df[df[col] > upper]
        lower_fraud, middle_fraud, upper_fraud = lower_sample[flag_col].mean(), middle_sample[flag_col].mean(), upper_sample[flag_col].mean()
        l = (lower_fraud / middle_fraud)
        u = (upper_fraud / middle_fraud)
        lower_log_odds, upper_log_odds = np.log(l), np.log(u)
        outlier_effect_dict[col] = {'log_odds_lower': lower_log_odds, 'log_odds_upper': upper_log_odds}

    res_df = pd.DataFrame.from_dict(outlier_effect_dict, orient='index')

    return res_df


def zero_score_normalization(df, 
                             col, 
                             percentiles = (1, 99), 
                             expand = False):

    lower, upper = np.percentile(df[col], percentiles[0]), np.percentile(df[col], percentiles[1])

    if lower == upper:
        return 1
    else:
        if expand:
            d = upper - lower
            upper, lower = upper + 1.5 * d, lower - 1.5 * d
        new_col = df[col].map(lambda x: min(max(x, lower), upper))
        mu, sigma = new_col.mean(), np.sqrt(new_col.var())
        new_var = norm_std(new_col)

        return {'new_var': new_var, 'lower': lower, 'upper': upper, 'mu': mu, 'sigma': sigma}


if __name__ == '__main__':

    # 1 - Gera uma sequência a de comprimento 1000, os elementos são números aleatórios uniformemente distribuídos entre 0 e 10
    a = np.random.uniform(0, 10, 1000)
    print(a)

    # 2 - Gera uma sequência b de comprimento 5, os elementos são números aleatórios uniformemente distribuídos entre 50 e 100
    b = np.random.uniform(50, 100, 5)
    print(b)
    # 3 - Combina a e b juntos para formar a sequência c
    c = np.concatenate((a, b), axis=0)
    print(c)

    # 4 - Encontra a média e o desvio padrão da sequência a e c, e compara-os
    a_stats = mean_std(a)
    b_stats = mean_std(c)
    print(a_stats, b_stats)

    # 5 - Encontra os quantis de 5% e 95% da sequência c
    c_5 = np.percentile(c, 5)
    c_95 = np.percentile(c, 95)
    print(c_5, c_95)

    # 6 - Verifica se o elemento em b está entre os dois quantis em (5)
    for i in b:
        if c_5 <= i <= c_95:
            print(i, ': between 5% and 95%')
        else:
            print(i, ": out of range")

    # 7 - Realiza normalização linear e normalização de desvio padrão médio
    linear_std_c = linear_std(c)
    norm_std_c = norm_std(c)
    print(linear_std_c)
    print(norm_std_c)

    # 8 - Remove o valor de c que não está entre os quantis de 5% e 95% e calcule max e min para os valores restantes. 
    # Em seguida, executa a normalização linear e normalização de desvio padrão médio em todas as amostras
    c_subset = c[(c_5 <= c) & (c <= c_95)]
    print(linear_std(c_subset))
    print(norm_std(c_subset))

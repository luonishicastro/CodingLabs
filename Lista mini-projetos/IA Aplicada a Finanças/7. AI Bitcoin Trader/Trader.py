# Projeto 6 - AI Bitcoin Trader

# Para executar, digite: python Trader.py

print('\nOlá. Seja bem-vindo(a) ao AI Bitcoin Trader. Vou ajudar você a investir em Bitcoin!')

# Versão da Linguagem Python
from platform import python_version
print('\nVersão da Linguagem Python Usada Neste AI Bot Trader:', python_version())

# CryptoCurrency eXchange Trading Library
# https://pypi.org/project/ccxt/
# pip install -q ccxt

# https://pypi.org/project/bayesian-optimization/
# pip install -q bayesian-optimization==1.2

# Imports
import csv
import ccxt
import time
import random
import types
import pkg_resources
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bayes_opt import BayesianOptimization
from pprint import pprint
from datetime import datetime

# Função para salvar dados em formato csv
def grava_csv(arquivo, dados):
    
    # Abre o arquivo para escrita
    with open(arquivo, mode = 'w') as arquivo_saida:
        
        # Gera o cabeçalho
        arquivo_saida.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
        
        # Grava os dados
        csv_writer = csv.writer(arquivo_saida, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        csv_writer.writerows(dados)


# Função para fazer conexão à exchange para extração dos dados
# https://www.bitmex.com/
# https://www.bitmex.com/app/apiOverview
def conecta_exchange(exchange, max_retries, symbol, timeframe, since, limit):
    
    # Zera o número de tentativas
    num_retries = 0
    
    # Tenta fazer a conexão
    try:
        num_retries += 1
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
        return ohlcv
    except Exception:
        if num_retries > max_retries:
            raise

# Função para extração dos dados
def extrai_dados(exchange, max_retries, symbol, timeframe, since, limit):
    
    # Timestamp
    earliest_timestamp = exchange.milliseconds()
    
    # Duração da janela em segundos
    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    
    # Duração da janela em milisegundos
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    
    # Diferença de tempo
    timedelta = limit * timeframe_duration_in_ms
    
    # Lista para os dados
    all_ohlcv = []
    
    # Loop
    while True:
        
        # Data de início para extração dos dados
        fetch_since = earliest_timestamp - timedelta
        
        # Conecta na exchange e extrai os dados
        ohlcv = conecta_exchange(exchange, max_retries, symbol, timeframe, fetch_since, limit)
        
        # Se alcançamos o limite, finaliza o loop
        if ohlcv[0][0] >= earliest_timestamp:
            break
        
        # Atualiza o tempo mais cedo
        earliest_timestamp = ohlcv[0][0]
        
        # Atualiza os dados
        all_ohlcv = ohlcv + all_ohlcv
        
        # Print do andamento
        print(len(all_ohlcv), 'registros extraídos de', exchange.iso8601(all_ohlcv[0][0]), 'a', exchange.iso8601(all_ohlcv[-1][0]))
        
        if fetch_since < since:
            break
            
    return all_ohlcv

# Função para extrair os dados e salvar em formato csv
def extrai_dados_para_csv(filename, exchange_id, max_retries, symbol, timeframe, since, limit):
    
    # Obtém o id da exchange com o pacote ccxt
    exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True,})
    
    # Checa a consistência 
    if isinstance(since, str):
        since = exchange.parse8601(since)
    
    # Extrai o que está sendo comercializado
    exchange.load_markets()
    
    # Extrai os dados
    ohlcv = extrai_dados(exchange, max_retries, symbol, timeframe, since, limit)
    
    # Contador
    key = 0
    
    # Loop
    for item in ohlcv:
        epoch = int(item[0]) / 1000
        ohlcv[key][0] = datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d')
        ohlcv[key][5] = int(item[5])
        ohlcv[key].append(ohlcv[key][5])
        ohlcv[key][5] = ohlcv[key][4]
        key += 1
    
    # Comprimento de dados extraídos
    ohlen = len(ohlcv)
    
    # Print do andamento
    pprint("Número de Registros: " + str(ohlen))
    
    # Vamos manter um limite para os dados
    if ohlen > 399:
        ohrem = ohlen - 399
        pprint("Removendo: " + str(ohrem))
        ohlcv = ohlcv[ohrem:]
        
    # Grava os dados em csv
    grava_csv(filename, ohlcv)
    
    # Print
    print('Salvos', len(ohlcv), 'registros no arquivo', filename)


# Define os parâmetros de extração dos dados

# Exchange: https://www.bitmex.com/app/apiOverview
exchange = "bitmex"

# Símbolo da criptomoeda
simbolo = "BTC/USD"

# Janela
janela = "1d"

# Data de início
data_inicio = "2018-01-01T00:00:00Z"

# Arquivo de saída
outfile = "dados/dataset.csv"

print('\nIniciando a extração de dados históricos de cotação do Bitcoin!\n')

# Executa a extração dos dados
extrai_dados_para_csv(outfile, exchange, 3, simbolo, janela, data_inicio, 100)

#  Executar a partir deste ponto usando o dataset fornecido.

# Carregando o arquivo do disco
df = pd.read_csv(outfile)

# Dados de fechamento
close = df.Close.values.tolist()

# Outros parâmetros para a versão base do modelo
window_size = 30
skip = 5
l = len(close) - 1

print('\nDados extraídos e salvos em disco!')

# Classe para a estratégia de treinamento
# Usamos Deep Evolution Strategy do OpenAI
class PoliticaTrader:

    # Inputs
    inputs = None

    # Construtor
    def __init__(self, weights, reward_function, population_size, sigma, learning_rate):
        
        # Inicializa os atributos da classe
        self.weights = weights
        self.reward_function = reward_function
        self.population_size = population_size
        self.sigma = sigma
        self.learning_rate = learning_rate

    # Obtém o peso a partir da população
    def get_weights_population(self, weights, population):
        
        # Lista para os pesos
        weights_population = []
        
        # Loop pela população
        for index, i in enumerate(population):
            jittered = self.sigma * i
            weights_population.append(weights[index] + jittered)
        
        return weights_population

    # Obtém os pesos
    def get_weights(self):
        return self.weights

    # Treinamento
    def treinamento(self, epoch = 100, print_every = 1):
        
        # Time
        lasttime = time.time()
        
        # Loop pelas épocas
        for i in range(epoch):
            
            # Lista para a população
            population = []
            
            # Recompensas
            rewards = np.zeros(self.population_size)
            
            # Loop pelo population_size
            for k in range(self.population_size):
                
                x = []
                
                # Loop
                for w in self.weights:
                    x.append(np.random.randn(*w.shape))
                    
                population.append(x)
            
            # Loop
            for k in range(self.population_size):
                
                weights_population = self.get_weights_population(self.weights, population[k])
                rewards[k] = self.reward_function(weights_population)
            
            # Recompensas
            rewards = (rewards - np.mean(rewards)) / np.std(rewards)
            
            # Loop
            for index, w in enumerate(self.weights):
                A = np.array([p[index] for p in population])
                
                # Pesos da rede neural 
                self.weights[index] = (w + self.learning_rate / (self.population_size * self.sigma) * np.dot(A.T, rewards).T)
            
            if (i + 1) % print_every == 0:
                print('Iteração %d. Recompensa: %f' % (i + 1, self.reward_function(self.weights)))
        
        print('Tempo Total de Treinamento:', time.time() - lasttime, 'segundos')


# Classe do Modelo
class Modelo:
    
    # Método construtor
    def __init__(self, input_size, layer_size, output_size):
        
        self.weights = [np.random.randn(input_size, layer_size),
                        np.random.randn(layer_size, output_size),
                        np.random.randn(layer_size, 1),
                        np.random.randn(1, layer_size),]

    # Função para previsão
    def predict(self, inputs):
        
        # Feed forward
        feed = np.dot(inputs, self.weights[0]) + self.weights[-1]
        
        # Decisão de compra (previsão)
        decision = np.dot(feed, self.weights[1])
        
        # Compra (decisão)
        buy = np.dot(feed, self.weights[2])
        
        return decision, buy

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights


# Função para obter o estado dos dados
def get_state(data, t, n):
    d = t - n + 1
    block = data[d : t + 1] if d >= 0 else -d * [data[0]] + data[0 : t + 1]
    res = []
    for i in range(n - 1):
        res.append(block[i + 1] - block[i])
    return np.array([res])

# Classe para o agente inteligente (Trader)
class Trader:
    
    # Método construtor
    def __init__(self, population_size, sigma, learning_rate, model, money, max_buy, max_sell, skip, window_size,):
        
        # Inicializa os atributos
        self.window_size = window_size
        self.skip = skip
        self.POPULATION_SIZE = population_size
        self.SIGMA = sigma
        self.LEARNING_RATE = learning_rate
        self.model = model
        self.initial_money = money
        self.max_buy = max_buy
        self.max_sell = max_sell
        self.es = PoliticaTrader(self.model.get_weights(),
                                 self.get_reward,
                                 self.POPULATION_SIZE,
                                 self.SIGMA,
                                 self.LEARNING_RATE,)

    # Método de ação
    def agir(self, sequence):
        decision, buy = self.model.predict(np.array(sequence))
        return np.argmax(decision[0]), int(buy[0])

    # Método para obter recompensa
    def get_reward(self, weights):
        
        # Valor inicial investido
        initial_money = self.initial_money
        starting_money = initial_money
        
        # Pesos
        self.model.weights = weights
        
        # Estado
        state = get_state(close, 0, self.window_size + 1)
        
        # Objetos de controle
        inventory = []
        quantity = 0
        
        # Loop
        for t in range(0, l, self.skip):
            
            # Ação e compra/venda
            action, buy = self.agir(state)
            
            # Próximo estado
            next_state = get_state(close, t + 1, self.window_size + 1)
            
            # Verifica ação e valor inicial investido
            if action == 1 and initial_money >= close[t]:
                if buy < 0:
                    buy = 1
                if buy > self.max_buy:
                    buy_units = self.max_buy
                else:
                    buy_units = buy
                    
                total_buy = buy_units * close[t]
                initial_money -= total_buy
                inventory.append(total_buy)
                quantity += buy_units
            
            elif action == 2 and len(inventory) > 0:
                if quantity > self.max_sell:
                    sell_units = self.max_sell
                else:
                    sell_units = quantity
                    
                quantity -= sell_units
                total_sell = sell_units * close[t]
                initial_money += total_sell

            # Próximo estado
            state = next_state
        
        return ((initial_money - starting_money) / starting_money) * 100

    # Treinamento do Trader
    def fit(self, iterations, checkpoint):
        self.es.treinamento(iterations, print_every = checkpoint)

    # Método para recomendação
    def investir(self):
        
        # Valor inicial
        initial_money = self.initial_money
        starting_money = initial_money
        
        # Estado
        state = get_state(close, 0, self.window_size + 1)
        
        # Listas de controle        
        states_sell = []
        states_buy = []
        inventory = []
        quantity = 0
        
        # Loop
        for t in range(0, l, self.skip):
            
            # Ação e compra
            action, buy = self.agir(state)
            
            # Próximo estado
            next_state = get_state(close, t + 1, self.window_size + 1)
            
            # Verifica ação e valor inicial investido
            if action == 1 and initial_money >= close[t]:
                if buy < 0:
                    buy = 1
                if buy > self.max_buy:
                    buy_units = self.max_buy
                else:
                    buy_units = buy
                
                total_buy = buy_units * close[t]
                initial_money -= total_buy
                inventory.append(total_buy)
                quantity += buy_units
                states_buy.append(t)
                
                print('Dia %d: comprar %d unidades ao preço de %f, saldo total %f' % (t, buy_units, total_buy, initial_money))
            
            elif action == 2 and len(inventory) > 0:
                bought_price = inventory.pop(0)
                if quantity > self.max_sell:
                    sell_units = self.max_sell
                else:
                    sell_units = quantity
                if sell_units < 1:
                    continue
                    
                quantity -= sell_units
                total_sell = sell_units * close[t]
                initial_money += total_sell
                states_sell.append(t)
                
                try:
                    invest = ((total_sell - bought_price) / bought_price) * 100
                except:
                    invest = 0
                
                print('Dia %d, vender %d unidades ao preço de %f, investimento %f %%, saldo total %f,' % (t, sell_units, total_sell, invest, initial_money))
            
            # Próximo estado
            state = next_state

        # Investimento
        invest = ((initial_money - starting_money) / starting_money) * 100
        
        print('\nGanho Total %f, Valor Total Investido %f' % (initial_money - starting_money, invest))
        
        plt.figure(figsize = (20, 10))
        plt.plot(close, label = 'Valor Real de Fechamento', c = 'g')
        plt.plot(close, 'X', label = 'Previsão de Compra', markevery = states_buy, c = 'b')
        plt.plot(close, 'o', label = 'Previsão de Venda', markevery = states_sell, c = 'r')
        plt.legend()
        plt.show()

# Função para encontrar o melhor trader
def melhor_trader(window_size, skip, population_size, sigma, learning_rate, size_network):
    
    # Cria o modelo
    model = Modelo(window_size, size_network, 3)
    
    # Cria o trader
    trader = Trader(population_size, sigma, learning_rate, model, 10000, 5, 5, skip, window_size,)
    
    # Treinamento
    try:
        trader.fit(100, 1000)
        return trader.es.reward_function(trader.es.weights)
    except:
        return 0


# Função para encontrar o melhor trader de acordo com os hiperparâmetros
def busca_melhor_trader(window_size, skip, population_size, sigma, learning_rate, size_network):
    
    # Variável global
    global accbest
    
    # Hiperparâmetros
    param = {'window_size': int(np.around(window_size)),
             'skip': int(np.around(skip)),
             'population_size': int(np.around(population_size)),
             'sigma': max(min(sigma, 1), 0.0001),
             'learning_rate': max(min(learning_rate, 0.5), 0.000001),
             'size_network': int(np.around(size_network)),}
    
    print('\nBuscando Parâmetros %s' % (param))
    
    # Investimento feito pelo melhor trader
    investment = melhor_trader(**param)
    
    print('Após 100 iterações o investimento foi de %f' % (investment))
        
    return investment


# Modelo para otimização bayesiana de hiperparâmetros
otimizacao_bayesiana = BayesianOptimization(busca_melhor_trader, {'window_size': (2, 50),
                                                                  'skip': (1, 15),
                                                                  'population_size': (1, 50),
                                                                  'sigma': (0.01, 0.99),
                                                                  'learning_rate': (0.000001, 0.49),
                                                                  'size_network': (10, 1000),},)

if __name__ == "__main__":

    # Otimização
	otimizacao_bayesiana.maximize(init_points = 30, n_iter = 50, acq = 'ei', xi = 0.0)

	# Execução do AI Bot Trader - Modelo Otimizado
	melhor_trader(window_size = int(np.around(max([d['window_size'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))), 
				  skip = int(np.around(max([d['skip'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))), 
		          population_size = int(max([d['population_size'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]])), 
                  sigma = max([d['sigma'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]), 
                  learning_rate = max([d['learning_rate'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]), 
                  size_network = int(np.around(max([d['size_network'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))))


	modelo_otim = Modelo(input_size = int(np.around(max([d['window_size'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))), 
                         layer_size = int(np.around(max([d['size_network'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))), 
                         output_size = 3)

	# Cria o trader com otimização
	trader_otim = Trader(population_size = int(np.around(max([d['population_size'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))), 
                         sigma = max([d['sigma'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]), 
                         learning_rate = max([d['learning_rate'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]), 
                         model = modelo_otim, 
                         money = 10000, 
                         max_buy = 5, 
                         max_sell = 5, 
                         skip = int(np.around(max([d['skip'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))), 
                         window_size = int(np.around(max([d['window_size'] for d in [dic['params'] for dic in otimizacao_bayesiana.res]]))))

    # Treinamento
	trader_otim.fit(500, 100)

    # Previsões de investimento
	trader_otim.investir()





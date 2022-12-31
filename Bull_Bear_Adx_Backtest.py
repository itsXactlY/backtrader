import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd

class MaCrossStrategy(bt.Strategy):
 
    def __init__(self):
        ma_fast = bt.ind.SMA(period = 10)
        ma_slow = bt.ind.SMA(period = 50)
         
        self.crossover = bt.ind.CrossOver(ma_fast, ma_slow)
 
    def next(self):
        if not self.position:
            if self.crossover > 0: 
                self.buy()
        elif self.crossover < 0: 
            self.close()


def _read_file(filename):
    from os.path import dirname, join
    
    data = pd.read_csv(join(dirname(__file__), filename),
                       index_col=0, parse_dates=True, infer_datetime_format=True)
    
    # stip datetime for backtest
    data.drop(columns=['datetime'], inplace=True)
    data.drop(columns=['adj_close'], inplace=True)
    print(data)
    # sleep(133337)

    return data 

######################################################################################################################
#                                   NOTES!                                                                           #
# pip uninstall backtrader                                                                                           # 
# pip install git+https://github.com/mementum/backtrader.git@0fa63ef4a35dc53cc7320813f8b15480c8f85517#egg=backtrader #
# pip install matplotlib                                                                                             #
######################################################################################################################




df = _read_file('binance_bars_BTC_4h.csv')

cerebro = bt.Cerebro()
 
data = bt.feeds.PandasData(dataname = df)
cerebro.adddata(data)
 
cerebro.addstrategy(MaCrossStrategy)
cerebro.broker.setcash(1000000.0)
 
cerebro.addsizer(bt.sizers.PercentSizer, percents = 50)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = "sharpe")
cerebro.addanalyzer(btanalyzers.Transactions, _name = "trans")

back = cerebro.run()

# sleep(133337)

cerebro.broker.getvalue() # Ending balance
back[0].analyzers.sharpe.get_analysis() # Sharpe
len(back[0].analyzers.trans.get_analysis()) # Number of Trades

cerebro.plot()

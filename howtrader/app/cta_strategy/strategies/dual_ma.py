from howtrader.app.cta_strategy import (CtaTemplate, CtaEngine, StopOrder)
from howtrader.trader.object import (TickData, BarData, TradeData, OrderData)
from howtrader.trader.utility import (BarGenerator, ArrayManager)
from decimal import Decimal

class DualMAStrategy(CtaTemplate):
    author = 'Ornob'
    fast_window = 10
    slow_window = 20
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    volume = 0.1
    
    parameters = ['fast_window', 'slow_window', 'volume']
    variables = ['fast_ma0', 'fast_ma1', 'slow_ma0', 'slow_ma1']
    
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()
        
    def on_init(self):
        self.writelog('Strategy initialized')
        self.load_bar(10)
    
    def on_start(self):
        self.write_log('Strategy started')
        self.put_event()
        
    def on_stop(self):
        self.writelog('Strategy stopped')
        self.put_event()
    
    def on_tick(self, tick: TickData):
        self.bg.update_tick(tick)
    
    def on_bar(self, bar: BarData):
        am = self.am
        am.update_bar(bar)
        if am.initied:
            return
        fast_ma = am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]
        
        slow_ma = am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma0 = slow_ma[-2]
        
        cross_over = (self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1)
        coss_below = (self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1)
        
        if cross_over:
            if self.pos == 0:
                self.buy(Decimal(bar.close_price), self.volume)
            elif self.pos < 0:
                self.cover(Decimal(bar.close_price), self.volume)
                self.buy(Decimal(bar.close_price), self.volume)
        
        elif cross_below:
            if self.pos == 0:
                self.short(Decimal(bar.close_price), self.volume)
            elif self.pos > 0:
                self.sell(Decimal(bar.close_price), self.volume)
                self.short(Decimal(bar.close_price), self.volume)
        
        self.put_event()
    
    def on_order(self, order: OrderData):
        self.write_log(f'Order update: {order.status} at {order.price} for {order.volume}')
    
    def on_trade(self, trade: TradeData):
        self.write_log(f'Trade executed: {trade.direction} {trade.volume} at {trade.price}')
        self.put_event()
    def on_stop_order(self, stop_order: StopOrder):
        pass            
        
        
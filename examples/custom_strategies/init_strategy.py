# To DO

# """ This file is used to initialize the strategy to HowTraders database. """

# import json
# import os
# from howtrader.event import EventEngine, Event
# from howtrader.trader.engine import MainEngine
# from howtrader.trader.ui import MainWindow, create_qapp
# from howtrader.trader.setting import SETTINGS
# from howtrader.gateway.binance import BinanceUsdtGateway, BinanceSpotGateway, BinanceInverseGateway
# from howtrader.app.cta_strategy import CtaStrategyApp
# from howtrader.app.data_manager import DataManagerApp
# from howtrader.app.data_recorder import DataRecorderApp
# from howtrader.app.algo_trading import AlgoTradingApp
# from howtrader.app.risk_manager import RiskManagerApp
# from howtrader.app.spread_trading import SpreadTradingApp
# from howtrader.app.tradingview import TradingViewApp
# from howtrader.app.cta_strategy.strategies.dual_ma import DualMAStrategy


# def strategy_configuration(strategy_name, strat_setting):
#     curr_dir = os.path.dirname(os.path.abspath(__file__))
#     json_dir = 'howtrader/cta_strategy_setting.json'
#     if os.path.exists(json_dir) and os.path.getsize(json_dir) > 0:
#         with open(json_dir) as f:
#             data = json.load(f)
#     else:
#         data = {}
#         print('File nopt found')
#     data[strategy_name] = strat_setting
#     with open(json_dir, 'w') as f:
#         json.dump(data, f, indent=4)
#         return

# def main():
#     event_engine = EventEngine()
#     main_engine = MainEngine(event_engine)
#     cta_engine = main_engine.add_app(CtaStrategyApp)
#     strategy_settings = {
#     "class_name": "DualMAStrategy",
#     "vt_symbol": "ETHUSDT.BINANCE",
#     "setting": {
#         "fast_window": 10.0,
#         "slow_window": 30.0,
#         "volume": 0.001,
#     }
# }
#     strategy_configuration('DualMAStrategy', strategy_settings)
#     # sleep(1)
#     # cta_engine.init_engine()
#     # cta_engine.stop_all_strategies()
#     cta_engine.add_strategy(DualMAStrategy, 'DualMAStrategy', strategy_settings['DualMAStrategy'])
#     cta_engine.load_strategy('DualMAStrategy')
    

# if __name__ == "__main__":
#     main()

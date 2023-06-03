
from howtrader.gateway.binance.binance_usdt_gateway import BinanceUsdtGateway
from howtrader.app.cta_strategy.strategies.dual_ma import DualMAStrategy
from howtrader.trader.ui import MainWindow, create_qapp
from howtrader.trader.engine import MainEngine
from howtrader.gateway.binance import BinanceUsdtGateway
from howtrader.event import EventEngine
from howtrader.app.cta_strategy import CtaStrategyApp
from vnpy_chartwizard import ChartWizardApp
from time import sleep
import multiprocessing
import json



event_engine: EventEngine = EventEngine()


def retrieveCreds():
    with open("howtrader/connect_binance_usdt.json") as f:
        data = json.load(f)
    return {
        "key": data["key"],
        "secret": data["secret"],
        "proxy_host": data["proxy_host"],
        "proxy_port": data["proxy_port"],
    }


def uploadStrategyConfig(ClassName: str, setting: dict):
    with open("howtrader/cta_strategy.json") as f:
        data = json.load(f)
    data[ClassName] = setting
    with open("howtrader/cta_strategy.json", "w") as f:
        json.dump(data, f, indent=4)


def get_settings():
    return {
        "class_name": "DualMAStrategy",
        "fast_window": 3,
        "slow_window": 7,
        "volume": 0.001,
    }


def main():
    qapp = create_qapp()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(BinanceUsdtGateway)
    gw = BinanceUsdtGateway(event_engine, gateway_name="BINANCE_USDT")
    gw.connect(setting=retrieveCreds())
    credentials = retrieveCreds()
    main_engine.connect(setting=credentials, gateway_name="BINANCE_USDT")

    cta_engine = main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(ChartWizardApp)

    cta_engine.init_engine()
    cta_engine.stop_all_strategies()
    cta_engine.add_strategy(class_name='MyDemoStrat', strategy_name='DualMAStrategy',
                            vt_symbol='BTCUSDT.BINANCE_USDT', setting=get_settings())
    cta_engine.init_all_strategies()

    # cta_engine.start_all_strategies()
    # sleep(2)
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()


if __name__ == "__main__":
    process = multiprocessing.Process(target=main)
    process.start()

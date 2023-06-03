import json
import multiprocessing
from vnpy_chartwizard import ChartWizardApp
from howtrader.app.cta_strategy import CtaStrategyApp
from howtrader.event import EventEngine
from howtrader.gateway.binance import BinanceUsdtGateway
from howtrader.trader.engine import MainEngine
from howtrader.trader.ui import MainWindow, create_qapp
event_engine: EventEngine = EventEngine()


def main():
    qapp = create_qapp()
    main_engine = MainEngine(event_engine)
    with open(
        "howtrader/connect_binance_usdt.json"
    ) as f:  # The credentials shoulb be stored in howtrader/connect_binance_usdt.json file for features gateway.
        config = json.load(f)
        key = config["key"]
        secret = config["secret"]
        proxy_host = config["proxy_host"]
        proxy_port = config["proxy_port"]
        user_profile = {
            "key": key,
            "secret": secret,
            "proxy_host": proxy_host,
            "proxy_port": proxy_port,
        }

    main_engine.add_gateway(BinanceUsdtGateway)
    main_engine.connect(setting=user_profile, gateway_name="BINANCE_USDT")
    cta_engine = main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(ChartWizardApp)

    cta_engine.init_engine()
    cta_engine.stop_all_strategies()
    cta_engine.init_all_strategies()
    # cta_engine.start_all_strategies()
    # sleep(2)
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()


if __name__ == "__main__":
    process = multiprocessing.Process(target=main)
    process.start()

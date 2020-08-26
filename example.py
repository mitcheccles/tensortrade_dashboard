import pandas as pd
import tensortrade.env.default as default
from tensortrade.data.cdd import CryptoDataDownload
from tensortrade.feed.core import Stream, DataFeed
from tensortrade.oms.exchanges import Exchange
from tensortrade.oms.services.execution.simulated import execute_order
from tensortrade.oms.instruments import USD, BTC, ETH
from tensortrade.oms.wallets import Wallet, Portfolio
from tensortrade.agents import DQNAgent
import tensortrade.env.default.actions as actions
import tensortrade.env.default.rewards as rewards
import tensortrade.env.default.stoppers as stoppers
import dashboard
import threading

ds = dashboard.DashboardServer()
t = threading.Thread(target=ds.run)
t.start()


def build_env():

    def rsi(price: Stream[float], period: float) -> Stream[float]:
        r = price.diff()
        upside = r.clamp_min(0).abs()
        downside = r.clamp_max(0).abs()
        rs = upside.ewm(alpha=1 / period).mean() / downside.ewm(alpha=1 / period).mean()
        return 100*(1 - (1 + rs) ** -1)

    cdd = CryptoDataDownload()
    data = cdd.fetch("Coinbase", "USD", "BTC", "1h")
    # data['vol'] = (data['volume'] - data['volume'].mean())/(data['volume'].max() - data['volume'].min())
    # data["roc"] = data["close"].pct_change(5).fillna(0)
    # data["rolling_fast"] = data['close'].rolling(13).mean().fillna(0)

    # data = load_csv("Coinbase_BTCUSD_1h.csv")

    features = []
    for c in data.columns[1:]:
        s = Stream.source(list(data[c]), dtype="float").rename(data[c].name)
        features += [s]

    cp = Stream.select(features, lambda s: s.name == "close")
    # vol = Stream.select(features, lambda s: s.name == "vol")
    # roc = Stream.select(features, lambda s: s.name == "roc")
    # fast = Stream.select(features, lambda s: s.name == "rolling_fast")
    features =[
        # rsi(cp, period=14).rename("rsi"),
        # vol,
        # roc,
        # fast,
        cp
    ]
    feed = DataFeed(features)
    feed.compile()

    coinbase = Exchange("coinbase", service=execute_order)(
        Stream.source(list(data["close"]), dtype="float").rename("USD-BTC")
    )

    cash = Wallet(coinbase, 10000 * USD)
    asset = Wallet(coinbase, 0 * BTC)

    portfolio = Portfolio(USD, [
        cash,
        asset
    ])

    renderer_feed = DataFeed([
        Stream.source(list(data["date"])).rename("date"),
        Stream.source(list(data["open"]), dtype="float").rename("open"),
        Stream.source(list(data["high"]), dtype="float").rename("high"),
        Stream.source(list(data["low"]), dtype="float").rename("low"),
        Stream.source(list(data["close"]), dtype="float").rename("close"),
        Stream.source(list(data["volume"]), dtype="float").rename("volume")
    ])

    reward_scheme = rewards.SimpleProfit()
    action_scheme = actions.BSH(cash, asset)

    # rend = mtc.MatplotlibTradingChart()

    env = default.create(
        portfolio=portfolio,
    #     action_scheme="managed-risk",
    #     reward_scheme="risk-adjusted",
        action_scheme=action_scheme,
        reward_scheme=reward_scheme,
        stopper=stoppers.MaxLossStopper(1000.0),
        feed=feed,
        renderer_feed=renderer_feed,
        renderer=default.renderers.PlotlyTradingChart(display=True, height=700, save_format="html"),
        # renderer=rend,
        window_size=20
    )
    return env


env = build_env()

def simple_trader(num_runs=10, n_steps=200):
    for i in range(num_runs):
        env.reset()
        action = 1
        for i in range(n_steps):
            env.render()
            dashboard.dashboard.update_figure(env.renderer.fig)
            action = action ^ 1
            ob, rew, done, info = env.step(action)

if __name__ == '__main__':
    simple_trader()

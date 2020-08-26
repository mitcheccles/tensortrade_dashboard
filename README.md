# Why?
Because I want to visualize trades in simulation runs.

# How?
Using [Dash](https://plotly.com/dash/); a framework for building apps and dashboards with plotly.

The dashboard in this repo works by creating a dash app, and running it on a thread, so not to block the execution of training. The graph is updated every 100 milliseconds via a callback setup on the dash app.

Steps:
1. import and create a dashboard in your training file or agent file:
```
import dashboard
import threading

ds = dashboard.DashboardServer()
t = threading.Thread(target=ds.run)
t.start()
```

2. Setup an environment with a `PlotlyTradingChart` renderer

3. In your training loop, after you call `env.render()` do:
```
dashboard.dashboard.update_figure(env.renderer.fig)
```

# What?

Run:
```
python3 example.py
```

To view the graph goto `localhost:8050`

![Live trading visualization](https://github.com/mitcheccles/tensortrade_dashboard/blob/master/vis.gif)

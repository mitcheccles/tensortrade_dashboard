# Why?
Because I want to visualize trades in simulation runs.

# How?
Using [Dash](https://plotly.com/dash/); a framework for building apps and dashboards with plotly.

The dashboard in this repo works by creating a dash app, and running it on a thread, so not to block the execution of training. The graph is updated every 100 milliseconds via a callback setup on the dash app.

# What?

Run:
```
python3 example.py
```

To view the graph goto `localhost:8050`

![Live trading visualization](https://github.com/mitcheccles/tensortrade_dashboard/blob/master/vis.gif)

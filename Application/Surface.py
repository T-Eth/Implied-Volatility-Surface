from Marketdata_API import optionsChain
import pandas as pd
import plotly.graph_objects as go

class Surface:
    def __init__(self, underlyingSymbol='AAPL', strikeFrom=80, strikeTo=120, side='call'):
        self.chain = optionsChain(underlyingSymbol, strikeFrom, strikeTo, side)
        self.plot_surface()

    def plot_surface(self):
        surface_df = self.chain.optionsChain.pivot(index='dte', columns='strike', values='iv')
        surface = go.Figure(data=[
                                    go.Surface(z=surface_df.values,
                                    x=surface_df.columns,
                                    y=surface_df.index)])
        surface.show()

def main():
    surface = Surface()
    print(surface.chain.optionsChain.head())
    print(surface.chain.optionsChain['iv'].head())
    print(surface.chain.optionsChain['dte'].head())
    print(surface.chain.optionsChain['strike'].head())

if __name__ == '__main__':
    main()
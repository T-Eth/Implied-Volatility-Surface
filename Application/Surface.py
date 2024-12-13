from Marketdata_API import optionsChain
import pandas as pd
import plotly.graph_objects as go

class Surface:
    def __init__(self, underlyingSymbol='AAPL', strikeFrom=70, strikeTo=130, side='call'):
        self.chain = optionsChain(underlyingSymbol, strikeFrom, strikeTo, side)
        self.plot_surface()

    def plot_surface(self):
        print(self.chain.optionsChain.head())
        print(self.chain.optionsChain.tail())
        surface_df = self.chain.optionsChain.pivot(index='dte', columns='strike', values='iv')
        surface = go.Figure(data=[
                                    go.Surface(z=surface_df.values,
                                    x=surface_df.index,
                                    y=surface_df.columns)])
        surface.update_layout(title='Implied Volatility Surface',
                                scene = dict(
                                                xaxis_title='Days to Expiration',
                                                yaxis_title='Strike',
                                                zaxis_title='Implied Volatility'))
        print("Before writing CSV")
        print(surface_df.index)
        surface_df.to_csv('ivdata.csv', index=True)
        print("After writing CSV")
        print(surface_df.index) 
        surface.show()

def main():
    surface = Surface()

if __name__ == '__main__':
    main()
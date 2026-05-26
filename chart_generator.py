import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd


def generate_chart(df, symbol):

    try:

        # =========================
        # COPY DATA
        # =========================

        chart_df = df.copy()

        # =========================
        # USE DATETIME INDEX
        # =========================

        if not isinstance(
            chart_df.index,
            pd.DatetimeIndex
        ):

            chart_df.index = pd.to_datetime(
                chart_df.index
            )

        # =========================
        # KEEP REQUIRED COLUMNS
        # =========================

        chart_df = chart_df[[

            'open',
            'high',
            'low',
            'close',
            'volume'
        ]]

        # =========================
        # LAST 120 CANDLES
        # =========================

        chart_df = chart_df.tail(120)

        # =========================
        # MARKET COLORS
        # =========================

        mc = mpf.make_marketcolors(

            up='#00ff88',

            down='#ff3355',

            edge='inherit',

            wick='inherit',

            volume='inherit'
        )

        # =========================
        # STYLE
        # =========================

        style = mpf.make_mpf_style(

            marketcolors=mc,

            facecolor='#0f172a',

            figcolor='#0f172a',

            edgecolor='#0f172a',

            gridcolor='#334155',

            gridstyle='--',

            y_on_right=True,

            rc={

                'axes.labelcolor': 'white',

                'xtick.color': 'white',

                'ytick.color': 'white',

                'text.color': 'white',

                'axes.titlecolor': 'white'
            }
        )

        # =========================
        # EMA LINES
        # =========================

        ema50 = chart_df['close'].ewm(
            span=50
        ).mean()

        ema200 = chart_df['close'].ewm(
            span=200
        ).mean()

        addplots = [

            mpf.make_addplot(

                ema50,

                color='#00bfff',

                width=1.2
            ),

            mpf.make_addplot(

                ema200,

                color='#ff9900',

                width=1.5
            )
        ]

        # =========================
        # CREATE CHART
        # =========================

        fig, axes = mpf.plot(

            chart_df,

            type='candle',

            style=style,

            volume=True,

            addplot=addplots,

            figsize=(12, 8),

            tight_layout=True,

            returnfig=True
        )

        # =========================
        # TITLE
        # =========================

        fig.suptitle(

            f"{symbol} Smart Signal Analysis",

            color='white',

            fontsize=16
        )

        # =========================
        # SAVE
        # =========================

        plt.savefig(

            "chart.png",

            dpi=150,

            bbox_inches='tight',

            facecolor='#0f172a'
        )

        plt.close()

        return "chart.png"

    except Exception as e:

        print(
            f"CHART ERROR: {e}",
            flush=True
        )

        return None
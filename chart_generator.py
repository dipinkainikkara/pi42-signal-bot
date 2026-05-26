import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd


# =========================
# GENERATE CHART
# =========================

def generate_chart(df, symbol):

    try:

        # =========================
        # COPY DATAFRAME
        # =========================

        chart_df = df.copy()

        # =========================
        # VALIDATION
        # =========================

        if chart_df.empty:

            print(
                "Chart dataframe empty",
                flush=True
            )

            return None

        # =========================
        # ENSURE TIMESTAMP INDEX
        # =========================

        if "timestamp" in chart_df.columns:

            chart_df["timestamp"] = pd.to_datetime(
                chart_df["timestamp"]
            )

            chart_df.set_index(
                "timestamp",
                inplace=True
            )

        elif not isinstance(
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

            "open",
            "high",
            "low",
            "close",
            "volume"
        ]]

        # =========================
        # LAST 120 CANDLES
        # =========================

        chart_df = chart_df.tail(120)

        # =========================
        # EMA CALCULATIONS
        # =========================

        chart_df["ema20"] = (

            chart_df["close"]

            .ewm(span=20)

            .mean()
        )

        chart_df["ema50"] = (

            chart_df["close"]

            .ewm(span=50)

            .mean()
        )

        # =========================
        # MARKET COLORS
        # =========================

        mc = mpf.make_marketcolors(

            up="#00ff88",

            down="#ff3355",

            edge="inherit",

            wick="inherit",

            volume="inherit"
        )

        # =========================
        # STYLE
        # =========================

        style = mpf.make_mpf_style(

            marketcolors=mc,

            facecolor="#0f172a",

            figcolor="#0f172a",

            edgecolor="#0f172a",

            gridcolor="#334155",

            gridstyle="--",

            y_on_right=True,

            rc={

                "axes.labelcolor":
                "white",

                "xtick.color":
                "white",

                "ytick.color":
                "white",

                "text.color":
                "white",

                "axes.titlecolor":
                "white",

                "figure.facecolor":
                "#0f172a",

                "savefig.facecolor":
                "#0f172a"
            }
        )

        # =========================
        # EMA OVERLAYS
        # =========================

        addplots = [

            mpf.make_addplot(

                chart_df["ema20"],

                color="#00bfff",

                width=1.2
            ),

            mpf.make_addplot(

                chart_df["ema50"],

                color="#ff9900",

                width=1.5
            )
        ]

        # =========================
        # CREATE CHART
        # =========================

        fig, axes = mpf.plot(

            chart_df,

            type="candle",

            style=style,

            volume=True,

            addplot=addplots,

            figsize=(14, 8),

            tight_layout=True,

            returnfig=True
        )

        # =========================
        # TITLE
        # =========================

        fig.suptitle(

            f"{symbol} Pi42 Futures Analysis",

            color="white",

            fontsize=16
        )

        # =========================
        # SAVE FILE
        # =========================

        chart_path = "chart.png"

        plt.savefig(

            chart_path,

            dpi=150,

            bbox_inches="tight",

            facecolor="#0f172a"
        )

        plt.close()

        print(
            f"Chart saved: {chart_path}",
            flush=True
        )

        return chart_path

    except Exception as e:

        print(
            f"CHART ERROR: {e}",
            flush=True
        )

        return None
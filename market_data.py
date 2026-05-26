import logging
import time
import pandas as pd
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class Pi42MarketDataError(Exception):
    pass


class Pi42MarketData:

    BASE_URL = "https://api.pi42.com/v1/market/klines"

    VALID_PAIRS = [
        "BTCINR",
        "ETHINR",
        "SOLINR"
    ]

    VALID_INTERVALS = [
        "1m",
        "5m",
        "15m",
        "30m",
        "1h",
        "4h",
        "1d"
    ]

    def __init__(self):

        self.timeout = 20
        self.session = self._create_session()

        logger.info(
            "Pi42MarketData initialized"
        )

    def _create_session(self):

        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504
            ],
            allowed_methods=["POST"]
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        session.mount(
            "https://",
            adapter
        )

        return session

    def get_klines(
        self,
        pair="BTCINR",
        interval="15m",
        limit=200
    ):

        logger.info(
            f"Fetching klines {pair} {interval}"
        )

        if pair not in self.VALID_PAIRS:

            raise Pi42MarketDataError(
                f"Invalid pair: {pair}"
            )

        if interval not in self.VALID_INTERVALS:

            raise Pi42MarketDataError(
                f"Invalid interval: {interval}"
            )

        payload = {
            "pair": pair,
            "interval": interval,
            "limit": limit
        }

        logger.info(
            f"Payload: {payload}"
        )

        try:

            time.sleep(0.2)

            response = self.session.post(
                self.BASE_URL,
                json=payload,
                timeout=self.timeout
            )

            logger.info(
                f"HTTP Status: {response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            logger.info(
                f"Response received with {len(data)} candles"
            )

            if isinstance(data, list):

                klines = data

            elif isinstance(data, dict):

                klines = data.get(
                    "data",
                    data.get("result", [])
                )

            else:

                raise Pi42MarketDataError(
                    f"Unexpected response: {type(data)}"
                )

            if not klines:

                logger.warning(
                    "No candle data returned"
                )

                return self._empty_dataframe()

            df = self._parse_klines(
                klines
            )

            logger.info(
                f"Fetched {len(df)} candles"
            )

            return df

        except requests.exceptions.RequestException as e:

            raise Pi42MarketDataError(
                f"Request failed: {e}"
            )

    def _parse_klines(
        self,
        klines
    ):

        records = []

        for candle in klines:

            try:

                if isinstance(candle, dict):

                    records.append({

                        "timestamp":
                        candle.get("startTime"),

                        "open":
                        candle.get("open"),

                        "high":
                        candle.get("high"),

                        "low":
                        candle.get("low"),

                        "close":
                        candle.get("close"),

                        "volume":
                        candle.get("volume")
                    })

                elif isinstance(
                    candle,
                    (list, tuple)
                ):

                    if len(candle) >= 6:

                        records.append({

                            "timestamp":
                            candle[0],

                            "open":
                            candle[1],

                            "high":
                            candle[2],

                            "low":
                            candle[3],

                            "close":
                            candle[4],

                            "volume":
                            candle[5]
                        })

            except Exception as e:

                logger.warning(
                    f"Skipping candle: {e}"
                )

        if not records:

            return self._empty_dataframe()

        df = pd.DataFrame(records)

        df["timestamp"] = pd.to_datetime(
            df["timestamp"].astype(float),
            unit="ms",
            errors="coerce"
        )

        for col in [
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df.dropna(inplace=True)

        df.sort_values(
            "timestamp",
            inplace=True
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    def _empty_dataframe(self):

        return pd.DataFrame(
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

    def close(self):

        self.session.close()

        logger.info(
            "Session closed"
        )


def get_candles(
    pair="BTCINR",
    interval="15m",
    limit=200
):

    fetcher = Pi42MarketData()

    try:

        return fetcher.get_klines(
            pair=pair,
            interval=interval,
            limit=limit
        )

    finally:

        fetcher.close()


if __name__ == "__main__":

    try:

        df = get_candles(
            pair="BTCINR",
            interval="15m",
            limit=20
        )

        print("\n===================")
        print("DATAFRAME")
        print("===================\n")

        print(df)

    except Exception as e:

        print("\nERROR:", e)
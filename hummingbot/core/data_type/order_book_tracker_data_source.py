#!/usr/bin/env python

from abc import (
    ABCMeta,
    abstractmethod
)
import asyncio
from typing import (
    Callable,
    Dict,
    List,
)
from hummingbot.core.data_type.order_book import OrderBook, OrderBookMessage


class OrderBookTrackerDataSource(metaclass=ABCMeta):

    def __init__(self, trading_pairs: List[str]):
        self._trading_pairs: List[str] = trading_pairs
        self._order_book_create_function = lambda: OrderBook()

    @property
    def order_book_create_function(self) -> Callable[[], OrderBook]:
        return self._order_book_create_function

    @order_book_create_function.setter
    def order_book_create_function(self, func: Callable[[], OrderBook]):
        self._order_book_create_function = func

    @classmethod
    async def get_last_traded_prices(cls, trading_pairs: List[str]) -> Dict[str, float]:
        raise NotImplementedError

    @abstractmethod
    async def get_order_book_snapshot_message(self, trading_pair: str) -> OrderBookMessage:
        raise NotImplementedError

    @abstractmethod
    async def listen_for_order_book_diffs(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        """
        Object type in the output queue must be OrderBookMessage
        """
        raise NotImplementedError

    @abstractmethod
    async def listen_for_order_book_snapshots(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        """
        Object type in the output queue must be OrderBookMessage
        """
        raise NotImplementedError

    @abstractmethod
    async def listen_for_trades(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue):
        """
        Object type in the output queue must be OrderBookMessage
        """
        raise NotImplementedError

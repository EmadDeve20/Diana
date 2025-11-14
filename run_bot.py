#!/usr/bin/env python3
import asyncio

from diana.bot import run_bot
from diana.database import create_all_tables


def main() -> None:
    asyncio.run(create_all_tables())
    run_bot()


if __name__ == "__main__":

    main()


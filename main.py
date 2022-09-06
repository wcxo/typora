#!/usr/bin/env python
from subprocess import Popen
from argparse import ArgumentParser
from typing import Any
from time import strptime, mktime
from sys import executable
from re import findall
import os


class make:

    typora = "typora.py"
    license = "dec_app/License.js"

    def __init__(self, asar) -> None:
        date = strptime('20991231235959', "%Y%m%d%H%M%S")
        self.date = str(int(mktime(date) * 1000))
        self.root = os.path.split(asar)[0]
        self.asar = asar

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        Popen([executable, self.typora, self.asar, "."]).wait()

        self._do()

        Popen([executable, self.typora, "-u", "dec_app", self.root]).wait()

    def _do(self):
        with open(self.license, "r", encoding="UTF-8") as f:
            license = f.read()

        for date in findall(r"(\d{12,14})", license):
            license = license.replace(date, self.date)

        with open(self.license, "wb") as f:
            f.write(license.encode("UTF-8"))


if __name__ == "__main__":

    args = ArgumentParser(
        description="[extract and decryption / pack and encryption] app.asar file from [Typora].",
        epilog="If you have any questions, please contact [ MasonShi@88.com ]",
    )
    args.add_argument("asar", type=str, help="app.asar file path/dir [input/ouput]")
    args = args.parse_args()
    make(args.asar)()

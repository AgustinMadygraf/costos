"""
CLI unificada para ejecutar comandos de costos.
"""

from __future__ import annotations

import argparse
import os
from typing import Sequence

from src.main import main as equilibrio_main
from src.main_mix import main as mix_main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="costos",
        description="CLI de costos: calcula equilibrio o muestra mix de ventas.",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nivel de logs (default: INFO).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Atajo para --log-level DEBUG.",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("equilibrio", help="Calcula y muestra punto de equilibrio.")
    subparsers.add_parser("mix", help="Muestra solo el mix de ventas.")
    parser.set_defaults(command="equilibrio")
    return parser


def run_cli(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    os.environ["LOG_LEVEL"] = "DEBUG" if args.debug else args.log_level

    from src.infrastructure.settings import get_logger

    logger = get_logger(__name__)
    logger.debug("CLI command=%s log_level=%s", args.command, os.environ["LOG_LEVEL"])

    try:
        if args.command == "mix":
            mix_main()
            return 0
        equilibrio_main()
        return 0
    except Exception as exc:  # pragma: no cover
        logger.error("Error ejecutando comando '%s': %s", args.command, exc)
        logger.debug("Detalle de error", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(run_cli())


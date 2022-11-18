#!/usr/bin/env python3

import os
import click
from dotenv import load_dotenv
import logging
import sys

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


@click.command()
@click.option(
    "--input-file", help="Input file", type=click.File("rt"), default=sys.stdin
)
@click.option(
    "--output-file", help="Output file", type=click.File("at"), default=sys.stdout
)
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
)
def main(input_file, output_file, log_level):
    """Console script for {{cookiecutter.project_slug}}."""
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logging.getLogger().setLevel(log_levels[log_level])
    if input_file.isatty():
        logging.critical("Input from stdin which is a tty - aborting")
        return 128
    with input_file:
        data = input_file.read()
    return 0


if __name__ == "__main__":
    main()

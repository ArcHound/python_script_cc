#!/usr/bin/env python3

import os
import click
import json
import csv
from dotenv import load_dotenv
import logging
import sys

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)

@click.command()
{%- if cookiecutter.file_input == "Yes" %}
@click.option(
    "--input-file", help="Input file [default: STDIN]", type=click.File("rt"), default=sys.stdin
)
{%- endif %}
{%- if cookiecutter.file_output == "Yes" %}
@click.option(
    "--output-file", help="Output file [default: STDOUT]", type=click.File("at"), default=sys.stdout
)
{%- endif %}
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
)
def main(
{%- if cookiecutter.file_input == "Yes" %}
        input_file, 
{%- endif %}
{%- if cookiecutter.file_output == "Yes" %}
        output_file, 
{%- endif %}
        log_level):
    """Console script for {{cookiecutter.project_slug}}."""
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logging.getLogger(__name__).setLevel(log_levels[log_level])
    # ======================================================================
    #                        Your script starts here!
    # ======================================================================
{%- if cookiecutter.file_input == "Yes" %}
    if input_file.isatty():
        logging.critical("Input from stdin which is a tty - aborting")
        return 128
    with input_file:
        in_data = input_file.read()
{%- endif %}
    return 0


if __name__ == "__main__":
    log.info("Starting...")
    main()
    log.info("Finishing.")

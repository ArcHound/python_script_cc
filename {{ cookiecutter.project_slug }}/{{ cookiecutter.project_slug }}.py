#!/usr/bin/env python3

import os
import json
import csv
import logging
import sys
import time
from functools import update_wrapper

import click
from dotenv import load_dotenv
{%- if cookiecutter.use_requests == "Yes" %}
import requests
{%- endif %}
{%- if cookiecutter.use_requests_cache == "Yes" %}
import requests_cache

requests_cache.install_cache(cache_name="{{ cookiecutter.requests_cache_name }}", backend="sqlite", expire_after=10800)
{%- endif %}

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)

log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
}

def log_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        log.setLevel(log_levels[ctx.params["log_level"]])
        log.info("Starting")
        r =  ctx.invoke(f,  *args, **kwargs)
        log.info("Finishing")
        return r
    return update_wrapper(new_func, f)

def time_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        t1 = time.perf_counter()
        r =  ctx.invoke(f,  *args, **kwargs)
        t2 = time.perf_counter()
        log.info(f"Execution in {t2-t1:0.4f} seconds")
        return r
    return update_wrapper(new_func, f)

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
{%- if cookiecutter.use_requests == "Yes" %}
@click.option(
    "--{{ cookiecutter.service_name }}-token",
    type=str,
    envvar="{{ cookiecutter.service_name|upper }}_TOKEN",
    required=True,
    help="Token for {{ cookiecutter.service_name }} API",
)
@click.option(
    "--{{ cookiecutter.service_name }}-url",
    type=str,
    envvar="{{ cookiecutter.service_name|upper }}_URL",
    default="{{ cookiecutter.service_url }}",
    help="Base URL for {{ cookiecutter.service_name }}",
)
@click.option(
    "--proxy",
    is_flag=True,
    help="Whether to use the proxy",
    envvar="PROXY",
)
@click.option(
    "--proxy-address",
    default="http://localhost:8080",
    help="Proxy address",
    envvar="PROXY_ADDRESS",
)
{%- endif %}
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
    envvar="LOG_LEVEL"
)
@log_decorator
@time_decorator
def main(
{%- if cookiecutter.file_input == "Yes" %}
        input_file, 
{%- endif %}
{%- if cookiecutter.file_output == "Yes" %}
        output_file, 
{%- endif %}
{%- if cookiecutter.use_requests == "Yes" %}
        {{ cookiecutter.service_name }}_token,
        {{ cookiecutter.service_name }}_url,
        proxy,
        proxy_address,
{%- endif %}
        log_level):
    """Console script for {{cookiecutter.project_slug}}."""
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
{%- if cookiecutter.use_requests == "Yes" %}
    proxies = {"http": proxy_address, "https": proxy_address}

    log.info("Init service session...")
    {{ cookiecutter.service_name }}_session = requests.Session()
    {{ cookiecutter.service_name }}_session.headers.update({"Authorization": "Bearer {}".format({{ cookiecutter.service_name }}_token)})
    if proxy:
        log.info("Got proxy {} for service {}".format(proxies, "{{ cookiecutter.service_name }}"))
        {{ cookiecutter.service_name }}_session.proxies.update(proxies)
        {{ cookiecutter.service_name }}_session.verify = False

{%- endif %}
    return 0


if __name__ == "__main__":
    main()

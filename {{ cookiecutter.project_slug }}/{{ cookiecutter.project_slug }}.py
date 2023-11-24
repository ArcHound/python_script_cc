#!/usr/bin/env python3

import os
import json
import csv
import logging
import sys
import time
import math
from functools import update_wrapper
import cProfile
import pstats

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
        try:
            r = ctx.invoke(f, *args, **kwargs)
            return r
        except Exception as e:
            raise e
        finally:
            t2 = time.perf_counter()
            mins = math.floor(t2-t1) // 60
            hours = mins // 60
            secs = (t2-t1) - 60 * mins - 3600 * hours
            log.info(f"Execution in {hours:02d}:{mins:02d}:{secs:0.4f}")
        
    return update_wrapper(new_func, f)


{%- if cookiecutter.profiling == "Yes" %}
def profile_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if ctx.params["profiling"]:
            with cProfile.Profile() as profile:
                r = ctx.invoke(f, *args, **kwargs)
                with open(ctx.params["profiling_file"], "w") as sfs:
                    pstats.Stats(profile, stream=sfs).strip_dirs().sort_stats(
                        ctx.params["profiling_sort_key"]
                    ).print_stats()
                return r
        else:
            r = ctx.invoke(f, *args, **kwargs)
            return r

    return update_wrapper(new_func, f)
{%- endif %}


@click.command()
{%- if cookiecutter.file_input == "Yes" %}
@click.option(
    "--input-file",
    help="Input file [default: STDIN]",
    type=click.Path(readable=True, file_okay=True, dir_okay=False),
    default="-",
)
{%- endif %}
{%- if cookiecutter.file_output == "Yes" %}
@click.option(
    "--output-file",
    help="Output file [default: STDOUT]",
    type=click.Path(readable=True, file_okay=True, dir_okay=False),
    default="-",
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
{%- if cookiecutter.profiling == "Yes" %}
@click.option(
    "--profiling",
    default=False,
    is_flag=True,
    help="Profile the program - get performance data",
)
@click.option(
    "--profiling-file",
    help="Profiling output file",
    type=click.Path(writable=True, file_okay=True, dir_okay=False),
    default=f"/tmp/{{cookiecutter.project_slug}}_profile.log",
    show_default=True,
)
@click.option(
    "--profiling-sort-key",
    help="Profiling sort key",
    type=click.Choice(
        [
            "calls",
            "cumulative",
            "cumtime",
            "file",
            "filename",
            "module",
            "ncalls",
            "pcalls",
            "line",
            "name",
            "nfl",
            "stdname",
            "time",
            "tottime",
        ]
    ),
    default="cumulative",
    show_default=True,
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
{%- if cookiecutter.profiling == "Yes" %}
@profile_decorator
{%- endif %}
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
{%- if cookiecutter.profiling == "Yes" %}
        profiling,
        profiling_file,
        profiling_sort_key,
{%- endif %}
        log_level):
    """Console script for {{cookiecutter.project_slug}}."""
    # ======================================================================
    #                        Your script starts here!
    # ======================================================================
{%- if cookiecutter.file_input == "Yes" %}
    if input_file == "-" and sys.stdin.isatty():
        logging.critical("Input from stdin which is a tty - aborting")
        return 128
    with click.open_file(input_file, "r") as f:
        in_data = f.read()

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
{%- if cookiecutter.file_output == "Yes" %}
    with click.open_file(output_file, "w") as f:
        f.write("Hello, world!")
{%- endif %}
    return 0


if __name__ == "__main__":
    main()

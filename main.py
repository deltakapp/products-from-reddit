from datetime import datetime, timedelta

import click
import pandas as pd
import requests

import reddit_auth
from crawl import full_crawl


@click.group()
def cli():
  """Entry point for CLI"""
  pass

@click.command()
@click.option('--start', default = None, help = 'what past datetime to crawl posts (utc)')
@click.option('--duration', default = None, help = 'the timedelta before present to crawl posts to')
def crawl(start, duration):
  "Fetch posts within specified timeframe"

  # generate start parameters if not specified
  if not start:
    if not duration:
      duration = timedelta(days = 30, minutes = 10)
    start = datetime.utcnow() - duration

  start_time = start
  print(start_time)

  full_crawl(start_time)

@click.command()
def scrape():
  """stub of scrape command"""
  click.echo('scrape command called')

cli.add_command(crawl)
cli.add_command(scrape)

# Runs CLI from script
if __name__ == "__main__":
  cli()
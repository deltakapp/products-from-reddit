from datetime import datetime, timedelta

import click

from crawl import full_crawl
from scrape import scrape_posts


@click.group()
def cli():
  """Entry point for CLI"""
  pass

@click.command()
@click.option(
  '--start',
   help = 'specify past date to crawl posts to (YYYY-MM-DD)',
   type=click.types.DateTime(),
   )
def crawl(start):
  """Fetch posts within specified timeframe."""

  if start:
    # Verify start is valid past datetime
    if start >= datetime.utcnow():
      click.echo("Error: start must be before present time")
      return

  else:
    # Supply default start
    start = (datetime.utcnow() - timedelta(days = 30, minutes = 10))

  click.echo(f"Crawling posts since {start}")

  full_crawl(start)
  click.echo("Crawling complete")

@click.command()
def scrape():
  """stub of scrape command"""
  click.echo('scrape command called')

  scrape_posts()


cli.add_command(crawl)
cli.add_command(scrape)

# Runs CLI from script
if __name__ == "__main__":
  cli()
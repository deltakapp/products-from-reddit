from datetime import datetime, timedelta

import click

from crawl import full_crawl


@click.group()
def cli():
  """Entry point for CLI"""
  pass

@click.command()
@click.option('--start', help = 'specify past timestamp to crawl posts to')
def crawl(start):
  "Fetch posts within specified timeframe"

  if start:

    # Parse start option into datetime format
    start = datetime.utcfromtimestamp(float(start))

    # Verify start is valid past datetime
    if start >= datetime.utcnow():
      click.echo("Error: start must be before present time")
      return

  else:
    # Supply default start
    # Note: click doesn't allow custom parameter types like datetime or timestamp
    # without explicit implementation
    start = (datetime.utcnow() - timedelta(days = 30, minutes = 10))

  full_crawl(start)
  click.echo("crawling complete")

@click.command()
def scrape():
  """stub of scrape command"""
  click.echo('scrape command called')

cli.add_command(crawl)
cli.add_command(scrape)

# Runs CLI from script
if __name__ == "__main__":
  cli()
import click


@click.group()
def cli():
  """Entry point for CLI"""
  pass

@click.command()
def crawl():
  """stub of crawl command"""
  click.echo('crawl command called')

@click.command()
def scrape():
  """stub of scrape command"""
  click.echo('scrape command called')

cli.add_command(crawl)
cli.add_command(scrape)

# Runs CLI from script
if __name__ == "__main__":
  cli()
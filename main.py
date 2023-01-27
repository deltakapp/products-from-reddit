import click


# Entry point for CLI
@click.group()
def cli():
  pass

# stub of crawl command
@click.group()
def crawl():
  pass

# stub of scrape command
@click.group()
def scrape():
  pass

cli.add_command(crawl)
cli.add_command(scrape)

# Runs CLI from script
if __name__ == "__main__":
  cli()
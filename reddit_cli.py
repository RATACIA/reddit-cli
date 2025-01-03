#!/usr/bin/env python3
import requests
import click

BASE_URL = "https://www.reddit.com"

@click.command()
@click.argument("subreddit", default="all")
@click.option("--filter", default="hot", help="Filter posts (hot, new, top, rising)")
def browse(subreddit, filter):
    """Browse Reddit posts."""
    url = f"{BASE_URL}/r/{subreddit}/{filter}.json"
    response = requests.get(url, headers={"User-Agent": "cli-tool"})
    if response.status_code == 200:
        posts = response.json()["data"]["children"]
        for idx, post in enumerate(posts):
            data = post["data"]
            click.echo(f"{idx + 1}. {data['title']} ({data['url']})")
    else:
        click.echo(f"Error: {response.status_code}")

if __name__ == "__main__":
    browse()

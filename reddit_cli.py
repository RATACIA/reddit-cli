#!/usr/bin/env python3
import requests
import click

BASE_URL = "https://www.reddit.com"

@click.command()
@click.argument("subreddit", default="all")
@click.option("--filter", type=click.Choice(['hot', 'new', 'top', 'rising'], case_sensitive=False), default='hot')
def browse(subreddit, filter):
    """Browse Reddit posts and view details with comments."""
    url = f"{BASE_URL}/r/{subreddit}/{filter}.json"
    response = requests.get(url, headers={"User-Agent": "cli-tool"})
    if response.status_code == 200:
        posts = response.json()["data"]["children"]
        for idx, post in enumerate(posts):
            data = post["data"]
            click.echo(f"{idx + 1}. {data['title']} ({data['url']})")
        
        # Prompt the user to select a post
        selected = click.prompt(
            "Enter the number of the post to view its details (or 0 to exit)",
            type=int,
            default=0
        )
        if selected == 0:
            click.echo("Exiting.")
            return

        if 1 <= selected <= len(posts):
            post_data = posts[selected - 1]["data"]
            view_post_details(post_data)
        else:
            click.echo("Invalid selection.")
    else:
        click.echo(f"Error: {response.status_code}")

def view_post_details(post_data):
    """View post details and fetch top 5 comments."""
    post_title = post_data["title"]
    post_url = post_data["url"]
    permalink = post_data["permalink"]

    click.echo(f"\n{post_title}\n{post_url}\n{'=' * 50}")

    # Fetch comments
    comments_url = f"{BASE_URL}{permalink}.json"
    response = requests.get(comments_url, headers={"User-Agent": "cli-tool"})
    if response.status_code == 200:
        comments_data = response.json()
        comments = comments_data[1]["data"]["children"]  # Comments are in the second part of the JSON

        click.echo("\nTop 5 Comments:\n")
        for idx, comment in enumerate(comments[:10]):
            if "body" in comment["data"]:
                click.echo(f"{idx + 1}. {comment['data']['body']}\n")
    else:
        click.echo(f"Error fetching comments: {response.status_code}")

if __name__ == "__main__":
    browse()

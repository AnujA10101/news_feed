import calendar
from datetime import datetime, timezone
from database import SessionLocal, init_db
import feedparser
from models import Article


def fetch_articles(
    feed_url: str,
    source: str,
    category: str,
) -> list[Article]:

    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        published = entry.get("published_parsed")

        published_at = (
            datetime.fromtimestamp(
                calendar.timegm(published),
                tz=timezone.utc,
            )
            if published
            else None
        )

        thumbnails = entry.get("media_thumbnail", [])
        image_url = thumbnails[0].get("url") if thumbnails else None

        article = Article(
            title=entry.get("title", ""),
            url=entry.get("link", ""),
            description=entry.get("summary", ""),
            source=source,
            category=category,
            published_at=published_at,
            external_id=entry.get("id"),
            image_url=image_url,
        )

        articles.append(article)

    return articles


if __name__ == "__main__":
    init_db()

    articles = fetch_articles(
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        source="BBC",
        category="World",
    )

    with SessionLocal() as session:
        for article in articles:
            existing = session.query(Article).filter_by(
                url=article.url
            ).first()

            if existing is None:
                session.add(article)

        session.commit()

    print(f"Processed {len(articles)} articles")
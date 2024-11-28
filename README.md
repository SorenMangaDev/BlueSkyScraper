# BlueSkyScraper

A Python script to collect posts from Bluesky's timeline using the official AT Protocol. The script fetches posts and saves them as CSV files with configurable parameters for data collection.

## Features

- Collects post content, engagement metrics, and metadata
- Configurable data collection parameters
- Rate limiting to respect API constraints
- Error handling with automatic retries
- CSV output with optional timestamped filenames
- Basic statistics reporting

## Setup

1. Clone the repository:
```bash
git clone https://github.com/SorenMangaDev/BlueSkyScraper.git
cd BlueSkyScraper
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv bsky_env

# Activate on Windows
bsky_env\Scripts\activate

# Activate on macOS/Linux
source bsky_env/bin/activate
```

3. Install dependencies:
```bash
pip install atproto pandas
```

## Configuration

Edit these parameters at the top of `bsky_scraper.py`:

```python
# Authentication
USERNAME = "your.email@example.com"
PASSWORD = "your_password"

# Collection Parameters
MAX_POSTS = 100            # Maximum posts to fetch
POSTS_PER_REQUEST = 50     # Posts per API call
RATE_LIMIT_DELAY = 1       # Delay between calls (seconds)

# Output Settings
OUTPUT_DIR = "data"        # Save directory
INCLUDE_TIMESTAMP = True   # Add timestamp to filename
```

## Usage

1. Configure your Bluesky credentials in the script
2. Run the script:
```bash
python bsky_scraper.py
```

The script will create a CSV file in the specified output directory with collected posts.

## Output

The CSV includes these fields:
- post_id: Unique identifier for the post
- author: Bluesky handle
- author_display_name: Display name of the author
- text: Post content
- created_at: Post timestamp
- likes: Like count
- reposts: Repost count
- replies: Reply count (if enabled)
- has_images: Whether post contains images (if enabled)
- image_count: Number of images (if enabled)
- is_quote: Whether it's a quote post (if enabled)

## License

MIT

## Disclaimer

This tool uses Bluesky's official API and includes rate limiting. Always respect Bluesky's terms of service and API guidelines.

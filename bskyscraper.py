import pandas as pd
from atproto import Client
from datetime import datetime
import time

# Authentication Settings
USERNAME = "example.bsky.social"  # or your handle
PASSWORD = "password"

# Data Collection Parameters
MAX_POSTS = 100            # Maximum number of posts to fetch
POSTS_PER_REQUEST = 50     # Number of posts to fetch per API call
RATE_LIMIT_DELAY = 1       # Delay between API calls in seconds

# Output Settings
OUTPUT_DIR = "data"        # Directory to save the CSV file
INCLUDE_TIMESTAMP = True   # Whether to include timestamp in filename
CSV_FILENAME = "bluesky_posts"  # Base filename (without timestamp/extension)

# Data Collection Settings
COLLECT_IMAGES = True      # Whether to collect image metadata
COLLECT_REPLIES = True     # Whether to collect reply counts
COLLECT_QUOTES = True      # Whether to collect quote post information
MAX_RETRIES = 3           # Number of retries for failed API calls

def fetch_bluesky_posts():
    """
    Fetch posts from Bluesky and save them as a CSV file using the configured parameters.
    """
    # Initialize the client
    client = Client()
    
    try:
        # Login to Bluesky
        client.login(USERNAME, PASSWORD)
        
        # Initialize empty lists to store post data
        posts_data = []
        cursor = None
        retries = 0
        
        while len(posts_data) < MAX_POSTS:
            try:
                # Fetch timeline posts
                response = client.get_timeline(limit=POSTS_PER_REQUEST, cursor=cursor)
                
                for post in response.feed:
                    # Extract post data
                    post_data = {
                        'post_id': post.post.uri.split('/')[-1],
                        'author': post.post.author.handle,
                        'author_display_name': post.post.author.display_name,
                        'text': post.post.record.text,
                        'created_at': post.post.record.created_at,
                        'likes': post.post.like_count,
                        'reposts': post.post.repost_count,
                    }
                    
                    # Add optional data based on settings
                    if COLLECT_REPLIES:
                        post_data['replies'] = post.post.reply_count
                    
                    if COLLECT_IMAGES:
                        post_data['has_images'] = hasattr(post.post.embed, 'images')
                        post_data['image_count'] = len(post.post.embed.images) if hasattr(post.post.embed, 'images') else 0
                    
                    if COLLECT_QUOTES:
                        post_data['is_quote'] = hasattr(post.post.record, 'quote')
                        if hasattr(post.post.record, 'quote'):
                            post_data['quoted_post'] = post.post.record.quote.uri
                    
                    posts_data.append(post_data)
                    
                    if len(posts_data) >= MAX_POSTS:
                        break
                
                # Reset retry counter on successful request
                retries = 0
                
                # Update cursor for pagination
                cursor = response.cursor
                if not cursor or len(response.feed) == 0:
                    break
                    
                # Respect rate limits
                time.sleep(RATE_LIMIT_DELAY)
                
            except Exception as e:
                retries += 1
                if retries >= MAX_RETRIES:
                    print(f"Maximum retries ({MAX_RETRIES}) reached. Stopping.")
                    break
                print(f"Error occurred, retrying ({retries}/{MAX_RETRIES}): {str(e)}")
                time.sleep(RATE_LIMIT_DELAY * 2)  # Longer delay on retry
        
        # Convert to DataFrame
        df = pd.DataFrame(posts_data)
        
        # Convert timestamps to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Create output directory if it doesn't exist
        import os
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{CSV_FILENAME}{'_' + timestamp if INCLUDE_TIMESTAMP else ''}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Successfully saved {len(posts_data)} posts to {filepath}")
        
        # Print statistics
        print("\nBasic Statistics:")
        print(f"Total posts collected: {len(df)}")
        print(f"Unique authors: {df['author'].nunique()}")
        if COLLECT_IMAGES:
            print(f"Posts with images: {df['has_images'].sum()}")
        print(f"Average likes per post: {df['likes'].mean():.2f}")
        print(f"Average reposts per post: {df['reposts'].mean():.2f}")
        
        return df
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    df = fetch_bluesky_posts()
# Instagram Basic Display API Configuration
INSTAGRAM_API_URL = "https://graph.instagram.com"
INSTAGRAM_OAUTH_URL = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_TOKEN_URL = "https://api.instagram.com/oauth/access_token"

# You'll need to replace these with your actual Instagram Basic Display API credentials
INSTAGRAM_APP_ID = "YOUR_APP_ID"
INSTAGRAM_APP_SECRET = "YOUR_APP_SECRET"
INSTAGRAM_REDIRECT_URI = "http://localhost:8000/auth/instagram/callback"

# API Endpoints
INSTAGRAM_MEDIA_ENDPOINT = f"{INSTAGRAM_API_URL}/me/media"
INSTAGRAM_MEDIA_DETAILS_ENDPOINT = f"{INSTAGRAM_API_URL}/{{media_id}}"

# Headers for API requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# URL Shortener Project

## Task Description
It was my first machine coding round that i appeared for at a Mumbai-Based Startup
Design a server capable of generating, tracking, and managing shortened URLs with specific functionalities. The server should offer various endpoints for interaction:

### Features
- **Custom Aliases**: Users can suggest custom URLs.
- **Random Alias**: If no custom alias is provided, a random alias will be generated. A new shortened URL is generated every time, even for the same original URL.
- **TTL (Time to Live)**: Each alias has a TTL. Users can specify the duration, with a default of 120 seconds.
- **Redirection**: Redirect users to the long URL based on the alias provided.
- **Analytics**: Retrieve information about the shortened URLs, including the number of visits and the last 10 access times.
- **Update**: Update the custom alias and TTL of the specified existing shortened URL. When updated, analytics data of the old alias will be deleted.
- **Delete**: Remove the specified existing shortened URL.

The mapping for the shortened URLs must be deleted from the datastore once the TTL duration has passed.

### Constraints
- Ensure quick redirections with low latency.
- Implement the solution with in-memory variables (no databases).
- Aim for O(log n) or O(1) complexity for scalability and efficiency.

## API Specification

### 1. Shortening URLs
**Endpoint:** `POST /shorten`  
**Description:** Generate a short, unique alias for a given long URL. Optionally, a custom alias and a time-to-live (TTL) can be specified.  
**Request Body:**
```json
{
  "long_url": "https://www.example.com/some/very/long/url",
  "custom_alias": "myalias",    // Optional
  "ttl_seconds": 60             // Optional
}

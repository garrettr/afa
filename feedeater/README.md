feedeater
---------

## Database schema:
Feed: A dynamic source of content. Could be a Facebook page, a Twitter account, or an RSS/Atom feed.
Entry: an item of content from a feed. i.e. a Facebook post, Tweet, etc.

Model of interaction:
To avoid running up against rate limits, for now when a new Feed is saved to the databse, we will:

1.  Try to access it, filling in metadata about the Feed if we can
2.  Save **all** previous posts, or at least links/excerpts. 
3.  Get ready to poll in the future, will be triggered by a custom django-admin command

## Dependencies:

1.  [Universal Feed Parser]
2.  [python-twitter]

For RSS/Atom and Twitter, you don't need to authenticate to access the data that we need to access.

We need an access token to get to a Facebook user or Page's feed.
[Graph API Documentation](https://developers.facebook.com/docs/reference/api/)
[App Login/Tokens](https://developers.facebook.com/docs/authentication/#app-login)

I decided to just use the Graph API directly with great success!

[Universal Feed Parser]: http://www.feedparser.org/docs/introduction.html
[python-twitter]: http://code.google.com/p/python-twitter/

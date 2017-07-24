# Twitter-Sentiment-Analysis
Monitoring and Exporting of live tweets of twitter users and doing Sentiment Analysis on them.

This application basically consists of 3 main areas to focus:

1. Monitoring : Real time streaming of tweets on screen and it's respective sentimental value

2. Downloading / Exporting : Exporting the tweet data with details including 
    - Tweet created_at, 
    - User's screen_name, 
    - language of tweet, 
    - Tweet text, 
    - UserProfileName, 
    - UserDescription, 
    - UserLocation, 
    - FavoritesCount, 
    - TotalTweetsCount, 
    - UserFriendCount, 
    - UserFollowersCount, 
    - TimeZone, 
    - UTCOffset Value, 
    - GeoEnabled, 
    - IfUserVerified, 
    - IfContributors, 
    - TweetSource, 
    - coordinates, 
    - SentimentPolarity, 
    - SentimentSubjectivity

Here we are using SQLite3 database to export these details. 

3. Sentimental Analysis: We are using module 'Textblob' to do sentimental analysis. In this module, sentimental value is further categorized into two sub-parts SentimentPolarity and SentimentSubjectivity. The value of SentimentPolarity range from -1 to +1.
    -1 indicates sentiments of give text is Negative
    +1 indicates sentiments of give text is Positive
     0 indicates sentiments of give text is Neutral

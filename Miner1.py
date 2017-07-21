from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
import sqlite3
import sys
from textblob import TextBlob

# auth
ckey="5tokDdzZ31AVXfEtqG462r9lH"
csecret="1VJo6eekVEq57iyFLK3HXkMAUPUrc0wXC46R113vSbUy0bLEm0"
atoken="843762251135901696-pmCo7hG1lr6eVkWQdznSV1OiJlKh7TF"
asecret="ncaDmeCAwEk2cYSaCR2Usz4eCQgapbAmgPHlUo6FRpIQT"

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = API(auth)

class StdOutListener(StreamListener):
    def on_status(self, status):

        # establish db
        conn = sqlite3.connect("MyDBName.sqlite3")  # db created if no MyDBName.sqlite3 found.
        c = conn.cursor()

        # create db table for data.
        c.execute("CREATE TABLE IF NOT EXISTS twitter(ID INTEGER PRIMARY KEY AUTOINCREMENT, created_at DATETIME, screen_name TEXT, lang TEXT, text TEXT, UserProfileName TEXT, UserDescription TEXT, UserLocation TEXT, FavoritesCount INTEGER, TotalTweetsCount INTEGER, UserFriendCount INTEGER, UserFollowersCount INTEGER, TimeZone TEXT, UTCOffset TEXT, GeoEnabled TEXT, IfUserVerified TEXT, IfContributors TEXT, TweetSource TEXT, coordinates TEXT, SentimentPolarity TEXT, SentimentSubjectivity TEXT)")

        tweet = status.text
        analysis = TextBlob(tweet)


        # write data.
        if status.text.find("RT @") == -1 or status.text.startswith("@"):  # ignore manual RTs.
            print("\n" + status.user.screen_name, tweet.translate(non_bmp_map), analysis.sentiment) #We are using "translate(non_bmp_map)", to avoid encoding issue

            c.execute("INSERT INTO twitter(created_at, screen_name, lang, text, UserProfileName, UserDescription, UserLocation, FavoritesCount, TotalTweetsCount, UserFriendCount, UserFollowersCount, TimeZone, UTCOffset, GeoEnabled, IfUserVerified, IfContributors, TweetSource, coordinates, SentimentPolarity, SentimentSubjectivity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (status.created_at, status.user.screen_name, status.lang, status.text, status.user.name, status.user.description, status.user.location, status.user.favourites_count, status.user.statuses_count, status.user.friends_count, status.user.followers_count, status.user.time_zone, status.user.utc_offset, status.user.geo_enabled, status.user.verified, status.contributors, status.source, str(status.geo), analysis.sentiment.polarity, analysis.sentiment.subjectivity))

            conn.commit()  # save to db.


    def on_error(self, status_code):
        # https://dev.twitter.com/overview/api/response-codes
        print("Error: " + str(status_code))
        return True

    def on_timeout(self):
        print("Timeout Tweepy on_timeout")
        return True


if __name__ == "__main__":
    stream = Stream(auth, StdOutListener())
    stream.filter(track=["India"], async=True)

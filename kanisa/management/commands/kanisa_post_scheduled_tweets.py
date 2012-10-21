import time
from django.core.management.base import BaseCommand
from kanisa.models import ScheduledTweet
from kanisa.utils.social import post_to_twitter, TwitterException


class Command(BaseCommand):
    help = 'Posts any scheduled tweets that are due for posting'

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        tweets = ScheduledTweet.future_objects.all()

        successful_tweets = 0

        for tweet in tweets:
            if successful_tweets > 0:
                # Don't post things too close together
                time.sleep(60)

            if self.verbosity >= 2:
                print "Posting tweet: '%s'" % tweet
            try:
                post_to_twitter(tweet.tweet)
                tweet.posted = True
                tweet.save()
                successful_tweets += 1
            except TwitterException, e:
                print e

        if self.verbosity >= 1:
            if len(tweets) == 1:
                object = "tweet"
            else:
                object = "tweets"

            print ("Posted %d %s (of which %d were successfully posted)."
                   % (len(tweets), object, successful_tweets))

class Tweet(object):
    def __init__(self, tweet_id, text):
        self.id_num = tweet_id
        self.text = text

    def __repr__(self):
        return str(self.id_num) + ': ' + self.text

    def __hash__(self):
        return hash(self.id_num)

    def __eq__(self, other_point):
        return self.id_num == other_point.id_num

    def distanceTo(self, tweet_text):
        tweet_1_words = set(self.text.split())
        tweet_2_words = set(tweet_text.split())

        intersection = tweet_1_words.intersection(tweet_2_words)
        union = tweet_1_words.union(tweet_2_words)

        return 1 - (len(intersection) / len(union))

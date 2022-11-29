import tweepy

# Authentification configs

api_key = 'L036EXtxHEj44uNOcegsLv4Hc'
api_key_secret = 'kn7Ts6Y4cGpJIowjRgsdeKdnz8RNY9WL3UYR4StlklYlnlgliR'
access_token = '1504422280847364099-R2WpUd76MFeUtfzcz5Z3FCFHfLPDpO'
access_token_secret = 'PkYeuxI4shJnBVEf76jBiPLdMksPS1Epx6tJyAZMOfzth'

# authentification

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

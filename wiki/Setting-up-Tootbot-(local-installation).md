This guide will help you get Tootbot running locally on your own computer or server. You will need to run some commands on your computer's terminal or command line. On Mac, you can do this from the 'Terminal' app. On Windows, type 'cmd' in the Start Menu search, and click on 'Command Prompt'.

## Applying for a Twitter developer account

Due to Twitter's recent [changes to API access](https://blog.twitter.com/developer/en_us/topics/tools/2018/new-developer-requirements-to-protect-our-platform.html), you now have to apply for a developer account. This doesn't take much effort on your part, but you will have to wait a day or two to be accepted. This step is not necessary if you only want to post to Mastodon.

1. [Sign in](https://twitter.com/login) with the Twitter account you want to use with the bot.
2. Once logged in, go [apply for a developer account](https://developer.twitter.com/en/apply/user).
3. When asked "Who are you requesting access for?", click the checkbox for "I am requesting access for my own personal use".
4. Twitter will ask you to explain how you will use the APIs. Type something like this:

```
1. I'm using Twitter's APIs to repost images from reddit.com to Twitter.
2. I am not analyzing any tweets.
3. I will be occasionally posting images to Twitter. The tool using the API will not interact with users in any way.
4. No Twitter content will be displayed.
```

Once you submit your application, you have to wait for approval from Twitter. You should receive an email in the next day or two. Continue on with this guide once you receive approval.


## Downloading Tootbot

If you haven't already, download Tootbot to your computer. You can grab the latest .zip or .tar.gz file from the [releases page](https://github.com/corbindavenport/tootbot/releases). Unzip the files to somewhere on your computer, like a 'Twitter Bot' folder in your documents folder. Tootbot.py, getmedia.py, and config.ini should all be in the same folder.

## Installing dependencies

Next, you will need to install Python 3.6, which is available on [the official Python website](https://www.python.org/downloads/). Due to [an issue with Tootbot's dependencies](https://github.com/corbindavenport/tootbot/issues/59#issuecomment-406107558), Python 3.7 and above does not work right now. **During the installation, make sure you check the box that says 'Add Python to PATH', if there is one.**

Next, you have to install the libraries that Tootbot needs. Open the command line/terminal and set your directory to the Tootbot folder. Then type this command:

    pip3 install -r requirements.txt

If you get an error, try using `pip` instead of `pip3`.

## Using the config file

All settings for the bot can be found in the `config.ini` file. Open the file in any text editor and perform the following tasks:

1. Under the `[BotSettings]` section, add the name of the subreddit to `SubredditToMonitor` (do not include the /r/). You can also set multiple subreddits using the `+` symbol (example: `AnimalsBeingBros+babyelephantgifs+aww`).
2. By default, the bot will wait at least 600 seconds between tweets to prevent spamming. You can change this by editing the `DelayBetweenTweets` setting in the `[BotSettings]` section.
3. By default, the bot will only look at the top 10 'hot' posts in a subreddit. You can change this by editing the `PostLimit` setting in the `[BotSettings]` section.
4. You can enable or disable NSFW posts and self-posts, by changing `NSFWPostsAllowed` and `SelfPostsAllowed` to true or false.
5. If you want Tootbot to only post media (images, GIFs, GIFV files, etc), set `MediaPostsOnly` to `true`.

By default, Tootbot will only post to Twitter. If you want to post to Mastodon, add the name of your instance (e.g. mastodon.social) to `InstanceDomain` in the `[Mastodon]` section. If you want to disable Twitter posting, set `PostToTwitter` in the `[Twitter]` section to `false`.

## Entering API information

Next, you need to run Tootbot to setup API access with Reddit, Imgur, and whichever social media platforms you have enabled (Twiter and/or Mastodon). Here's an explanation for what each service is used for:

* The Reddit API is used to grab posts from subreddits.
* The Imgur API is used to grab direct image URLs from gallery/album links.
* Twitter and/or Mastodon API access is required for posting to social media.

Open the command line/terminal and set your directory to the Tootbot folder. Then type this command:

```
python tootbot.py
```

After Tootbot starts up, it will begin asking for API keys. You only have to do this process once.

### Setting up Reddit API access

1. Log into Reddit, go to your [app preferences](https://www.reddit.com/prefs/apps), and click the 'Create a new application' button at the bottom.
2. Select 'script' as the application type, and click the 'Create app' button.
3. You should see a Reddit agent string (underneath 'personal use script') and an agent secret. Paste these into Tootbot when it asks for them, pressing Enter after each one.

![Reddit API keys](https://i.imgur.com/z6HSpVQ.png)

If you ever want to re-setup Reddit access (if you make a new account, for example), just delete the `reddit.secret` file and run Tootbot again.

### Setting up Imgur API access

1. Sign into [Imgur](https://imgur.com/) with your account, or make one if you haven't already.
2. Register an application [here](https://api.imgur.com/oauth2/addclient) and choose 'OAuth 2 authorization without a callback URL' as the app type.
3. Imgur will give you a Client ID and Client Secret. Paste these into Tootbot when it asks for them, pressing Enter after each one.

If you ever want to re-setup Imgur access (if you make a new account, for example), just delete the `imgur.secret` file and run Tootbot again.

### Setting up Twitter API access (if Twitter posting is enabled)

1. Go to the [application dashboard](https://developer.twitter.com/en/apps) and click the 'Crete an app' button.
2. Fill out the required text boxes and click 'Create' at the bottom.
3. Click the 'Permissions' tab, and make sure the Access permission says 'Read and write'
4. Click the 'Keys and tokens' tab, and click the 'Create' button underneath 'Access token & access token secret'.

Now that you have all the API keys, you need to save them in Heroku.

1. Go to the [Heroku dashboard](https://dashboard.heroku.com/apps) and click on the Tootbot app you just made.
2. Click the Settings tab, and click the `Reveal Config Vars` button. At the bottom of the variables list are two blank boxes, one for `KEY` and one for `VALUE`.
3. Paste `TWITTER_ACCESS_TOKEN` in the `KEY` box, then paste the Twitter Access Token you just got in the `VALUE` box. Then click the `Add` button.
4. Paste `TWITTER_ACCESS_TOKEN_SECRET` in the `KEY` box, then paste the Twitter Access Token Secret you just got in the `VALUE` box. Then click the `Add` button.
5. Paste `TWITTER_CONSUMER_KEY` in the `KEY` box, then paste the Twitter Consumer Key you just got in the `VALUE` box. Then click the `Add` button.
5. Paste `TWITTER_CONSUMER_SECRET` in the `KEY` box, then paste the Twitter Consumer Secret you just got in the `VALUE` box. Then click the `Add` button.

If you ever want to re-setup Twitter access (if you switch to a new account, for example), just delete the `twitter.secret` file and run Tootbot again.

### Setting up Mastodon API access (if Mastodon posting is enabled)

Just enter the email and password for the Mastodon account you want to use, when Tootbot asks for it. Your login data is only used to generate API keys, it is not stored in any way.

If you ever want to re-setup Mastodon access (if you make a new account, for example), just delete the `mastodon.secret` file and run Tootbot again.

## Running Tootbot

Now that you have everything set up, Tootbot should start posting to Twitter and/or Mastodon. For detailed instructions on  running Tootbot, including automatically running the script when your computer turns on, see [this page](https://github.com/corbindavenport/tootbot/wiki/Running-Tootbot).

Once you're done making a bot account with Tootbot, please add it to [the list of accounts using Tootbot](https://github.com/corbindavenport/tootbot/wiki/Accounts-using-Tootbot)! Also make sure to subscribe to the Tootbot updates feed [via email](https://feedburner.google.com/fb/a/mailverify?uri=tootbot) or [with an RSS reader](http://feeds.feedburner.com/tootbot), so you'll be notified when a new version is available.
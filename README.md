# 31113
Main repository for 31113

## Usage
1. Create a file named `secret.py` inside the `bot` folder.
1. Define your discord bot token as `TOKEN`, saucenao api token as `SAUCE_TOKEN`, reddit data as `REDDIT_ID` and `REDDIT_SECRET` respectively. Follow [these steps](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to obtain the required reddit data.
    ### Example
    ```py
    TOKEN = "discordbottokenhere"
    # Leave the strings below empty as "" if you don't plan on using them
    SAUCE_TOKEN = "saucenaoapitokenhere"
    REDDIT_ID = "redditappidhere"
    REDDIT_SECRET = "redditappsecrethere"
    ```
1. Run the bot with
    ```bash
    python -O -m bot
    # Windows users may need to run this instead
    py -O -m bot
    ```

End User Documentation is available [here](https://femboy.my/31113)

<a href="https://www.digitalocean.com/?refcode=0f3434ca0483&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"><p align="center"><img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg" alt="DigitalOcean Referral Badge" /></p></a>
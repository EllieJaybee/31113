# 31113
Main repository for 31113

## Usage

1. Create `secret.py` inside the `bot` folder.
2. Define your tokens and IDs in `secret.py`:
    - `TOKEN` for Discord bot token
    - `SAUCE_TOKEN` for SauceNao API token
    - `REDDIT_ID` and `REDDIT_SECRET` for Reddit data (follow [these steps](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to obtain them)
    - `GELBOORU_KEY` and `GELBOORU_ID` for Gelbooru

    ### Example
    ```python
    TOKEN = "discordbottokenhere"
    # Leave the strings below empty as "" if you don't plan on using them
    SAUCE_TOKEN = "saucenaoapitokenhere"
    REDDIT_ID = "redditappidhere"
    REDDIT_SECRET = "redditappsecrethere"
    GELBOORU_KEY = "gelboorukeyhere"
    GELBOORU_ID = "gelbooruidhere"
    ```

3. Run the bot with:
    ```bash
    python -O -m bot
    # Windows users may need to run this instead
    py -O -m bot
    ```

## Documentation

End User Documentation is available [here](https://femboy.my/31113)

<p align="center">
    <a href="https://www.digitalocean.com/?refcode=0f3434ca0483&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge">
        <img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg" alt="DigitalOcean Referral Badge" />
    </a>
</p>
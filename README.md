# ShortLinkBot
## How to install

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip3 install --upgrade pip`

`pip3 install -r requirements.txt`

## Start

`Before start, you need to create file settings.py which contains `

`import os`

`_config = {
    'TOKEN': "your bot token", 
    'DATABASE': "your database name"
}`

`config = _config`

`python3 bot.py`

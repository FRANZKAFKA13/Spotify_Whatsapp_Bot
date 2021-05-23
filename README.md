# Spotify Whatsapp Bot

## Deployment: Spotify API Script

- Clone repository
- Create [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements.txt with pip
- Create application on the [Spotify developer dashboard](https://developer.spotify.com/dashboard/)
- For authentication with the Spotify application, the [client credentials flow](https://spotipy.readthedocs.io/en/2.18.0/#client-credentials-flow) is applied
    - Requires setting up environment variables in your virtual environment (see [code snippet](https://github.com/FRANZKAFKA13/Spotify_Whatsapp_Bot/blob/main/resources/activate))
- If you use Jupyter Notebook, make sure it runs on the virtual environment you set up 
- Run [run.py](scripts/run.py) ( cd scripts ; python run.py )


## [WIP] Deployment and Configuration: Chatbot

- Extensive [documentation](https://rasa.com/docs/rasa/) available for [Rasa](https://rasa.com/)
- Most relevant files:
    - Set up intent data for NLU in [nlu.yml](bot/data/nlu.yml) 
    - Change behavior through [rules.yml](bot/data/rules.yml) and [stories.yml](bot/data/stories.yml)
    - Make sure your bot's [domain.yml](bot/domain.yml) contains everything you defined 
    - Write custom code for actions in [actions.py](bot/actions/actions.py)
- Bot training:
    - Whenever one of the above files was changed, train bot: ( cd bot ; rasa train )
- Interaction with bot through CLI:
    - Run bot from root directory: ( cd bot ; rasa shell)
    - Run action server from root directory: ( cd bot ; rasa run actions )
- Requirements:
    - DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS venv/lib/python3.8/site-packages/rasa/core/channels/console.py needs to be increased to 60 to avoid timeouts when data is being pulled


## [WIP] Configuration: Database
- The bot uses a [SQLite](https://docs.python.org/3/library/sqlite3.html) database
- Change database schema:
    - The database is created through the function create_initial_db in [database_access.py](bot/actions/functions/database_access.py) where the schema is defined

- Accessing [Google BigQuery Tutorial](https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-python)

## Built With

- [Python](https://www.python.org/) - Main programming language used
- [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/#installation) - Used for connecting to the Spotify API
- [Rasa](https://rasa.com/) - A simple and powerful framework for conversational agents
- [pandas](https://pandas.pydata.org/) - Used for data transformations
- [starship](https://starship.rs) - Customize shell


## Authors

- Hier Nimmt Member Placeholder
- Hier Nimmt Member Placeholder
- Hier Nimmt Member Placeholder
- [**Carsten Granig**](https://www.linkedin.com/in/carsten-granig/)




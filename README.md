# Spotify Whatsapp Bot

## Deployment Spotify API Script

- Clone repository
- Create [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements.txt with pip
- Create application on the [Spotify developer dashboard](https://developer.spotify.com/dashboard/)
- For authentication with the Spotify application, the [client credentials flow](https://spotipy.readthedocs.io/en/2.18.0/#client-credentials-flow) is applied
    - Requires setting up environment variables in your virtual environment (see [code snippet](https://github.com/FRANZKAFKA13/Spotify_Whatsapp_Bot/blob/main/resources/activate))
- If you use Jupyter Notebook, make sure it runs on the virtual environment you set up 
- Run "run.py" from "/scripts" folder from console (e.g. "python run.py")


## [WIP] Deployment Chatbot

- Will probably be built with [Rasa](https://rasa.com/) or [MS Bot Framework](https://dev.botframework.com/)

# Requirements
- DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS venv/lib/python3.8/site-packages/rasa/core/channels/console.py needs to be increased to 60 to avoid timeouts when data is being pulled

## Built With

- [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/#installation) - Used for connecting to the Spotify API
- [pandas](https://pandas.pydata.org/) - Used for data transformations


## Authors

- Hier Nimmt Member Placeholder
- Hier Nimmt Member Placeholder
- Hier Nimmt Member Placeholder
- [**Carsten Granig**](https://www.linkedin.com/in/carsten-granig/)




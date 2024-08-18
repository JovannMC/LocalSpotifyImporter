# LocalSpotifyImporter

This is a very quick project (made in Python) that helps you import songs from a local directory into a Spotify playlist of your choosing. Could be useful for people migrating from a local song library over to Spotify.

This requires you to create an application via Spotify's [developer dashboard](https://developer.spotify.com/dashboard/create) and place the correct details in a `config.json` - refer to `config.json.example` and the "How to use" section.

## How to use

- Open a text editor (or duplicate the `config.json.example` as `config.json`) to note the details you will need for this to work
- Create an application through Spotify's [developer dashboard](https://developer.spotify.com/dashboard/create) with any details you want
  - Add `http://localhost:8888/callback` to the "Redirect URIs" setting
  - (Optional) Select "Web API" under `"Which API/SDKs are you planning to use?"
- Once the app is created, click "Settings" and copy the "Client ID" and "Client Secret" (click on "View client secret")
- Open your Spotify's [Account](https://www.spotify.com/account/overview/) settings, click "Edit profile", and copy "Username"
- Open the Spotify playlist you want to import the songs to and copy its playlist ID
  - It is found at the end of the playlist URL: `https://open.spotify.com/playlist/PLAYLIST_ID_HERE`
- Configure your `config.json` with the details you've noted (refer to `config.json.example` for format)
- Open a terminal and install the dependencies with `pip install -r requirements.txt`
- Finally, run the script and provide the directory you want to import songs from (e.g. `python3 importer.py`)

## License

This package is licensed under the [MIT](https://opensource.org/license/mit/) License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Spotipy](https://github.com/spotipy-dev/spotipy)
- [Mutagen](https://github.com/quodlibet/mutagen)

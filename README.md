# The Rare Jackal

Studio website: https://rarejackal.com

To add a game: add an entry to `_build/games.py`, put its card art in `assets/` and screenshots in `assets/games/<slug>/`, then run `python _build/build.py` and push. Gallery images can be regenerated with `python _build/images.py`.

To feature an app or tool on the homepage, add its name, description, type, icon, platform, and development status (plus an optional public URL and link label) to `_build/software.py` in display order. Run `python3 _build/build.py` to regenerate the site.

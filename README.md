# Home Dashboard

A digital clock and weather app built with Python for the Raspberry Pi

Check out the [documentation](https://aalcala07.github.io/home_dashboard/) to get started.



## Developer Instructions

These instructions are for anyone wanting to change the source code.

### Initial Environment Setup

1. Clone repository

```
git clone git@github.com:aalcala07/home_dashboard.git
```

2. Create venv from within project directory:

```
python -m venv venv
source venv/bin/activate
```

4. Install packages:

```
pip install -r requirements.txt
```

5. Copy example config

```
cp .env.example .env
```

6. Edit the `.env` file and copy your API key to `OPEN_WEATHER_MAP_API_KEY`
7. Change the `LOCATION_LAT` and `LOCATION_LONG` (go to Google Maps and right click your city or any point on the map to get coordinates)
8. Change the `SCREEN_WIDTH` and `SCREEN_HEIGHT` to match your screen resolution or desired resolution
9. Tweak other config fields as needed

### Starting and Stopping Environment

To start the venv use:

```
source venv/bin/activate
```

To exit the venv use:

```
deactivate
```

### Launching the App

Run the script inside of your project directory (make sure venv is activated):

```
python main.py
```

### Saving Requirements

If you install any new packages using pip, save them to the requirements so they are added when setting up a new environment.

```
pip freeze > requirements.txt

```

### Adding Components

Create a new custom component to display in the app:

1. Create new Python module in `components` directory
2. Register the component in the `templates.json` file

All components must have a `draw` function with `screen`, `rect` and `props` arguments. Check out the existing components for examples.

You can add a component to an existing row's columns in the `template.json` or create a new row.

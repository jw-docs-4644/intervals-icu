# intervals-icu

This python script can be used to push workout data to intervals.icu through their api. Plan your intervals in a spreadsheet, save to csv, and send it to Intervals. 

# Pre-requisites

- Python installed
- Basic knowledge of python
- An account with [intervals.icu](https://intervals.icu)
  - user id
  - api key

# Getting info from Intervals.icu

You can find your user id and api key in the Settings page:

1. Scroll down to Developer Settings.
2. Grab your AthleteID.
3. Click under` API key` to generate and copy your API key. 

# Using this Script

## Set up your .env file.

In the root folder for the project:

1. Create a file called `.env`
2. Paste these lines:
   `
   INTERVALS_API_KEY=[Paste Your API Key]
   INTERVALS_ATHLETE_ID=[Paste your Athlete ID]
   `

## Plan your workout in CSV

Modify the file workouts.csv and replace the workouts that are there with your own workouts. 

### 

The csv file that stores the workouts is kind of picky. Here's a description from Gemini that hopefully catches the nuances of it:

Requirement,Correct Format,Type,Impact
Date,2026-02-14,Required,Places the workout on the correct calendar day.
Name & Type,"Easy Run, Run",Required,Identifies the sport and title for your watch.
The Hyphen (-),- 10km...,Required,"The Trigger: Without a leading hyphen, no bar graph is created."
Target Keyword,...Pace,Required,Forces the watch to use the Pace Gauge instead of HR/Power.
Repeat Syntax,Repeat 2x,Required,"Creates the nested ""skyline"" blocks for intervals/hills."
Double Quotes,"""...""",Required,"Wraps the text so \n or , don't break the file structure."
Step Distance,- 5km...,Required,Required for Intervals.icu to tally your weekly distance.
Broad Ranges,50-90% Pace,Optional,"Prevents the watch from ""beeping"" if you are off-pace."
Step Labels,...Hill Effort,Optional,"Labels the step on your watch screen (e.g., ""Hill Effort"")."
Coaching Notes,Conversational pace,Optional,Extra text for your reference; does not affect the bar graph.

#### Pro-Tip: The "Zero-Space" Rule

For the Hyphen requirement, ensure your CSV row looks like this: ...Run,"- 5km Z2 Pace..." If there is even one space like this: " - 5km", the system will treat it as a plain note and will not show the bar graph.

# Running the Script

Once everything is set up correctly, just start your python venv and run `python upload-plan.py`

If everything in the CSV is correct, your workouts will appear in Intervals. 

# Other Scripts

There are a few other scripts in the project folder: 

| script name   | purpose                                                                                                                                                                                       |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| test-api.py   | run this to make sure your api is set up correctly.                                                                                                                                           |
| debug.py      | run this to send a test workout to intervals and pipe the resulting json file to the clipboad. You an use that json output to troubleshoot your csv file.                                     |
| delete-plan.py | Use this to clear previously synced workouts from intervals.icu. This is helpful when you've been uploading a bunch of stuff and need to start over. Adjust the dated in the script as needed |

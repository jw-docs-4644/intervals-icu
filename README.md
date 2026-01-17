# intervals-icu

# CSV

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

## Pro-Tip: The "Zero-Space" Rule

For the Hyphen requirement, ensure your CSV row looks like this: ...Run,"- 5km Z2 Pace..." If there is even one space like this: " - 5km", the system will treat it as a plain note and will not show the bar graph.

Would you like me to update your Python script with a final "cleanup" line to make sure it automatically strips out any accidental spaces or quotes before uploading?

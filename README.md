# bcstats
Script to gather statistics from Bugcrowd programs

This is a simple script to get all Bugcrowd program's statistics and saving it in a CSV file.
It was created to keep a track of activities happening in all the programs I am participating in.

**Usage**

Install requirements
`pip install -r requirements.txt`

Run `python bugcrowd.py` 

Also supports fetching private program data using the `--session` flag.

Compare 2 different CSVs to see what has changed.

`daff bugcrowd-2018-06-30.csv bugcrowd-2018-06-29.csv`

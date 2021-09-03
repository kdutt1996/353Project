# CMPT 353 - Deducing user reading levels from tweets
## Getting the data
To gather Tweets from specific users, we had three options, scraping data from Twitter directly, leveraging Twitter's API, or searching for third-party collections.
We decided to leverage Twitter's existing developer API to gather tweets, however, this meant we were limited to 3200 tweets per user.

This route also allowed us simplified development as numerous python libraries have been created to interface with the API, abstracting the underlying network requests.
We chose to use `python-twitter` as it is the most up-to-date library and still being actively maintained.

Script `01_get_data.py` uses the `python-twitter` library to gather the last 3200 tweets for a user from `users.csv`. 
The script then outputs the tweets to a `screen_name.csv` file with the header `created_at, text`.

## Calculating reading level
We used a library called `textstat` to calculate the reading level of our twitter candidates. We used the following algorithms:

**Flesch Reading Ease formula** - returns the difficulty of text given. Max score is 121.22

**Flesch-Kincaid Grade Level** - Returns the Flesch-Kincaid Grade of the given text. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

**Automated Readability index** - Returns the ARI (Automated Readability Index) which outputs a number that approximates the grade level needed to comprehend the text.
if the ARI is 6.5, then the grade level to comprehend the text is 6th to 7th grade.

**Coleman-Liau Index** - Returns the grade level of the text using the Coleman-Liau Formula. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

**Dale-Chall Readability Score** - Uses a lookup table of the 3000 most commonly used English words. Returns the grade level of the text given.

_Readability consensus is based upon all the above tests and returns the estimated school grade level required to understand the text._

## Scripts

_Note: Not all of the external libraries referenced in `requirments.txt` are required, but rather the file denotes the environment in which scripts were run_

| # | script | purpose | usage | output | comment |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `01_get_data.py` | Collect user tweets and output them to individual csv files | `python 01_get_data.py <users.csv>` | creates `user_tweets` directory and files | **Can not be run without a new Twitter API Key** |
| 2 | `02_clean_data.py` | Remove artifacts from tweets (emojis, retweets, etc.) | `python 02_clean_data.py` | creates `Cleaned_user_tweets` directory and files | - |
| 3 | `03_combine_data.py` | Consolidate all the collected data into a single pandas data frame | `python 03_combine_data.py <users.csv> <Clean_tweets dir>` | - |**helper library** which should not be run independently |
| 4 | `04_data_analysis.py` | Computes statistical results and plots tweets | `python 04_data_analysis.py <users.csv> <cleaned_tweets dir> <command>` | ttest computations and plots | main entry point to analysis |
| 5 | `05_age_analysis.py` | Computes the correlation of age vs reading level. Performs a linear least-squares regressions and outputs the p-value to indicate a non-zero slope | `python 05_age_analysis.py` | P-values for each test and plots | - |

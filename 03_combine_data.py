import pandas as pd
import sys
import re
import os


def extract_user_from_file(filename):
    regex = r'(Cleaned_)([A-Za-z0-9_]+)(.csv)'
    return re.match(regex, filename).group(2)


def get_tweets(screen_name, user_data, directory):
    file = user_data[user_data['screen_name'] == screen_name]['file']
    tweets = pd.read_csv(os.path.join(directory, *file.values), engine='python')
    tweets['created_at'] = pd.to_datetime(tweets['created_at'])
    return tweets


def collect_data(users_file, *args):
    user_data = pd.read_csv(users_file, engine='python')
    users_file_manifest = {'screen_name': [], 'file': []}
    for f in args:
        users_file_manifest['screen_name'].append(extract_user_from_file(f))
        users_file_manifest['file'].append(f)

    user_file_manifest = pd.DataFrame(users_file_manifest, columns=['screen_name', 'file'])
    user_data = user_data.join(user_file_manifest.set_index('screen_name'), on='screen_name')
    return user_data


if __name__ == '__main__':
    user_data = collect_data(sys.argv[1], *os.listdir(sys.argv[2]))
    print(user_data)
    print(get_tweets('BarackObama', user_data, sys.argv[2]))
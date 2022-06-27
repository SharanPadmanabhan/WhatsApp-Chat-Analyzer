from collections import Counter
from pathlib import Path

import emoji
import pandas
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()


def fetch_statistics(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]
    number_of_messages = dataframe.shape[0]

    words = list()
    links = list()

    for message in dataframe['message']:
        words.extend(message.split())

    number_of_media_messages = dataframe[dataframe['message'] == '<Media omitted>\n'].shape[0]

    for message in dataframe['message']:
        links.extend(extract.find_urls(message))

    return number_of_messages, len(words), number_of_media_messages, len(links)


def most_busy_users(dataframe):
    user = dataframe['user'].value_counts().head()
    dataframe = round((dataframe['user'].value_counts() / dataframe.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return user, dataframe


def create_wordcloud(selected_user, dataframe):
    with open(f'{Path(__file__).parent}\\stop_english.txt') as file:
        stop_words = file.read()

    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]

    temporary = dataframe[dataframe['user'] != 'group_notification']
    temporary = temporary[temporary['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return ' '.join(words)

    word_cloud = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temporary['message'] = temporary['message'].apply(remove_stop_words)
    dataframe_of_word_cloud = word_cloud.generate(temporary['message'].str.cat(sep=" "))
    return dataframe_of_word_cloud


def most_common_words(selected_user, dataframe):
    with open(f'{Path(__file__).parent}\\stop_english.txt') as file:
        stop_words = file.read()

    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]

    temporary = dataframe[dataframe['user'] != 'group_notification']
    temporary = temporary[temporary['message'] != '<Media omitted>\n']

    words = list()
    for message in temporary['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_dataframe = pandas.DataFrame(Counter(words).most_common(30))
    return most_common_dataframe


def emoji_helper(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]

    emojis = list()
    for message in dataframe['message']:
        emojis.extend([char for char in message if char in emoji.UNICODE_EMOJI['en']])

    emoji_dataframe = pandas.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_dataframe


def monthly_timeline(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]

    timeline = dataframe.groupby(['year', 'month_number', 'month']).count()['message'].reset_index()

    time = list()
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]
    daily_time_line = dataframe.groupby('only_date').count()['message'].reset_index()
    return daily_time_line


def week_activity_map(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]
    return dataframe['day_name'].value_counts()


def month_activity_map(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]
    return dataframe['month'].value_counts()


def activity_heatmap(selected_user, dataframe):
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['user'] == selected_user]
    user_heatmap = dataframe.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

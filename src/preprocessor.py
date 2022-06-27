import re
import pandas


def preprocess(data: str) -> pandas.DataFrame:
    pattern: str = r'\[?\d{1,2}\/\d{1,2}\/\d{2,4}\,\s\d{1,2}\:\d{1,2}\:?\d{1,2}?\s?[a|A|p|P]?[m|M]?\]?\s?\-?\s'

    messages = re.split(pattern, data)[1:]
    dates = [date.replace('[', '').replace(']', ' -') for date in re.findall(pattern, data)]

    dataframe = pandas.DataFrame({'user_message': messages, 'message_date': dates})

    dataframe['message_date'] = pandas.to_datetime(dataframe['message_date'], format='%d/%m/%Y, %H:%M - ', errors='coerce') \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')) \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%Y, %H:%M:%S %p - ', errors='coerce')) \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%y, %H:%M:%S %p - ', errors='coerce')) \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%Y, %H:%M %p - ', errors='coerce')) \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%y, %H:%M %p - ', errors='coerce')) \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%Y, %H:%M:%S - ', errors='coerce')) \
        .combine_first(pandas.to_datetime(dataframe['message_date'], format='%d/%m/%y, %H:%M:%S - ', errors='coerce'))

    dataframe.rename(columns={'message_date': 'date'}, inplace=True)

    users: list = list()
    messages: list = list()
    for message in dataframe['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(' '.join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    dataframe['user'] = users
    dataframe['message'] = messages
    dataframe.drop(columns=['user_message'], inplace=True)

    dataframe['only_date'] = dataframe['date'].dt.date
    dataframe['year'] = dataframe['date'].dt.year
    dataframe['month_number'] = dataframe['date'].dt.month
    dataframe['month'] = dataframe['date'].dt.month_name()
    dataframe['day'] = dataframe['date'].dt.day
    dataframe['day_name'] = dataframe['date'].dt.day_name()
    dataframe['hour'] = dataframe['date'].dt.hour
    dataframe['minute'] = dataframe['date'].dt.minute

    period = []
    for hour in dataframe[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    dataframe['period'] = period

    return dataframe

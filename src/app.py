from random import random

import streamlit
from streamlit_echarts import st_echarts as streamlit_echarts

import helper
import preprocessor


@streamlit.cache
def load_data_frame(data):
    return preprocessor.preprocess(data)


def plot_line_chart(data, options=None):
    line_chart_options = {
        'xAxis': {
            'type': 'category',
            'data': data['xAxis'],
        },
        'yAxis': {'type': 'value'},
        'tooltip': {'trigger': 'axis'},
        'series': [
            {
                'data': data['yAxis'],
                'lineStyle': {'color': options['lineColor'] if 'lineColor' in options else 'black', 'type': 'solid'},
                'itemStyle': {'color': options['lineColor'] if 'lineColor' in options else 'black'},
                'symbol': 'none',
                'type': 'line'
            }
        ]
    }

    streamlit_echarts(options=line_chart_options, height=options['height'] if 'height' in options else '500px')


def plot_bar_chart(data, options=None):
    bar_chart_options = {
        'xAxis': {
            'type': 'category',
            'data': data['xAxis'],
        },
        'yAxis': {'type': 'value'},
        'tooltip': {'trigger': 'item'},
        'series': [
            {
                'data': data['yAxis'],
                'itemStyle': {'color': options['itemColor'] if 'itemColor' in options else 'black'},
                'type': 'bar'
            }
        ]
    }

    streamlit_echarts(options=bar_chart_options, height=options['height'] if 'height' in options else '500px')


def plot_heat_map(data, options=None):
    heat_map_options = {
        'xAxis': {'type': 'category', 'data': data['xAxis'], 'splitArea': {'show': True}},
        'yAxis': {'type': 'category', 'data': data['yAxis'], 'splitArea': {'show': True}},
        'gradientColor': {0: '#04051a', 1: '#541e4e', 2: '#c41753', 3: '#f4845c', 4: '#fbeee2'},
        'grid': {'height': '50%', 'top': '10%'},
        'tooltip': {'position': 'left'},

        'visualMap': {
            'min': data['min'] if 'min' in data else '0',
            'max': data['max'] if 'max' in data else '100',
            'calculable': False,
            'orient': 'horizontal',
            'left': 'center',
            'bottom': '20%',
        },

        'series': [
            {
                'data': data['data'],
                'name': data['name'],
                'type': 'heatmap',
                'label': {'show': False},
                'emphasis': {
                    'itemStyle': {'shadowBlur': 2.5, 'shadowColor': 'rgba(0, 0, 0, 0.25)'}
                },
            }
        ],
    }

    streamlit_echarts(options=heat_map_options, height=options['height'] if 'height' in options else '500px',
                      width=options['width'] if 'width' in options else '500px')


def plot_pie_chart(data, options=None):
    pie_chart_options = {
        'title': {
            'text': data['title'] if 'title' in data else 'Donut Chart',
            'left': 'center'
        },
        'legend': {'top': '5%', 'left': 'center'},
        'tooltip': {'trigger': 'item'},
        'series': [
            {
                'radius': ['30%', '70%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#ffffff',
                    'borderWidth': 5,
                },
                'label': {'show': False, 'position': 'center'},
                'labelLine': {'show': False},
                'data': data['data'],
                'name': data['name'],
                'emphasis': {
                    'label': {
                        'show': True,
                        'fontSize': '40',
                        'fontWeight': 'bold'
                    }
                },
                'type': 'pie'
            }
        ]
    }

    streamlit_echarts(options=pie_chart_options, height=options['height'] if 'height' in options else '500px')


def plot_word_cloud(data, options=None):
    word_cloud_options = {
        'tooltip': {'trigger': 'item'},
        'series': [
            {
                'type': 'wordCloud',
                'sizeRange': [20, 100],
                'textStyle': {
                    'color': f'rgb({round(random() * 160)}, {round(random() * 160)}, {round(random() * 160)})',
                },
                'data': data['data'],
            }
        ],
        'emphasis': {
            'textStyle': {'shadowBlur': 10, 'shadowColor': 'rgba(0, 0, 0, 0.25)'}
        },
    }

    streamlit_echarts(word_cloud_options, height=options['height'] if 'height' in options else '500px')


def create_side_bar():
    streamlit.sidebar.title('Whatsapp Chat Analyser')
    streamlit.markdown('''
        <style>
            .css-hxt7ib h1 {
                padding: 0;
            }
            .css-hxt7ib h3 {
                padding: 0.5rem 0 1rem 0;
            }
        </style>
    ''', unsafe_allow_html=True)

    streamlit.sidebar.subheader('Version 2.0')
    return streamlit.sidebar.file_uploader('Choose a File')


def display_statistics(selected_user, dataframe):
    statistics_container = streamlit.container()
    with statistics_container:
        statistics_container.markdown('# Top Statistics')

        number_of_messages, number_of_words, number_of_media_messages, number_of_links = helper.fetch_statistics(selected_user, dataframe)
        total_messages_column, total_words_column, total_media_column, total_links_column = statistics_container.columns(4)

        with total_messages_column:
            streamlit.markdown('## Total Messages')
            streamlit.markdown(f'### {number_of_messages}')

        with total_words_column:
            streamlit.markdown('## Total Words')
            streamlit.markdown(f'### {number_of_words}')

        with total_media_column:
            streamlit.markdown('## Media Shared')
            streamlit.markdown(f'### {number_of_media_messages}')

        with total_links_column:
            streamlit.markdown('## Links Shared')
            streamlit.markdown(f'### {number_of_links}')

        streamlit.markdown('<br />', unsafe_allow_html=True)

        monthly_timeline_column, daily_timeline_column = statistics_container.columns(2)

        with monthly_timeline_column:
            streamlit.markdown('# Monthly Timeline')
            timeline = helper.monthly_timeline(selected_user, dataframe)

            plot_line_chart(data={'xAxis': [str(timeline['time'][i]) for i in range(len(timeline['time']))],
                                  'yAxis': [int(timeline['message'][i]) for i in range(len(timeline['message']))]},
                            options={'height': '500px', 'lineColor': '#32a852'})

        with daily_timeline_column:
            streamlit.markdown('# Daily Timeline')
            timeline = helper.daily_timeline(selected_user, dataframe)

            plot_line_chart(data={'xAxis': [str(timeline['only_date'][i]) for i in range(len(timeline['only_date']))],
                                  'yAxis': [int(timeline['message'][i]) for i in range(len(timeline['message']))]},
                            options={'height': '500px', 'lineColor': '#181818'})


def display_activity(selected_user, dataframe):
    activity_container = streamlit.container()
    with activity_container:
        activity_container.markdown('# Activity Map')
        most_busy_day_column, most_busy_month_column, most_busy_week_column = activity_container.columns(3)

        with most_busy_day_column:
            streamlit.markdown('## Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, dataframe)

            plot_bar_chart(data={'xAxis': [str(day) for day in busy_day.index],
                                 'yAxis': [int(value) for value in busy_day.values]},
                           options={'height': '500px', 'itemColor': '#843299'})

        with most_busy_month_column:
            streamlit.markdown('## Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, dataframe)

            plot_bar_chart(data={'xAxis': [str(month) for month in busy_month.index],
                                 'yAxis': [int(value) for value in busy_month.values]},
                           options={'height': '500px', 'itemColor': '#d98c1a'})

        with most_busy_week_column:
            streamlit.markdown('## Weekly Activity Map')
            streamlit.markdown('<br />', unsafe_allow_html=True)

            user_heatmap = helper.activity_heatmap(selected_user, dataframe)

            values: list = user_heatmap.to_numpy()
            data: list = [[(i, j, values[i][j]) for j in range(len(values[i]))] for i in range(len(values))]

            plot_heat_map(data={'xAxis': [str(value) for value in user_heatmap.head()],
                                'yAxis': [str(value)[:3] for value in user_heatmap.index],
                                'data': [[d[1], d[0], d[2]] for i in range(len(data)) for d in data[i]],
                                'name': 'Weekly Activity', 'max': max(map(max, values)), 'min': min(map(min, values))},
                          options={'height': '500px', 'width': '95%'})

        if selected_user == 'Overall':
            streamlit.markdown('## Most Busy Users')
            x, new_dataframe = helper.most_busy_users(dataframe)
            plot_bar_chart(data={'xAxis': [str(month) for month in x.index],
                                 'yAxis': [int(value) for value in x.values]},
                           options={'height': '500px', 'itemColor': '#fa4343'})


def display_word_analysis(selected_user, dataframe):
    word_analysis_container = streamlit.container()
    with word_analysis_container:
        emoji_dataframe_column, emoji_chart_column = word_analysis_container.columns(2)

        with emoji_dataframe_column:
            streamlit.markdown('# Word Cloud')
            dataframe_word_cloud = helper.create_wordcloud(selected_user, dataframe)
            streamlit.write('<style>.css-1kyxreq.etr89bj2 { display: grid; place-items: center; }</style>', unsafe_allow_html=True)
            streamlit.image(dataframe_word_cloud.to_image(), clamp=True)

        with emoji_chart_column:
            streamlit.markdown('# Most common words')
            most_common_dataframe = helper.most_common_words(selected_user, dataframe)
            plot_bar_chart(data={'xAxis': [str(month) for month in most_common_dataframe[0]],
                                 'yAxis': [int(value) for value in most_common_dataframe[1]]},
                           options={'height': '500px', 'itemColor': '#05a8ed'})


def display_emoji_analysis(selected_user, dataframe):
    emoji_container = streamlit.container()
    with emoji_container:
        emoji_container.markdown('# Emoji Analysis')
        emoji_dataframe = helper.emoji_helper(selected_user, dataframe)
        emoji_dataframe_column, emoji_chart_column = emoji_container.columns(2)

        with emoji_dataframe_column:
            emoji_dataframe.rename(columns={0: 'Emoji', 1: 'Count'}, inplace=True)
            streamlit.table(emoji_dataframe.head(n=15))

        with emoji_chart_column:
            plot_pie_chart(data={'data': [{'value': value, 'name': label} for (value, label) in
                                          zip(emoji_dataframe['Count'].head(), emoji_dataframe['Emoji'].head())],
                                 'title': 'Emoji Analysis', 'name': 'Emoji'},
                           options={'height': '600px'})


def create_page():
    uploaded_file = create_side_bar()

    if uploaded_file is not None:
        bytes_of_data = uploaded_file.getvalue()
        data = bytes_of_data.decode('utf-8')

        dataframe = load_data_frame(data)
        user_list = dataframe['user'].unique().tolist()

        if 'group_notification' in user_list:
            user_list.remove('group_notification')

        user_list.sort()
        user_list.insert(0, 'Overall')

        selected_user = streamlit.sidebar.selectbox('Show analysis of', user_list)

        if streamlit.sidebar.button('Show Analysis'):
            display_statistics(selected_user, dataframe)
            display_activity(selected_user, dataframe)
            display_word_analysis(selected_user, dataframe)
            display_emoji_analysis(selected_user, dataframe)

        else:
            streamlit.markdown('# WhatsApp Chat Analyser')

    else:
        streamlit.markdown('# WhatsApp Chat Analyser')


def init():
    # Set page Configuration
    page_config_options = {
        'page_title': 'WhatsApp Chat Analyser',
        'layout': 'wide', 'initial_sidebar_state': 'auto'
    }
    streamlit.set_page_config(**page_config_options)

    # Hide Streamlit default style.
    hide_st_style = '''
        <style>
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
            header { visibility: hidden; }
        </style>
    '''
    streamlit.markdown(hide_st_style, unsafe_allow_html=True)

    create_page()


if __name__ == '__main__':
    init()

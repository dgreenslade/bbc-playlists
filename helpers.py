from bs4 import BeautifulSoup
from datetime import date, timedelta
import requests
import re


def get_date_list(start_date, end_date):
    """
    Return list of dates bewteen two input dates.  Input dates must be date objects
    """
    daterange = end_date - start_date
    daterange_list = []

    for i in range(daterange.days + 1):
        date = start_date + timedelta(days=i)
        date_str = date.strftime('%Y/%m/%d')
        daterange_list.append(date_str)

    return daterange_list


def bbc_daily_schedule_urls(base_url, list_of_dates):
    """
    Return list of BBC radio daily schedule URLs by day.

    base_url : str
    list_of_dates: list of date objects
    """

    url_list = []
    for date in list_of_dates:
        url = base_url + date
        url_list.append(url)

    return url_list


def bbc_program_urls(date_url):
    """
    Scrape BBC Radio schedule URL on specific date
    to find links to each individual program on the day
    """
    program_urls = []

    html_data = requests.get(date_url)
    html_bs = BeautifulSoup(html_data.content, 'html.parser')
    divs = html_bs.find_all('h4', attrs={'class': 'programme__titles'})
    for x in divs:
        href = x.find('a')['href']
        program_urls.append(href)

    return program_urls


def get_playlist(program_url):
    """
    Take BBC Program schedule URL and return a Python dict with Program Tile, Host and List of Tracks
    """
    print('Accessing data from {}'.format(program_url))

    html_data = requests.get(program_url)
    html_bs = BeautifulSoup(html_data.content, 'html.parser')

    # Program Timestamp
    prog_timestamp = html_bs.find_all('div', attrs={'class': 'broadcast-event__time beta'})[0]['content']
    # Program Host
    prog_host = html_bs.find_all('div', attrs={'class': 'br-masthead__title'})[0].text.strip()
    # Program Title
    prog_title = html_bs.find_all('h1')[0].text.strip()

    playlist = None
    tracks = []

    # All segment__track divs
    div_list = html_bs.find_all('div', attrs={'class': 'segment__track'})

    # compile regex for whitespace stripping
    regex = re.compile(r'\s+')

    for div in div_list:

        # Artist in <h3>
        headers = div.find_all('h3')
        for header in headers:
            track_artist = re.sub(regex, ' ', header.text.strip())

            # Song title in <p>
            for para in div.find_all('p'):
                track_title = re.sub(regex, ' ', para.text.strip())

                song = (track_artist, track_title)
                tracks.append(song)

    playlist = {
        'timestamp': prog_timestamp,
        'url': program_url,
        'host': prog_host,
        'prog_title': prog_title,
        'tracks': tracks
    }

    return playlist

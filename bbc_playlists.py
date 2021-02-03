import conf
import helpers

# Configuration parameters pulled from conf.py
bbc_radio6_url = conf.config('bbc_show_url')
start_date = conf.config('start_date')
end_date = conf.config('end_date')


def main():
    """
    Workflow function to print a list of all playlists within a date range.

    In development, need to change output to otuput to MongoDB.

    """

    print("Retreiving BBC playlists for dates between {} and {}".
          format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

    # Get daily schedule URLs within date range
    radio6_schedule_list = helpers.bbc_daily_schedule_urls(bbc_radio6_url, helpers.get_date_list(start_date, end_date))

    # Get all show URLS
    all_program_urls = []
    for url in radio6_schedule_list:
        all_program_urls += helpers.bbc_program_urls(url)

    # Get all track playlists from program URLs
    track_lists = []
    for url in all_program_urls:
        program_playlist = helpers.get_playlist(url)
        track_lists.append(program_playlist)

    print(track_lists)
    return track_lists


if __name__ == "__main__":
    main()



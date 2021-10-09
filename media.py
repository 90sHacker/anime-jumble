import webbrowser

class Anime():
    def __init__(self, title, ep_length, storyline, episodes, date,
                 rating, youtube_url, poster_image):
        
        self.title = title
        self.duration = ep_length
        self.storyline = storyline
        self.episodes = episodes
        self.air_date = date
        self.rating = rating
        self.trailer_youtube_url = youtube_url
        self.poster_image_url = poster_image

    def show_trailer(self):
        webbrowser.open(self.trailer)

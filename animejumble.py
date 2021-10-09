import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>AnimeJumble</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 10px;
            padding-top: 10px;
        }

        .tile-size {
            max-width: 100%;
            height: 340px;
            box-shadow: 0 0 13px #000;
        }

        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>

    <style type="text/css" media="screen">
      html, body {
				box-sizing: border-box;
			}
			
			.header {
				width: 100%;
        display: inline-block;
        background-image: linear-gradient(110deg, rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url("https://images.unsplash.com/photo-1613376023733-0a73315d9b06?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=870&q=80");
				background-size: contain;
        background-repeat: repeat;
				min-height: 180px;
			}
			
			.header-text {
				color: white;
        font-size: 1.2em;
			}

      .category {
        position: relative;
        top: -10px;
        text-align: left;
        padding-left: 10px;
        font-size: 1.3em;
      }

      h3 {
        font-size: 12px;
        font-weight: 600;
      }
    </style>

    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <header class="header header-text">
			<nav id="drawer" class="navbar">
				<div class="container-fluid">
					<div class="navbar-header">
						<a class="navbar-brand header-text" href="#">AnimeJumble</a>
					</div>
					<div>
						<ul class="nav navbar-nav">
						<li class="nav-item"> <a href="#" class="header-text">Home</a>
						<li class="nav-item"> <a href="#" class="header-text">Latest</a>
						<li class="nav-item"> <a href="#" class="header-text">Genres</a>
						<li class="nav-item"> <a href="#" class="header-text">Discussion</a>
						</ul>
					</div>
				</div>
			</nav>
      <article class="text-center">
        <h1>Watch Anime Trailers</h1>
      </article>
		</header>

    <section class="container-fluid">
      <h2 class="category">Top Shows</h2>
      <div class="container">
            {movie_tiles}
      </div>
    </section>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-sm-12 col-md-4 col-lg-3 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" alt="{alt_text}" class="tile-size img-thumbnail">
    <h3>{movie_title}</h3>
</div>
'''


def create_movie_tiles_content(animes):
    # The HTML content for this section of the page
    content = ''
    for anime in animes:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', anime.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', anime.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=anime.title,
            poster_image_url=anime.poster_image_url,
            alt_text = anime.title,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(animes):
    # Create or overwrite the output file
    output_file = open('index.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(animes))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)

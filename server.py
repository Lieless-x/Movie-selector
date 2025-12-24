from flask import Flask, jsonify, send_file
from flask_cors import CORS
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Get your free API key from: http://www.omdbapi.com/apikey.aspx
OMDB_API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your OMDb API key

# Database setup
DB_NAME = 'movies.db'

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Movies table
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (id TEXT PRIMARY KEY,
                  title TEXT,
                  year INTEGER,
                  rating REAL,
                  genres TEXT,
                  description TEXT,
                  poster TEXT,
                  imdb_url TEXT,
                  actors TEXT,
                  director TEXT,
                  runtime TEXT,
                  category TEXT,
                  rank INTEGER,
                  last_updated TIMESTAMP)''')
    
    # Watched movies table
    c.execute('''CREATE TABLE IF NOT EXISTS watched
                 (movie_id TEXT PRIMARY KEY,
                  watched_date TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def save_movie_to_db(movie, category):
    """Save or update a movie in the database"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''INSERT OR REPLACE INTO movies 
                 (id, title, year, rating, genres, description, poster, imdb_url, 
                  actors, director, runtime, category, rank, last_updated)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (movie['id'], movie['title'], movie['year'], movie['rating'],
               ','.join(movie['genres']), movie['description'], movie['poster'],
               movie['imdb_url'], movie['actors'], movie['director'],
               movie['runtime'], category, movie['rank'], datetime.now()))
    
    conn.commit()
    conn.close()

def get_movies_from_db(category):
    """Get movies from database by category"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('SELECT * FROM movies WHERE category = ? ORDER BY rank', (category,))
    rows = c.fetchall()
    conn.close()
    
    movies = []
    for row in rows:
        movies.append({
            'id': row[0],
            'title': row[1],
            'year': row[2],
            'rating': row[3],
            'genres': row[4].split(',') if row[4] else [],
            'description': row[5],
            'poster': row[6],
            'imdb_url': row[7],
            'actors': row[8],
            'director': row[9],
            'runtime': row[10],
            'rank': row[12]
        })
    
    return movies

def get_watched_movies():
    """Get list of watched movie IDs"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('SELECT movie_id FROM watched')
    rows = c.fetchall()
    conn.close()
    
    return [row[0] for row in rows]

# IMDB Top 100 movie IDs
TOP_100_IDS = [
    'tt0111161', 'tt0068646', 'tt0468569', 'tt0071562', 'tt0050083',
    'tt0108052', 'tt0167260', 'tt0110912', 'tt0060196', 'tt0120737',
    'tt0137523', 'tt0109830', 'tt0080684', 'tt1375666', 'tt0167261',
    'tt0073486', 'tt0099685', 'tt0133093', 'tt0047478', 'tt0114369',
    'tt0317248', 'tt0076759', 'tt0102926', 'tt0038650', 'tt0120815',
    'tt0245429', 'tt0118799', 'tt0120689', 'tt0816692', 'tt0114814',
    'tt0110413', 'tt0120586', 'tt0034583', 'tt0021749', 'tt0064116',
    'tt0027977', 'tt0253474', 'tt0407887', 'tt0088763', 'tt1675434',
    'tt0103064', 'tt2582802', 'tt0047396', 'tt0082971', 'tt0110357',
    'tt0054215', 'tt0172495', 'tt0110475', 'tt0209144', 'tt0078788',
    'tt0095765', 'tt0032553', 'tt0095327', 'tt0043014', 'tt0405094',
    'tt0057012', 'tt4154756', 'tt0050825', 'tt0081505', 'tt1853728',
    'tt0910970', 'tt0119698', 'tt0051201', 'tt0169547', 'tt0090605',
    'tt0087843', 'tt2380307', 'tt0112573', 'tt0082096', 'tt0056172',
    'tt0180093', 'tt0338013', 'tt0066921', 'tt0056592', 'tt0052357',
    'tt0361748', 'tt0070735', 'tt0053125', 'tt0105236', 'tt0086879',
    'tt5311514', 'tt0022100', 'tt0033467', 'tt0112641', 'tt0086190',
    'tt0045152', 'tt1345836', 'tt0036775', 'tt0075314', 'tt0211915',
    'tt0208092', 'tt0435761', 'tt0086250', 'tt0119217', 'tt0093058',
    'tt0040522', 'tt0114709', 'tt0120735', 'tt0031679', 'tt0113277'
]

# Top movies 2024-2025
TOP_2024_2025_IDS = [
    'tt15398776', # Oppenheimer
    'tt14230458', # Poor Things
    'tt9362722',  # Spider-Man: Across the Spider-Verse
    'tt6710474',  # Everything Everywhere All at Once
    'tt1745960',  # Top Gun: Maverick
    'tt10366206', # John Wick: Chapter 4
    'tt11389872', # The Holdovers
    'tt13238346', # Past Lives
    'tt15789038', # Killers of the Flower Moon
    'tt14444726', # Asteroid City
    'tt14230388', # The Boy and the Heron
    'tt6467266',  # Babylon
    'tt11358390', # Barbie
    'tt0974015',  # The Zone of Interest
    'tt10954600', # Ant-Man and the Wasp: Quantumania
    'tt9114286',  # Dune: Part Two
    'tt13751694', # Godzilla Minus One
    'tt10648342', # Thor: Love and Thunder
    'tt9419884',  # Doctor Strange in the Multiverse of Madness
    'tt1160419',  # Dune
    'tt10872600', # Spider-Man: No Way Home
    'tt10648342', # The Batman
    'tt9376612',  # Shang-Chi and the Legend of the Ten Rings
    'tt9032400',  # Eternals
    'tt6710474',  # The French Dispatch
    'tt7657566',  # Don't Look Up
    'tt11291274', # The Fabelmans
    'tt14539740', # Avatar: The Way of Water
    'tt1630029',  # Black Panther: Wakanda Forever
    'tt10298810', # The Whale
    'tt1649418',  # The Northman
    'tt9620292',  # Everything Everywhere All at Once
    'tt10954984', # Nope
    'tt11198330', # The Banshees of Inisherin
    'tt11138512', # The Menu
    'tt13923084', # All Quiet on the Western Front
    'tt1745960',  # Elvis
    'tt14444726', # Triangle of Sadness
    'tt11703710', # The Woman King
    'tt10160976', # The Northman
    'tt11426232', # Turning Red
    'tt9419884',  # Bullet Train
    'tt1745960',  # Tar
    'tt15255288', # Cocaine Bear
    'tt9764362',  # The Watcher
    'tt13320622', # M3GAN
    'tt12262116', # Scream VI
    'tt11564570', # Glass Onion: A Knives Out Mystery
    'tt13320622', # The Black Phone
    'tt10298810', # The Northman
]

# Genre-specific top movies (50 each)
GENRE_MOVIES = {
    'Action': [
        'tt0468569', 'tt0137523', 'tt0167260', 'tt0167261', 'tt0120737',
        'tt0080684', 'tt0076759', 'tt0120815', 'tt0133093', 'tt0816692',
        'tt1375666', 'tt0245429', 'tt0103064', 'tt0088763', 'tt0172495',
        'tt0120689', 'tt4154756', 'tt0361748', 'tt0482571', 'tt0407887',
        'tt1853728', 'tt0110912', 'tt0253474', 'tt0338013', 'tt2582802',
        'tt0986264', 'tt1345836', 'tt0372784', 'tt0910970', 'tt1392190',
        'tt0477348', 'tt0112573', 'tt0114814', 'tt0119217', 'tt0458339',
        'tt0119488', 'tt0266543', 'tt0377092', 'tt0379786', 'tt0382932',
        'tt0468569', 'tt0473075', 'tt0499549', 'tt0848228', 'tt1228705',
        'tt1568346', 'tt2024544', 'tt2096673', 'tt2267998', 'tt3501632'
    ],
    'Adventure': [
        'tt0167260', 'tt0167261', 'tt0120737', 'tt0076759', 'tt0080684',
        'tt0086190', 'tt0088763', 'tt0095327', 'tt0103064', 'tt0107290',
        'tt0108052', 'tt0110912', 'tt0114709', 'tt0118799', 'tt0119217',
        'tt0120815', 'tt0133093', 'tt0172495', 'tt0245429', 'tt0266697',
        'tt0317705', 'tt0325980', 'tt0338013', 'tt0361748', 'tt0371746',
        'tt0382932', 'tt0399201', 'tt0401792', 'tt0416449', 'tt0449059',
        'tt0468569', 'tt0477348', 'tt0482571', 'tt0499549', 'tt0816692',
        'tt0848228', 'tt0910970', 'tt0993846', 'tt1130884', 'tt1201607',
        'tt1345836', 'tt1375666', 'tt1392190', 'tt1392214', 'tt1853728',
        'tt2024544', 'tt2096673', 'tt2267998', 'tt2380307', 'tt3748528'
    ],
    'Animation': [
        'tt0245429', 'tt0910970', 'tt1049413', 'tt0109830', 'tt0114709',
        'tt0110357', 'tt0347149', 'tt0892769', 'tt0382932', 'tt0120623',
        'tt0126029', 'tt0167260', 'tt0266543', 'tt0317705', 'tt0434409',
        'tt0198781', 'tt0325980', 'tt1049413', 'tt0382932', 'tt0477348',
        'tt0993846', 'tt1049413', 'tt1217209', 'tt1323594', 'tt1453405',
        'tt1570728', 'tt1979320', 'tt2277860', 'tt2948356', 'tt3606756',
        'tt3011894', 'tt4633694', 'tt4881806', 'tt5109280', 'tt6791350',
        'tt7131622', 'tt8097030', 'tt8923482', 'tt9426210', 'tt10298810',
        'tt10872600', 'tt11126994', 'tt13320622', 'tt14537428', 'tt15789038',
        'tt16419074', 'tt0087332', 'tt0095327', 'tt0096283', 'tt0103639'
    ],
    'Comedy': [
        'tt0068646', 'tt0108052', 'tt0110912', 'tt0167260', 'tt0095327',
        'tt0109830', 'tt0816692', 'tt0120815', 'tt0167261', 'tt0102926',
        'tt0071562', 'tt0119217', 'tt0118799', 'tt0120689', 'tt0245429',
        'tt0910970', 'tt0107290', 'tt0107207', 'tt0088763', 'tt0253474',
        'tt0083658', 'tt0087332', 'tt0092005', 'tt0093779', 'tt0095016',
        'tt0097165', 'tt0107048', 'tt0120338', 'tt0120601', 'tt0129167',
        'tt0145487', 'tt0169547', 'tt0172495', 'tt0266697', 'tt0317705',
        'tt0325980', 'tt0338013', 'tt0382932', 'tt0408306', 'tt0449059',
        'tt0477348', 'tt0486655', 'tt0499549', 'tt0765429', 'tt0910970',
        'tt0993846', 'tt1187043', 'tt1245492', 'tt1323594', 'tt1392190'
    ],
    'Crime': [
        'tt0111161', 'tt0068646', 'tt0468569', 'tt0071562', 'tt0050083',
        'tt0108052', 'tt0110912', 'tt0137523', 'tt0099685', 'tt0102926',
        'tt0114369', 'tt0253474', 'tt0407887', 'tt0172495', 'tt0120586',
        'tt0088763', 'tt0054215', 'tt0110357', 'tt0082971', 'tt0078788',
        'tt0114814', 'tt0119488', 'tt0266697', 'tt0317248', 'tt0338013',
        'tt0361748', 'tt0372784', 'tt0477348', 'tt0482571', 'tt0758758',
        'tt0910970', 'tt0993846', 'tt1130884', 'tt1187043', 'tt1201607',
        'tt1210166', 'tt1345836', 'tt1375666', 'tt1392190', 'tt1397280',
        'tt1430132', 'tt1454029', 'tt1535109', 'tt1568346', 'tt1675434',
        'tt1853728', 'tt1877832', 'tt2024544', 'tt2267998', 'tt2380307'
    ],
    'Drama': [
        'tt0111161', 'tt0068646', 'tt0071562', 'tt0050083', 'tt0108052',
        'tt0167260', 'tt0110912', 'tt0060196', 'tt0167261', 'tt0073486',
        'tt0099685', 'tt0047478', 'tt0317248', 'tt0102926', 'tt0038650',
        'tt0245429', 'tt0118799', 'tt0120689', 'tt0816692', 'tt0114814',
        'tt0034583', 'tt0021749', 'tt0027977', 'tt0253474', 'tt0407887',
        'tt1675434', 'tt0103064', 'tt2582802', 'tt0047396', 'tt0082971',
        'tt0054215', 'tt0172495', 'tt0110475', 'tt0209144', 'tt0078788',
        'tt0032553', 'tt0043014', 'tt0405094', 'tt0057012', 'tt4154756',
        'tt0050825', 'tt0081505', 'tt1853728', 'tt0119698', 'tt0051201',
        'tt0169547', 'tt0090605', 'tt0087843', 'tt2380307', 'tt0112573'
    ],
    'Horror': [
        'tt0081505', 'tt0078748', 'tt0073486', 'tt0070047', 'tt0087843',
        'tt0119396', 'tt0054215', 'tt0167260', 'tt0209144', 'tt0114746',
        'tt1179904', 'tt1457767', 'tt1663202', 'tt1853728', 'tt2582802',
        'tt3263904', 'tt4016934', 'tt4425200', 'tt4731136', 'tt5052448',
        'tt5095030', 'tt6751668', 'tt7144666', 'tt7349950', 'tt7784604',
        'tt8772262', 'tt9419884', 'tt10298810', 'tt10954984', 'tt11286314',
        'tt11564570', 'tt13320622', 'tt13372126', 'tt13375076', 'tt13406094',
        'tt13560574', 'tt14230458', 'tt14444726', 'tt14539740', 'tt15255288',
        'tt15398776', 'tt15789038', 'tt16419074', 'tt0054215', 'tt0063522',
        'tt0067992', 'tt0070047', 'tt0073486', 'tt0078748', 'tt0081505'
    ],
    'Romance': [
        'tt0034583', 'tt0038650', 'tt0043014', 'tt0045152', 'tt0052357',
        'tt0053125', 'tt0056172', 'tt0056592', 'tt0060196', 'tt0066921',
        'tt0070735', 'tt0075314', 'tt0082096', 'tt0086879', 'tt0093779',
        'tt0102926', 'tt0105236', 'tt0114709', 'tt0118715', 'tt0119217',
        'tt0120601', 'tt0126029', 'tt0137523', 'tt0167260', 'tt0180093',
        'tt0211915', 'tt0266543', 'tt0317705', 'tt0338013', 'tt0361748',
        'tt0382932', 'tt0405094', 'tt0449059', 'tt0477348', 'tt0758758',
        'tt0816692', 'tt0910970', 'tt0993846', 'tt1205489', 'tt1323594',
        'tt1392190', 'tt1411250', 'tt1504320', 'tt1583421', 'tt1745960',
        'tt1853728', 'tt2120120', 'tt2267998', 'tt2278388', 'tt2380307'
    ],
    'Sci-Fi': [
        'tt0076759', 'tt0080684', 'tt0086190', 'tt0133093', 'tt0137523',
        'tt0167260', 'tt0167261', 'tt0209144', 'tt0245429', 'tt0338013',
        'tt0816692', 'tt1375666', 'tt0103064', 'tt0088763', 'tt0172495',
        'tt0054215', 'tt0078788', 'tt0119698', 'tt0120737', 'tt0361748',
        'tt0482571', 'tt0910970', 'tt1345836', 'tt1392190', 'tt1392214',
        'tt0407887', 'tt0468569', 'tt0477348', 'tt0499549', 'tt0758758',
        'tt0848228', 'tt0993846', 'tt1156398', 'tt1160419', 'tt1201607',
        'tt1211837', 'tt1285016', 'tt1431045', 'tt1504320', 'tt1535108',
        'tt1568346', 'tt1663662', 'tt1764651', 'tt1832382', 'tt1843866',
        'tt1853728', 'tt2015381', 'tt2024544', 'tt2096673', 'tt2267998'
    ],
    'Thriller': [
        'tt0111161', 'tt0468569', 'tt0137523', 'tt0109830', 'tt0114369',
        'tt0114814', 'tt0102926', 'tt0054215', 'tt0110357', 'tt0172495',
        'tt0110413', 'tt0078788', 'tt0095765', 'tt0095327', 'tt0090605',
        'tt0338013', 'tt0209144', 'tt0070735', 'tt0056172', 'tt0180093',
        'tt0119488', 'tt0266697', 'tt0317705', 'tt0372784', 'tt0407887',
        'tt0482571', 'tt0758758', 'tt0910970', 'tt1130884', 'tt1187043',
        'tt1201607', 'tt1345836', 'tt1375666', 'tt1392190', 'tt1397280',
        'tt1424432', 'tt1454029', 'tt1504320', 'tt1535108', 'tt1568346',
        'tt1663202', 'tt1675434', 'tt1853728', 'tt1877832', 'tt2024544',
        'tt2278388', 'tt2380307', 'tt2562232', 'tt2582802', 'tt2637276'
    ]
}

def fetch_movie_from_omdb(imdb_id, rank):
    """Fetch movie data from OMDb API"""
    try:
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}&plot=full"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('Response') == 'True':
                genres = data.get('Genre', 'Drama').split(', ')
            
            # Get high quality poster
            poster = data.get('Poster', '')
            if poster and poster != 'N/A':
                poster = poster
            else:
                poster = ''
            
            # Parse rating
            rating = 0.0
            imdb_rating = data.get('imdbRating', '0')
            try:
                rating = float(imdb_rating) if imdb_rating != 'N/A' else 0.0
            except:
                rating = 0.0
            
            # Parse year
            year = 0
            year_str = data.get('Year', '0')
            try:
                year = int(year_str.split('–')[0].split('-')[0])
            except:
                year = 0
            
            return {
                'id': imdb_id,
                'title': data.get('Title', 'Unknown'),
                'year': year,
                'rating': rating,
                'genres': genres,
                'description': data.get('Plot', 'No description available.'),
                'poster': poster,
                'rank': rank,
                'imdb_url': f'https://www.imdb.com/title/{imdb_id}/',
                'actors': data.get('Actors', ''),
                'director': data.get('Director', ''),
                'runtime': data.get('Runtime', '')
            }
        return None
    except Exception as e:
        print(f"Error fetching {imdb_id}: {e}")
        return None

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_file('index.html')

@app.route('/api/movies/top100')
def get_top100():
    """API endpoint for Top 100 movies"""
    # Check if we have cached data
    cached_movies = get_movies_from_db('top100')
    if cached_movies:
        print(f"Returning {len(cached_movies)} cached movies from database")
        return jsonify(cached_movies)
    
    # Fetch fresh data
    movies = []
    print("Fetching Top 100 movies from OMDb API...")
    
    for idx, movie_id in enumerate(TOP_100_IDS, 1):
        movie = fetch_movie_from_omdb(movie_id, idx)
        if movie:
            movies.append(movie)
            save_movie_to_db(movie, 'top100')
            print(f"Fetched {idx}/{len(TOP_100_IDS)}: {movie['title']}")
    
    print(f"Successfully fetched {len(movies)} movies")
    return jsonify(movies)

@app.route('/api/movies/top100/refresh')
def refresh_top100():
    """Refresh Top 100 movies from API"""
    movies = []
    print("Refreshing Top 100 movies from OMDb API...")
    
    for idx, movie_id in enumerate(TOP_100_IDS, 1):
        movie = fetch_movie_from_omdb(movie_id, idx)
        if movie:
            movies.append(movie)
            save_movie_to_db(movie, 'top100')
            print(f"Refreshed {idx}/{len(TOP_100_IDS)}: {movie['title']}")
    
    print(f"Successfully refreshed {len(movies)} movies")
    return jsonify(movies)

@app.route('/api/movies/2024-2025')
def get_2024_2025():
    """API endpoint for top movies 2024-2025"""
    # Check if we have cached data
    cached_movies = get_movies_from_db('2024-2025')
    if cached_movies:
        print(f"Returning {len(cached_movies)} cached movies from database")
        return jsonify(cached_movies)
    
    # Fetch fresh data
    movies = []
    print("Fetching 2024-2025 movies from OMDb API...")
    
    for idx, movie_id in enumerate(TOP_2024_2025_IDS, 1):
        movie = fetch_movie_from_omdb(movie_id, idx)
        if movie:
            movies.append(movie)
            save_movie_to_db(movie, '2024-2025')
            print(f"Fetched {idx}/{len(TOP_2024_2025_IDS)}: {movie['title']}")
    
    print(f"Successfully fetched {len(movies)} movies")
    return jsonify(movies)

@app.route('/api/movies/2024-2025/refresh')
def refresh_2024_2025():
    """Refresh 2024-2025 movies from API"""
    movies = []
    print("Refreshing 2024-2025 movies from OMDb API...")
    
    for idx, movie_id in enumerate(TOP_2024_2025_IDS, 1):
        movie = fetch_movie_from_omdb(movie_id, idx)
        if movie:
            movies.append(movie)
            save_movie_to_db(movie, '2024-2025')
            print(f"Refreshed {idx}/{len(TOP_2024_2025_IDS)}: {movie['title']}")
    
    print(f"Successfully refreshed {len(movies)} movies")
    return jsonify(movies)

@app.route('/api/movies/genre/<genre>')
def get_genre_movies(genre):
    """API endpoint for genre-specific movies"""
    if genre not in GENRE_MOVIES:
        return jsonify({'error': f'Genre {genre} not found'}), 404
    
    # Check if we have cached data
    cached_movies = get_movies_from_db(f'genre_{genre}')
    if cached_movies:
        print(f"Returning {len(cached_movies)} cached {genre} movies from database")
        return jsonify(cached_movies)
    
    # Fetch fresh data
    movies = []
    print(f"Fetching {genre} movies from OMDb API...")
    
    movie_ids = GENRE_MOVIES[genre]
    for idx, movie_id in enumerate(movie_ids, 1):
        movie = fetch_movie_from_omdb(movie_id, idx)
        if movie:
            movies.append(movie)
            save_movie_to_db(movie, f'genre_{genre}')
            print(f"Fetched {idx}/{len(movie_ids)}: {movie['title']}")
    
    print(f"Successfully fetched {len(movies)} {genre} movies")
    return jsonify(movies)

@app.route('/api/movies/genre/<genre>/refresh')
def refresh_genre_movies(genre):
    """Refresh genre-specific movies from API"""
    if genre not in GENRE_MOVIES:
        return jsonify({'error': f'Genre {genre} not found'}), 404
    
    movies = []
    print(f"Refreshing {genre} movies from OMDb API...")
    
    movie_ids = GENRE_MOVIES[genre]
    for idx, movie_id in enumerate(movie_ids, 1):
        movie = fetch_movie_from_omdb(movie_id, idx)
        if movie:
            movies.append(movie)
            save_movie_to_db(movie, f'genre_{genre}')
            print(f"Refreshed {idx}/{len(movie_ids)}: {movie['title']}")
    
    print(f"Successfully refreshed {len(movies)} {genre} movies")
    return jsonify(movies)

@app.route('/api/watched')
def get_watched():
    """Get list of watched movies"""
    watched = get_watched_movies()
    return jsonify(watched)

@app.route('/api/watched/<movie_id>', methods=['POST'])
def mark_watched(movie_id):
    """Mark a movie as watched"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO watched (movie_id, watched_date) VALUES (?, ?)',
              (movie_id, datetime.now()))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/watched/<movie_id>', methods=['DELETE'])
def unmark_watched(movie_id):
    """Unmark a movie as watched"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM watched WHERE movie_id = ?', (movie_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/genres')
def get_genres():
    """Get list of available genres"""
    return jsonify(list(GENRE_MOVIES.keys()))

if __name__ == '__main__':
    print("=" * 60)
    print("Movie Selector - Server Starting")
    print("=" * 60)
    print("Initializing database...")
    init_db()
    print("✓ Database ready")
    print("=" * 60)
    print("Server starting on: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)

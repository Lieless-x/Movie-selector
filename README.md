# 🎬 Movie Selector

A beautiful, interactive web application for discovering and tracking movies. Browse curated collections of IMDb's Top 100, recent releases (2024-2025), and genre-specific recommendations. Features an engaging spinning wheel to help you decide what to watch next!

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **📊 Curated Movie Collections**
  - IMDb Top 100 of all time
  - Top movies from 2024-2025
  - Genre-specific selections (Action, Comedy, Drama, Horror, Sci-Fi, Thriller, Romance, Adventure, Animation, Crime)

- **🎡 Interactive Spinning Wheel**
  - Can't decide what to watch? Let the wheel choose for you!
  - Select multiple movies and spin to get a random recommendation

- **✅ Watch Tracking**
  - Mark movies as watched/unwatched
  - Visual indication of watched movies (grayscale filter)
  - Persistent tracking across sessions

- **🔍 Advanced Filtering & Sorting**
  - Search by title or description
  - Filter by genre
  - Sort by rating, title, year, or IMDb rank

- **💾 Smart Caching**
  - SQLite database for local movie data storage
  - Reduces API calls and improves performance
  - Option to refresh data when needed

- **🎨 Beautiful UI**
  - Modern, responsive design
  - Dark theme with gradient backgrounds
  - Smooth animations and transitions
  - Card-based layout with movie posters

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OMDb API key (get one for free at [omdbapi.com](http://www.omdbapi.com/apikey.aspx))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/movie-selector.git
   cd movie-selector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   
   Open `server.py` and replace the placeholder with your OMDb API key:
   ```python
   OMDB_API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your actual API key
   ```

4. **Run the application**
   ```bash
   python server.py
   ```

5. **Open in browser**
   
   Navigate to `http://localhost:5000`

## 📖 Usage

### Browsing Movies

1. **Select a collection**: Choose from Top 100, 2024-2025, or a specific genre
2. **Load movies**: Click the corresponding button to fetch movie data
3. **Browse**: Scroll through the movie cards with posters, ratings, and descriptions

### Using the Spinning Wheel

1. **Select movies**: Click the "Select" button on movies you're interested in
2. **Show wheel**: Click "Show Wheel" in the controls
3. **Spin**: Click "Spin!" to let the wheel randomly select a movie for you

### Tracking What You've Watched

1. **Mark as watched**: Click the "Watched" button on any movie card
2. **Hide watched**: Use the "Hide Watched" filter to focus on unwatched movies
3. **Unmark**: Click "Unwatched" to remove the watched status

### Filtering & Searching

- **Search bar**: Type to filter by title or description
- **Genre dropdown**: Filter movies by specific genre
- **Sort dropdown**: Sort by rank, rating, title, or year

## 🛠️ Technical Details

### Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **API**: OMDb API for movie data
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Canvas API**: For the interactive spinning wheel

### Project Structure

```
movie-selector/
├── server.py              # Flask backend server
├── index.html             # Frontend interface
├── requirements.txt       # Python dependencies
├── movies.db             # SQLite database (auto-generated)
└── README.md             # This file
```

### API Endpoints

- `GET /` - Serve main HTML interface
- `GET /api/movies/top100` - Get IMDb Top 100 movies
- `GET /api/movies/2024-2025` - Get recent top movies
- `GET /api/movies/genre/<genre>` - Get genre-specific movies
- `GET /api/movies/top100/refresh` - Force refresh Top 100 data
- `GET /api/movies/2024-2025/refresh` - Force refresh recent movies
- `GET /api/movies/genre/<genre>/refresh` - Force refresh genre data
- `GET /api/watched` - Get watched movie IDs
- `POST /api/watched/<movie_id>` - Mark movie as watched
- `DELETE /api/watched/<movie_id>` - Unmark movie as watched
- `GET /api/genres` - Get available genres

### Database Schema

**movies table**
- `id` (TEXT, PRIMARY KEY) - IMDb ID
- `title` (TEXT) - Movie title
- `year` (INTEGER) - Release year
- `rating` (REAL) - IMDb rating
- `genres` (TEXT) - Comma-separated genres
- `description` (TEXT) - Plot summary
- `poster` (TEXT) - Poster image URL
- `imdb_url` (TEXT) - IMDb page URL
- `actors` (TEXT) - Main actors
- `director` (TEXT) - Director name
- `runtime` (TEXT) - Movie duration
- `category` (TEXT) - Collection category
- `rank` (INTEGER) - Position in collection
- `last_updated` (TIMESTAMP) - Last refresh date

**watched table**
- `movie_id` (TEXT, PRIMARY KEY) - IMDb ID
- `watched_date` (TIMESTAMP) - When marked as watched

## 🎨 Customization

### Adding New Movie Collections

Edit `server.py` and add your IMDb IDs to the appropriate list:

```python
# Add a new collection
MY_CUSTOM_COLLECTION = [
    'tt0111161',  # The Shawshank Redemption
    'tt0068646',  # The Godfather
    # ... more IMDb IDs
]
```

Then create corresponding API endpoints following the existing patterns.

### Styling

The CSS is embedded in `index.html`. Key customization points:

- **Color scheme**: Modify the gradient backgrounds and accent colors
- **Card layout**: Adjust grid template in `.movie-grid`
- **Animations**: Tweak transition durations and easing functions

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🎨 Enhance UI/UX
- 🔧 Submit pull requests

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Movie data provided by [OMDb API](http://www.omdbapi.com/)
- Movie rankings based on IMDb ratings
- Icons and emojis from Unicode standard

## 📧 Contact

Questions or suggestions? Feel free to open an issue on GitHub!

---

**Enjoy discovering your next favorite movie! 🍿**

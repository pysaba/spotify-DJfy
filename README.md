# DJfy: Harmonic Playlist Sorting for Spotify

DJfy is a Python-based tool that reorders Spotify playlists according to harmonic compatibility using the Camelot wheel system. The user can choose which song the new playlist should start with. By analyzing the musical key of each track, DJfy rearranges your playlist to ensure a musically coherent listening experience, perfect for DJs and music enthusiasts alike.

## Getting Started

To use DJfy, you'll need to set up Spotify API access and configure your environment with the necessary credentials.

### Prerequisites

- Python 3.6 or higher
- A Spotify Premium account
- `spotipy` - A lightweight Python library for the Spotify Web API

### Spotify API Setup

1. **Create a Spotify App**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account.
   - Click "Create an App", fill in the app name (e.g., DJfy), and description, and agree to the terms.

2. **Get Your API Credentials**:
   - Note your `Client ID` and `Client Secret` from the app page.

3. **Set the Redirect URI**:
   - Click "Edit Settings" on your app page.
   - Add a Redirect URI (e.g., `http://localhost:8888/callback`) and save.

### Configuration

Store your Spotify API credentials and Redirect URI in an `.env` file in the root directory of the project:

```env
SPOTIFY_CLIENT_ID='your_client_id_here'
SPOTIFY_CLIENT_SECRET='your_client_secret_here'
SPOTIFY_REDIRECT_URI='http://localhost:8888/callback'
```
## Installation

### Install the required Python packages:

```bash
pip install spotipy python-dotenv
```

## Usage
Run the script from your command line:

```bash
python djfy.py
```
Follow the prompts to enter your Spotify playlist ID and let the script organize your playlist harmonically.

## Upcoming Features
- Sorting by Tempo and Mood: Integrate audio feature analysis to sort tracks by tempo, mood, etc.
- Dynamic Playlist Modes:
  - Energy Levels: Create playlists that start slow and gradually increase in tempo or vice versa.
  - Mood Transitions: Sort tracks to guide listeners through a journey of changing moods.
- Web App / Website: To make DJfy more accessible and user-friendly, a web interface is in development, allowing users to interact with DJfy's features through a browser.


Stay tuned for these exciting updates.

Your feedback and contributions are welcome as we expand the project's capabilities to include more sophisticated sorting algorithms and user options.


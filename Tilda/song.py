class Song:
    def __init__(self, track_id, song_id, artist_name, song_title):
        self.track_id = track_id
        self.song_id = song_id
        self.artist_name = artist_name
        self.song_title = song_title

    def __lt__(self, other):
        # Compare based on artist_name
        return self.artist_name < other.artist_name

    def __repr__(self):
        # For easy debugging and visualization
        return f"Song({self.track_id}, {self.artist_name}, {self.song_title})"

def read_songs(file_path):
    songs = []
    with open(file_path, encoding='latin1') as file:
        for line in file:
            # Each line has the format: trackid<SEP>låt-id<SEP>artistnamn<SEP>låt-titel
            parts = line.strip().split('<SEP>')
            if len(parts) == 4:
                track_id, song_id, artist_name, song_title = parts
                song = Song(track_id, song_id, artist_name, song_title)
                songs.append(song)
    return songs

# Test the function with a smaller file
songs = read_songs("C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\unique_tracks.txt")
print(songs[:5])  # Print the first 5 songs to verify reading works correctly
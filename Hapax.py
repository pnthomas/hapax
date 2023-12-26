# pseudocode
'''
Create sourcelist file in the format [done]
    0) Number (e.g. 1-50)
    1) Common name of source
    2) Lyrics
    3) Legomena

create a UI for name + lyrics into the dictionary [done]
    Note: Can intake lyrics right now, but need to sanitize inputs. Right now reading back the lyrics blows up the json interpreter.

Process sourcelist to create a lyrics glossary table in the format
    0) lyric
    1) occurrences
    2) source(s) (number from sourcelist, comma delimited)

function glossarize()
    For each word in the song:
        Consult the lyrics glossary
            If the word exists in the glossary
                increment occurrences by 1
                append source number to the source row
            Else (the word doesn't exist in the glossary)
                add lyric to table
                set occurrence to 1
                append source number to the source row

function findhap()
    For each song in songlist:
        glossarize()
    For each lyric (row) in the songlist
        If occurrence count == 1
            add lyric to row 4 (legomena) of sourcelist
        Else
            end

function showhap()
    Sort sourcelist by number of entries in row 3 (number of uniques in that song)
        # make a copy or otherwise make sure not to break
        # the link between number and name
    For each row in sourcelist where row 3 > 0
        Print
            "Song name:" row 1
            Number: number of entries in row 3
            List: output row 3 in order
        End


Output format: A table with the heading "Hapax Legomena of Common Christmas Songs"

    Source Name: Silent Night
    Number: 4
    List: Virgin, _______, _______

    Source Name: We Wish You A Merry Christmas
    Number: 2
    List: Figgu, Pudding
'''

import json

file_path = "/Users/pthomas/Documents/Personal/python_projects/Hapax/songs.json"
with open(file_path, 'r') as file:
    songs_data = json.load(file)

#create a UI for assisting in manually adding name + lyrics into the dictionary
def add_new_song():
    # Ask the user if they want to add a new song
    user_response = input("Do you want to add a new song? (y/n): ")

    if user_response.lower() != 'y':
        print("No new song added. Exiting.")
        return

    # Prompt the user for song title
    song_title = input("Enter the title of the song and hit enter: ")

    # Prompt the user for lyrics
    song_lyrics = input("Paste in the lyrics and hit enter:\n")

    # Create a new song dictionary
    new_song = {
        'refnum': len(songs_data) + 1,  # Assuming refnum is one more than the current maximum
        'name': song_title,
        'lyrics': song_lyrics,
        'legomena': ''
    }

    # Add the new song to the list
    songs_data.append(new_song)

    # Update the .json file with the new song
    with open(file_path, 'w') as file:
        json.dump(songs_data, file)

    print(f"Song '{song_title}' added successfully!")

#Process sourcelist to create a lyrics glossary table in the format
#    0) lyric
#    1) occurrences
#    2) source(s) (number from sourcelist, comma delimited)

def generate_word_info(songs_data):
    """
    Generate information about unique words in the lyrics of songs_data.

    Parameters:
    - songs_data (list): A list of dictionaries representing songs.

    Returns:
    - dict: A dictionary containing information about unique words.
    """
    word_info = {}

    for song in songs_data:
        lyrics_words = song['lyrics'].split()

        for word in lyrics_words:
            cleaned_word = word.lower().strip('.,?!()[]{}:;\'"')

            if cleaned_word in word_info:
                word_info[cleaned_word]['count'] += 1
                word_info[cleaned_word]['refnums'].append(song['refnum'])
            else:
                word_info[cleaned_word] = {'count': 1, 'refnums': [song['refnum']]}

    print(f"\nProcessed {len(word_info)} glossary entries.")

    return word_info

def display_song_list():
    for song in songs_data:
        print(f"Refnum: {song['refnum']}, Name: {song['name']}")

def display_glossary(word_info):
    print(f"\nGlossary entries: {len(word_info)}")
    for word, info in word_info.items():
        print(f"{word} {info['count']}")

# Main menu
while True:
    print("\nSelect an operation:")
    print("1. Add new song")
    print("2. Show song list so far")
    print("3. Generate word info")
    print("4. Display the glossary")
    print("5. Exit")

    user_choice = input("Enter your choice (1-5): ")

    if user_choice == '1':
        add_new_song()
    elif user_choice == '2':
        display_song_list()
    elif user_choice == '3':
        word_info = generate_word_info(songs_data)
    elif user_choice == '4':
        display_glossary(word_info)
    elif user_choice == '5':
        print("Exiting. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
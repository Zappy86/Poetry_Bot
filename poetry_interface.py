import pandas as pd

def initialize_dataframe(data_file_input: str) -> int:
    '''Loads the `data_file` into memory. Returns `0` on completion.'''
    
    global df, data_file
    data_file = data_file_input
    try:
        df = pd.read_csv(data_file, index_col=0)
        return 0
    except:
        return -1

# Returns a set so there are no duplicates
def list_tags() -> list:
    '''Returns a set with every tag.'''
    
    tags = set()
    
    # Ignores "na", AKA NaNs, AKA missing values
    for row in df.dropna().itertuples():
        tags.update(row.Tags.split(","))
        
    return list(tags)

def get_num_of_tag(desired_tag: str) -> int:
    # Returns the sum of a boolean table, 1s and 0s, the result will be the number of True items
    return df['Tags'].str.lower().str.contains(desired_tag).sum()

def get_total_num_of_poems() -> int:
    return int(df.last_valid_index() + 1)

def get_poems_with_tag(desired_tag: str, num_of_poems: int = 5) -> list:
    '''
    Returns `num_of_poems` tuples in a list:
    
    `[(Title, Poet), (Title, Poet)]`
    '''
    # Maps a boolean table of the tags column to the original dataframe
    poems_with_tag = df[df["Tags"].str.contains(desired_tag, na=False)].reset_index()
    
    if poems_with_tag.empty:
        return []
    
    # If there are less poems than requested, return all poems, otherwise take a sample
    if int(poems_with_tag.last_valid_index() + 1) < num_of_poems:
        chosen_poems = list(zip(poems_with_tag["Title"] , poems_with_tag["Poet"]))
        return chosen_poems
    
    else:
        sample = poems_with_tag.sample(num_of_poems)
        chosen_poems = [(poem.Title, poem.Poet) for poem in sample.itertuples()]
        return chosen_poems

def get_tags_of_poem(title: str, poet: str = "") -> list:
    '''Poet param is optional, useful when more than one poem has the same name.'''
    
    tags = []
    
    # If poet was given, checks against title and poet, otherwise just title
    if poet:
        for row in df.itertuples():
            if row.Title == title and row.Poet == poet[0]:
                tags = row.Tags.split(",")
    else:
        for row in df.itertuples():
            if row.Title == title:
                tags = row.Tags.split(",")
    return tags

def get_poems_by_a_poet(poet: str, num_of_poems: int = 5) -> tuple:
    '''
    Returns a list with a list of titles and the number of titles found.
    `[[titles], num_of_titles_found]`
    '''
    
    # Maps a boolean table of the Poet column to the original dataframe, with a new index
    poems_of_poet = df[df["Poet"].str.lower().str.contains(poet.lower(), na=False)].reset_index()
        
    if poems_of_poet.empty:
        return [[], 0]
    
    num_of_titles = poems_of_poet.last_valid_index() + 1
        
    # Returns whole title column or random sample of it
    if int(num_of_titles) < num_of_poems:
        return [list(poems_of_poet["Title"]), num_of_titles]
    
    else:
        return [list(poems_of_poet.sample(num_of_poems)["Title"]), num_of_titles]

def get_poem_by_title(title: str, *poet: str) -> tuple:
    '''
    Poet param is optional, useful when more than one poem has the same name.

    Returns: `(Title, Poet, Poem)`
    '''
    
    # If poet was given, checks against title and poet, otherwise just title
    if poet:
        for row in df.itertuples():
            if str(row.Title).lower() == title.lower() and str(row.Poet).lower() == poet[0].lower():
                return (row.Title, row.Poet, row.Poem)
    else:
        for row in df.itertuples():
            if str(row.Title).lower() == title.lower():
                return (row.Title, row.Poet, row.Poem)
    return ()

def get_all_poems_with_title(title: str) -> list:
    '''
    Returns Titles and Poets as tuples in a list:
    
    `[(Title, Poet), (Title, Poet)]`
    '''
    
    # Maps a boolean table, title must match exactly, not very useful compared to search
    poems_with_title = df[df["Title"] == title]
    
    if poems_with_title.empty:
        return []    
    else:
        chosen_poems = list(zip(poems_with_title["Title"] , poems_with_title["Poet"]))
        return chosen_poems


def search_titles_for_string(search: str, num_of_poems) -> list:
    '''
    Returns a list of tuples with exact matches first, 
    
    and the number of titles that matched the string:
    
    `[[(Exact_Title, Poet), (Title, Poet)], num_of_titles]`
    '''
    
    # Compares df to boolean map, this is passed a lowercase value and checks against lowercase values
    poems_with_string = df[df["Title"].str.lower().str.contains(search, na=False)].reset_index()
    
    if poems_with_string.empty:
        return [[], 0]
    
    chosen_poems = list(zip(poems_with_string["Title"] , poems_with_string["Poet"]))

    num_of_titles = (len(chosen_poems))
    
    # Moves exact matches to front of list and returns it if there are less titles found than the requested number
    if num_of_titles < num_of_poems:
        for index, item in enumerate(chosen_poems):
            if search == item[0].lower():
                chosen_poems.insert(0, chosen_poems.pop(index))
        return [(chosen_poems), num_of_titles]
    
    # If there are more results than requested, adds exact matches to limited_poems, pops the match that was added,
    # then gets a sample for how many more are needed to bring the total to the requested number and adds that to limited_poems
    else:
        limited_poems = []
        for index, item in enumerate(chosen_poems):
            if search == item[0].lower():
                limited_poems.append(item)
                chosen_poems.pop(index)
                        
        if len(limited_poems) < num_of_poems:
            sample = poems_with_string.sample(num_of_poems - len(limited_poems))
            limited_poems += [(poem.Title, poem.Poet) for poem in sample.itertuples()]
            
        return [limited_poems, num_of_titles]
    


def get_duplicates() -> None:
    '''Function I used for debugging, for some reason there are 21 different poems named "Song"...'''
    
    duplicates = list((df.dropna()[df["Title"].dropna().duplicated(keep=False)])["Title"])
    dup_dict = {}

    for dup in duplicates:
        if dup in dup_dict:
            dup_dict[dup] += 1
        else:
            dup_dict[dup] = 1

    max_value = max(dup_dict.values())
    max_keys = next(key for key, value in dup_dict.items() if value == max_value)

    for item in dup_dict.items():
        print(f"{item[0]}: {item[1]}")
        
    print(f"Most duplicates: '{max_keys}' with {max_value} duplicates.")

def get_rand_poem(num_of_poems: int = 1) -> list:
    '''Returns list: `[(Title, Poet, Poem), (Title, Poet, Poem)]`'''
    sample = df.sample(num_of_poems)
    
    return [(poem.Title, poem.Poet, poem.Poem) for poem in sample.itertuples()]

def edit_poem(title: str, poet: str, poem_edit: str) -> None:
    '''Edit the text of a poem using it's title and author, many of the poems are formatted poorly.'''
    
    for row in df.itertuples(index=True):
        if (row.Title == title) and (row.Poet == poet):
            df.at[row[0], "Poem"] = poem_edit
    df.to_csv(data_file)
    
if __name__ == "__main__":
    import os
    print("\nPlease run 'main.py' to initialise bot!\n")
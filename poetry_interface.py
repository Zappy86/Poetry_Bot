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
def list_tags() -> set:
    '''Returns a set with every tag.'''
    tags = set()
    
    # Ignores "na", AKA NaNs, AKA missing values
    for row in df.dropna().itertuples():
        tags.update(row.Tags.split(","))
        
    return tags

def get_total_num_of_tags(desired_tag: str) -> int:
    return df['Tags'].str.contains(desired_tag).sum()

def get_total_num_of_poems() -> int:
    return df.last_valid_index()

def get_poems_with_tag(desired_tag: str, num_of_poems: int = 5) -> list:
    '''
    Returns `num_of_poems` tuples in a list:
    
    `[(Title, Poet), (Title, Poet)]`
    '''
    poems_with_tag = df[df["Tags"].str.contains(desired_tag, na=False)]
    
    if poems_with_tag.empty:
        return []
    
    if poems_with_tag.last_valid_index() < num_of_poems - 1:
        chosen_poems = list(zip(poems_with_tag["Title"] , poems_with_tag["Poet"]))
        return chosen_poems
    
    else:
        sample = poems_with_tag.sample(num_of_poems)
        chosen_poems = [(poem.Title, poem.Poet) for poem in sample.itertuples()]
        return chosen_poems

def get_tags_of_poem(title: str, poet: str = "") -> list:
    '''Poet param is optional, useful when more than one poem has the same name.'''
    tags = []
    
    if poet:
        for row in df.itertuples():
            if row.Title == title and row.Poet == poet[0]:
                tags = row.Tags.split(",")
    else:
        for row in df.itertuples():
            if row.Title == title:
                tags = row.Tags.split(",")
    return tags

def get_poems_by_a_poet(poet: str, num_of_poems: int = 5) -> list:
    '''Returns a list of Titles.'''
    poems_of_poet = df[df["Poet"].str.contains(poet, na=False)]
    if poems_of_poet.empty:
        return []
    if poems_of_poet.last_valid_index() < num_of_poems - 1:
        return list(poems_of_poet["Title"])
    else:
        return list(poems_of_poet.sample(num_of_poems)["Title"])

def get_poem_by_title(title: str, *poet: str) -> tuple:
    '''Poet param is optional, useful when more than one poem has the same name.'''
    if poet:
        for row in df.itertuples():
            if row.Title == title and row.Poet == poet[0]:
                return (row.Poet, row.Poem)
    else:
        for row in df.itertuples():
            if row.Title == title:
                return (row.Poet, row.Poem)
    return ()

def get_all_poems_with_title(title: str) -> list:
    '''
    Returns Titles and Poems as tuples in a list:
    
    `[(Title, Poet), (Title, Poet)]`
    '''
    poems_with_title = df[df["Title"] == title]
    
    if not poems_with_title.empty:
        chosen_poems = list(zip(poems_with_title["Title"] , poems_with_title["Poet"]))
        return chosen_poems
    else:
        return []

def search_titles_for_string(title: str) -> list:
    '''
    Returns a list of tuples with exact matches first:
    
    `[(Exact_Title, Poet), (Title, Poet)]`
    '''
    poems_with_string = df[df["Title"].str.contains(title, na=False)]
    
    if not poems_with_string.empty:
        chosen_poems = list(zip(poems_with_string["Title"] , poems_with_string["Poet"]))
        for index, item in enumerate(chosen_poems):
            if title == item[0]:
                chosen_poems.insert(0, chosen_poems.pop(index))
        return chosen_poems
    else:
        return []

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
    sample = df.sample(num_of_poems)
    
    return [(poem.Title, poem.Poet, poem.Poem) for poem in sample.itertuples()]

def edit_poem(title: str, poet: str, poem_edit: str) -> None:
    '''Edit the text of a poem using it's title and author, many of the poems are formatted poorly.'''
    for row in df.itertuples(index=True):
        if (row.Title == title) and (row.Poet == poet):
            df.at[row[0], "Poem"] = poem_edit
    df.to_csv(data_file)
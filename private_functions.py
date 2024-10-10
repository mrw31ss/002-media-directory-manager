from urllib.parse import quote_plus
from genericpath import isdir, isfile
import os
import re
import json
import pathlib
import requests
import datetime

# generate the current dir
def get_dir():
    return os.getcwd()

# generate current year
def get_year():
    return datetime.datetime.now().year

# list directory(ies) entries
def cur_dir_entries(watched_dir)-> list[str]:

    # check if all the given directories are valid
    watched_dirs = [dir for dir in watched_dir if isdir(dir)]

    # returns an empty list if there are no valid directories
    if not watched_dirs:return []

    # create an outer list to expand
    all_entries = list()

    # loop through each directory and collect non-hidden entries
    for dir in watched_dirs:
        dir_path = pathlib.Path(dir)
        entries = (str(path) for path in dir_path.iterdir() if not path.name.startswith("."))
        all_entries.extend(entries)

    return all_entries # return all entries from all given directories, if empty no return

# transform pathname into basename only
def to_basename(entry:str) -> str:
    return os.path.basename(entry)

# removing special chars using regex
def no_schars(string:str) -> str:
    pattern = r"[^\w\s]"
    no_spec_chars = re.sub(pattern, " ", string)
    no_extra_spaces = re.sub(r"\s+", " ", no_spec_chars)
    return no_extra_spaces

# extract 4-digit words, return index
def split_phrase(phrase:str):
    splitted = phrase.split(" ")
    word_index = 0
    for index, word in enumerate(splitted):
        if len(word) == 4 and word.isdigit():
            word_index = index
            return [word_index, splitted[word_index]]
        else: pass
    return [word_index, word_index]

# check if word is year
def is_year(title_year, start_year, cur_year):
    if (title_year != 0) and (start_year <= int(title_year) <= cur_year):
        return True
    else:
        return False

# separate words before year
def extract_title(index_year_key:list, title:str, start_year):
    list_sum = [int(x) for x in index_year_key]
    list_sum = sum(list_sum)
    if (0 <= list_sum <= start_year):
        return "PROBABLY NOT A MOVIE TITLE"
    else:
        index = index_year_key[0]
        title_split = title.split(" ")
        return " ".join(title_split[:index])

# create the google request
def google_query(query:str, api_key:str, engine_id:str, full_search:bool=False):
    # match case to filter type of query
    match full_search:
        case True:
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q={query}"
        case False:
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&fields=items(title,link)&q={query}"

    request = requests.get(url=url)
    if request.status_code == 200:
        return request.json()
    else:
        return f"ERROR CODE : {request.status_code}"

# parse imdb link to extract movie ID
def parse_imdb_link(link:str):
    if not link.startswith("https://www.imdb.com/title/"):
        return "NOT A VALID IMDB LINK"
    else:
        no_prefix_link = link.removeprefix(r"https://www.imdb.com/title/")
        imdb_code = no_prefix_link.replace("/", "")
        return imdb_code

# create the directory name
def generate_dir_name(google_response):
    try:
        media_title = google_response["items"][0]["title"].removesuffix(" - IMDb")
        imdb_link = google_response["items"][0]["link"]
        imdb_code = parse_imdb_link(imdb_link)
        return media_title + " {imdb-" + imdb_code + "}"
    except:
        return "NOT A VALID JSON OBJECT"

# read json file
def read_config(config_file_path:str):
    # try reading the file
    try:
        with open(config_file_path, "r") as f:
            config_contents = f.read()
            config_json = json.loads(config_contents)
            f.close()
            return config_json
    except json.JSONDecodeError: return "INVALID CONFIG JSON FILE" # invalid then halt

# read the config file
def get_config(cur_dir:str, config_dir:str, config_file:str):
    # normalise arguments to lower
    config_dir_norm = config_dir.lower()
    config_file_norm = config_file.lower()

    # concat path with given directory
    config_path = os.path.join(cur_dir, config_dir_norm)

    # check if given dir is valid
    if isdir(config_path): pass # is valid then continue
    else: return "INVALID CONFIGURATION FOLDER" # invalid then halt

    # concat the file name
    config_file_path = os.path.join(config_path, config_file_norm)

    # check if path is valid for file name
    if isfile(config_file_path):
        bufferd_config = read_config(config_file_path) # valid then read json
        return bufferd_config # return json object
    else:
        return "INVALID CONFIGURATION FILE" # invalid then halt

# concat the request name
def create_request_name(title:str, year:int):
    return f"{title} {year}"

# prepare the quote encoding URL with plus as space
def url_encode(quote:str):
    return quote_plus(quote)


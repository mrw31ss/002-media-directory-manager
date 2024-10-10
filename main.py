from private_functions import *

config_file = get_config(get_dir(), "002_config", "config.json")

START_YEAR = config_file["parameters"]["current_year"]
CUR_YEAR = get_year()
GOOGLE_API_KEY = config_file["credentials"]["google_api_key"]
ENGINE_ID = config_file["credentials"]["google_engine_identifier"]
WATCHED = config_file["directories"]

# list directories for all given paths in config.json
cur_entries = cur_dir_entries(WATCHED)

commands = list()

for entry in cur_entries[2:]:

    # complete path name
    title_abspath = entry
    title_basename = to_basename(entry)

    # break the loop if the file is already formatted
    if " {imdb" in title_basename:
        print(f"ALREADY FORMATTED - {title_basename}")
        continue

    # remove special characters for the entry
    title_clean = no_schars(title_basename)

    # get year for the entry and check validity
    index_year_pair = split_phrase(title_clean)
    year_check = is_year(index_year_pair[1], START_YEAR, CUR_YEAR)

    # break loop if number is not year
    if not year_check:continue

    # put the title year on a variable
    title_year = index_year_pair[1]

    # given the year index, extract the title of the entry
    title_clean = extract_title(index_year_pair, title_clean, START_YEAR)
    
    # prepare the query for the google request
    request_name = create_request_name(title_clean, title_year)
    encoded_title = url_encode(request_name)
    response = google_query(encoded_title, GOOGLE_API_KEY, ENGINE_ID)
    new_dir_name = generate_dir_name(response)

    print(f"FOUND - {new_dir_name}")
    rename_command = f"mv \"{title_basename}\" \"{new_dir_name}\""

    commands.append(rename_command)


with open("commands.txt", "a") as file:
    [file.write(f"{line}\n") for line in commands]
    file.close()
# ext/functions.py

import re
import json
import traceback

from ext.utils import invert_bytes

def process_sleeve(file_content, new_sleeve):
    inverted_content = invert_bytes(file_content)
    file_str = inverted_content.decode("utf-8", errors="replace")

    level_pattern = r'"selectedSleeveId": \d+'
    modified_file_str = re.sub(level_pattern, f'"selectedSleeveId": {new_sleeve}', file_str)

    processed_content = invert_bytes(modified_file_str.encode("utf-8"))

    return processed_content

def process_clone(content, team_id, character_id):
    inverted_content = invert_bytes(content)

    try:
        file_str = inverted_content.decode("utf-8", errors="replace")
        data = json.loads(file_str)

        for team in data["party"]["partyInfo_"]:
            if team["id_"] == team_id:
                for character in team["characters_"]:
                    character["characterId_"] = character_id

        modified_file_str = json.dumps(data, indent=4)
        processed_content = invert_bytes(modified_file_str.encode("utf-8"))

        return processed_content
    except Exception as e:
        traceback_str = traceback.format_exc()
        raise Exception(f"Error:\n{e}\n```{traceback_str}```")

def process_all_replacements(content):
    inverted_content = invert_bytes(content)

    def process_substring(substring, replacement_func):
        def replace_count(match):
            value = int(match.group(1))
            return f'{replacement_func(value)}'

        pattern = r'(?<="count":\s)(\d+)'
        processed_substring = re.sub(pattern, replace_count, substring)

        return processed_substring

    try:
        file_str = inverted_content.decode("utf-8", errors="replace")

        match_shards = re.search(r'"characterShards_": \[.*?\],', file_str, re.DOTALL)
        if match_shards:
            substring_shards = match_shards.group()
            processed_substring_shards = process_substring(substring_shards, shards_replacement)
            file_str = file_str.replace(substring_shards, processed_substring_shards)
        else:
            raise ValueError("No 'characterShards_' found in the file.")

        match_zenkai = re.search(r'"characterPlentyShards_": \[.*?\],', file_str, re.DOTALL)
        if match_zenkai:
            substring_zenkai = match_zenkai.group()
            processed_substring_zenkai = process_substring(substring_zenkai, zenkai_replacement)
            file_str = file_str.replace(substring_zenkai, processed_substring_zenkai)
        else:
            raise ValueError("No 'characterPlentyShards_' found in the file.")

        with open("Soul_boost.txt", "r") as boost_file:
            new_boost_content = boost_file.read()

        file_str = re.sub(r'"boost": \[.*?\]', f'"boost": [{new_boost_content}]', file_str, flags=re.DOTALL)

        if '"boost": [ ]' in file_str:
            with open("Soul_boost2.txt", "r") as missing_boost_file:
                new_missing_boost_content = missing_boost_file.read()

            file_str = file_str.replace('"boost": [ ]', f'"boost": [{new_missing_boost_content}]')

        arts_boosts = ["strikeArtsBoost", "shotArtsBoost", "specialArtsBoost"]
        for arts_boost in arts_boosts:
            file_str = re.sub(rf'"{arts_boost}": (\d+)', f'"{arts_boost}": 99', file_str)

        processed_content = file_str.encode("utf-8", errors="replace")
        processed_content = invert_bytes(processed_content)

        return processed_content
    except UnicodeDecodeError:
        raise ValueError("File content is not valid UTF-8 format.")

def process_combined_replacements(content):
    inverted_content = invert_bytes(content)

    def process_substring(substring, replacement_func):
        def replace_count(match):
            value = int(match.group(1))
            return f'{replacement_func(value)}'

        pattern = r'(?<="count":\s)(\d+)'
        processed_substring = re.sub(pattern, replace_count, substring)

        return processed_substring

    try:
        file_str = inverted_content.decode("utf-8", errors="replace")

        match_shards = re.search(r'"characterShards_": \[.*?\],', file_str, re.DOTALL)
        if match_shards:
            substring_shards = match_shards.group()
            processed_substring_shards = process_substring(substring_shards, shards_replacement)
            file_str = file_str.replace(substring_shards, processed_substring_shards)
        else:
            raise ValueError("No 'characterShards_' found in the file.")

        match_zenkai = re.search(r'"characterPlentyShards_": \[.*?\],', file_str, re.DOTALL)
        if match_zenkai:
            substring_zenkai = match_zenkai.group()
            processed_substring_zenkai = process_substring(substring_zenkai, zenkai_replacement)
            file_str = file_str.replace(substring_zenkai, processed_substring_zenkai)
        else:
            raise ValueError("No 'characterPlentyShards_' found in the file.")

        with open("Soul_boost.txt", "r") as boost_file:
            new_boost_content = boost_file.read()

        file_str = re.sub(r'"boost": \[.*?\]', f'"boost": [{new_boost_content}]', file_str, flags=re.DOTALL)

        if '"boost": [ ]' in file_str:
            with open("Soul_boost2.txt", "r") as missing_boost_file:
                new_missing_boost_content = missing_boost_file.read()

            file_str = file_str.replace('"boost": [ ]', f'"boost": [{new_missing_boost_content}]')

        arts_boosts = ["strikeArtsBoost", "shotArtsBoost", "specialArtsBoost"]
        for arts_boost in arts_boosts:
            file_str = re.sub(rf'"{arts_boost}": (\d+)', f'"{arts_boost}": 99', file_str)

        with open("Costume.txt", "r") as custom_file:
            custom_content = custom_file.read()

        if '"type": 19' in file_str and '"paramList": [' in file_str:
            start_index = file_str.index('"type": 19')
            param_list_start = file_str.index('"paramList": [', start_index)
            param_list_end = file_str.index(']', param_list_start)
            last_bracket_index = file_str.rfind('}', param_list_start, param_list_end)

            modified_file_str = (
                file_str[:last_bracket_index + 1] +
                custom_content +
                file_str[last_bracket_index + 1:]
            )

            processed_content = invert_bytes(modified_file_str.encode("utf-8"))

            return processed_content
        else:
            raise ValueError("Required sections not found in the file.")
    except Exception as e:
        traceback_str = traceback.format_exc()
        raise Exception(f"Error:\n{e}\n```{traceback_str}```")

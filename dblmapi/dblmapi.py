# dblmapi.py

import re

class DBLMAPIV2:
    @staticmethod
    def invert_bytes(content):
        byte_array = bytearray(content)
        for i in range(len(byte_array)):
            byte_array[i] = ~byte_array[i] & 0xFF
        inverted_content = bytes(byte_array)
        return inverted_content

    @staticmethod
    def process_file(content, callback=None):
        try:
            inverted_content = DBLMAPIV2.invert_bytes(content)
            file_str = inverted_content.decode("utf-8", errors="replace")

            # Use regex to find the substring between "characterShards_": [ and ],
            match = re.search(r'"characterShards_": \[.*?\],', file_str, re.DOTALL)
            if match:
                substring = match.group()

                # Use callback for custom processing
                if callback:
                    processed_substring = callback(substring)
                else:
                    # Default replacement function
                    def replace_count(match):
                        value = int(match.group(1))
                        return f'{9999 if 100 <= value <= 9999 else value}'

                    pattern = r'(?<="count":\s)(\d+)'
                    processed_substring = re.sub(pattern, replace_count, substring)

                processed_content = file_str.replace(substring, processed_substring)
            else:
                raise ValueError("No 'characterShards_' found in the file.")

            processed_content = processed_content.encode("utf-8", errors="replace")
            processed_content = DBLMAPIV2.invert_bytes(processed_content)

            return processed_content
        except UnicodeDecodeError:
            raise ValueError("File content is not valid UTF-8 format.")

    @staticmethod
    def zenkai_file(content, callback=None):
        try:
            inverted_content = DBLMAPIV2.invert_bytes(content)
            file_str = inverted_content.decode("utf-8", errors="replace")

            # Use regex to find the substring between "characterPlentyShards_": [ and ],
            match = re.search(r'"characterPlentyShards_": \[.*?\],', file_str, re.DOTALL)
            if match:
                substring = match.group()

                # Use callback for custom processing
                if callback:
                    processed_substring = callback(substring)
                else:
                    # Default replacement function
                    def replace_count(match):
                        value = int(match.group(1))
                        return f'{7000 if 0 <= value <= 7000 else value}'

                    pattern = r'(?<="count":\s)(\d+)'
                    processed_substring = re.sub(pattern, replace_count, substring)

                processed_content = file_str.replace(substring, processed_substring)
            else:
                raise ValueError("No 'characterPlentyShards_' found in the file.")

            processed_content = processed_content.encode("utf-8", errors="replace")
            processed_content = DBLMAPIV2.invert_bytes(processed_content)

            return processed_content
        except UnicodeDecodeError:
            raise ValueError("File content is not valid UTF-8 format.")

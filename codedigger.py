import os
import re
import pickle
import chardet
from datetime import datetime
from rapidfuzz import fuzz


class CodeDigger:
    def __init__(self, codebase_directories, codebase_version):
        self.codebase_directories = codebase_directories
        self.index_version = codebase_version
        self.index_timestr = None
        self.index_dict = {}
        self.load_dictionary()

    def process_java_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()
                class_pattern = r'\bclass\s+(\w+)'
                class_names = re.findall(class_pattern, content)
                for class_name in class_names:
                    if class_name not in self.index_dict:
                        self.index_dict[class_name] = [filename]
                    elif filename not in self.index_dict[class_name]:
                        self.index_dict[class_name].append(filename)

                tokens = content.replace('(', ' ').replace(')', ' ').split()
                for token in tokens:
                    if len(token) > 3 and not token.startswith('"') and not token.endswith('"'):
                        key = token.strip()
                        if not key.isdigit() and key != '':
                            if key in self.index_dict:
                                if filename not in self.index_dict[key]:
                                    self.index_dict[key].append(filename)
                            else:
                                self.index_dict[key] = [filename]
        except FileNotFoundError:
            print(f"The file {filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def index_files(self, directory):
        cnt = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                cnt += 1
                print(f"\rProgress: {cnt} files", end='', flush=True)
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        rawdata = f.read()
                    encoding = chardet.detect(rawdata)['encoding']
                    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                        self.process_java_file(file_path)
        print()

    def save_dictionary(self):
        dictionaries_dir = os.path.join(os.path.dirname(__file__), 'dictionaries', self.index_version)
        os.makedirs(dictionaries_dir, exist_ok=True)
        filename = os.path.join(dictionaries_dir, f"{self.index_timestr}.pkl")
        with open(filename, 'wb') as f:
            pickle.dump(self.index_dict, f)

    def load_dictionary(self):
        dictionaries_dir = os.path.join(os.path.dirname(__file__), 'dictionaries', self.index_version)
        if not os.path.exists(dictionaries_dir):
            return {}
        files = os.listdir(dictionaries_dir)
        pickle_files = [f for f in files if f.endswith('.pkl') and len(f) == 18]
        if not pickle_files:
            return {}
        pickle_files.sort()
        filename = os.path.join(dictionaries_dir, pickle_files[-1])
        with open(filename, 'rb') as f:
            self.index_timestr = pickle_files[-1][:-4]
            self.index_dict = pickle.load(f)

    def count_java_files(self):
        java_file_count = 0
        for directory in self.codebase_directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.java'):
                        java_file_count += 1
        return java_file_count

    def process_codebase(self):
        for directory in self.codebase_directories:
            self.index_files(directory)
        self.index_timestr = datetime.now().strftime("%Y%m%d%H%M%S")
        self.save_dictionary()

    def lookup(self, keyword):
        return self.index_dict.get(keyword, [])

    def find_most_similar_keyword(self, potential_keyword):
        best_match = None
        highest_similarity = 0
        for key in self.index_dict.keys():
            similarity = fuzz.ratio(potential_keyword, key)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = key
        return best_match

    def find_most_similar_keywords(self, potential_keyword, threshold=80):
        similar_keys = []
        for key in self.index_dict.keys():
            similarity = fuzz.ratio(potential_keyword, key)
            if similarity >= threshold:
                similar_keys.append((key, similarity))
        similar_keys.sort(key=lambda x: x[1], reverse=True)
        return [key for key, _ in similar_keys]

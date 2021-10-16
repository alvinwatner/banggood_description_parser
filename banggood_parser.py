import copy
import pandas as pd

from bs4 import BeautifulSoup as bs
from typing import List

# from styleframe import StyleFrame


class BanggoodDescription():
    def __init__(self, csv):
        self.list_of_titles = ['Main Features:',
                               'Feature:', 'Features:',
                               'Description:', 'Descriptions:',
                               'Specification:', 'Specifications:',
                               'Package included:', 'Package Included:', 'Package Includes :']

        self.banggood_csv = csv
        prodID_key = 'Product_ID'

        self.desc_key = 'description'
        self.description_data = csv[self.desc_key]

        self.output_df = {prodID_key : self.banggood_csv[prodID_key],
                          'description': []}

    def __getitem__(self, idx):
        return self.description_data[idx]

    def __len__(self):
        return len(self.description_data)

    def check_substring(self, string, sub_str):
        if (string.find(sub_str) == -1):
            return False
        else:
            return True

    def check_duplicate(self, text, previous_text):

        if text in previous_text:
            isDuplicate = True
        else:
            isDuplicate = False

        return isDuplicate

    def detect_unwanted_string(self, text):
        if text == 'Details Pictures:':
            return True

        elif self.check_substring(text, 'Download'):
            if self.check_substring(text, 'Click'):
                return True

        elif text == ' ':
            return True

        else:
            return False

    def read(self, html: str = None,
             list_of_titles: List = None,
             disallowed_characters: List = [';'],
             duplicate_penalty: int = 2,
             extract_all: bool = False,
             check_duplicate: bool = True
             ):

        if list_of_titles is None:
            list_of_titles = self.list_of_titles

        # If field is empty
        if pd.isna(html):
            nan_string = 'Maaf deskripsi produk dibuat kosong karena alasan tertentu. Harap chat untuk info lebih detail'
            stored_descriptions = nan_string
            parsed_data = nan_string
            return parsed_data, stored_descriptions

        if html == ' ':
            nan_string = 'Maaf deskripsi produk dibuat kosong karena alasan tertentu. Harap chat untuk info lebih detail'
            stored_descriptions = nan_string
            parsed_data = nan_string
            return parsed_data, stored_descriptions

        soup = bs(html, features="html.parser")

        list_of_titles_states = copy.deepcopy(list_of_titles)

        previous_text = []
        duplicate_penalty_counter = 0

        parsed_data = []

        stored_descriptions = ''

        first_title = False
        flag = False
        isDuplicate = False
        joint_info = False

        temporary_title = ''

        # extract all data without filtering
        if extract_all:
            for s in soup.find_all('span'):
                parsed_data.append(s.text)
                stored_descriptions += s.text
                stored_descriptions += '\n'

        # extract and filter data
        else:

            for s in soup.find_all('span'):
                if flag == True:
                    for title in list_of_titles_states:
                        if self.check_substring(s.text, title):
                            flag = False

                            if not first_title:
                                first_title = True
                            elif first_title:
                                stored_descriptions += '\n'
                                stored_descriptions += '\n'

                            break

                    if flag:

                        text = s.text

                        if check_duplicate:
                            isDuplicate = self.check_duplicate(text, previous_text)

                        if text == '' or s.parent.name == 'td':
                            pass

                        else:

                            if isDuplicate == True:
                                pass

                            # The asssumption is that any text end up to this section is the
                            # "main data" (text) not the "title (temporary_title)". Therefore just in case
                            # the "main_data" == "title", then we will ignore it. Because it will be
                            # unnecessary to add the "title" to our "main_data".
                            # The trade-off of this mechanism is that it will sometimes ruin the
                            # "first_title" mechanism

                            elif temporary_title == text:
                                stored_descriptions += '\n'
                                pass

                            elif temporary_title == 'Specifications:':
                                array = [p.name for p in s.parents]
                                if 'td' in array[:2]:
                                    pass

                            elif self.detect_unwanted_string(text):
                                pass

                            elif self.check_substring(text, 'Other'):
                                if self.check_substring(text, 'Options'):
                                    flag = False

                            # Else Data is allowed to be parsed
                            else:
                                for char in disallowed_characters:
                                    text = text.replace(char, '')

                                if first_row:
                                    # print(f"=================   {temporary_title}   ==========")
                                    stored_descriptions += "=================="
                                    stored_descriptions += '\n'
                                    stored_descriptions += temporary_title
                                    stored_descriptions += '\n'
                                    stored_descriptions += "=================="
                                    stored_descriptions += '\n'

                                first_row = False

                                # print(f"[FLAG] title : {temporary_title} | text : {text}")

                                if joint_info:

                                    stored_descriptions += joint_info_text
                                    stored_descriptions += '\n'

                                    # reset joint info states
                                    joint_info = False
                                    joint_info_text = ''

                                else:

                                    stored_descriptions += text
                                    stored_descriptions += '\n'

                                parsed_data.append(text)

                                if duplicate_penalty_counter == duplicate_penalty:
                                    # reset
                                    duplicate_penalty_counter = 0
                                    previous_text = []
                                else:
                                    previous_text.append(text)
                                    duplicate_penalty_counter += 1

                if flag == False:
                    for title in list_of_titles_states:
                        if self.check_substring(s.text, title):

                            # if s.text > longer than the longest title, then the title and the description is joint
                            if len(s.text) > len('Package included:') + 5:
                                joint_info = True
                                joint_info_text = copy.deepcopy(s.text)

                            flag = True
                            list_of_titles_states.remove(title)
                            temporary_title = title
                            first_row = True
                            break

        return parsed_data, stored_descriptions

    def parse_html(self, html):
        parsed_data, stored_descriptions = self.read(html)
        if len(parsed_data) == 0:
            parsed_data, stored_descriptions = self.read(html, extract_all=True)

        if len(stored_descriptions) < 10:
            nan_string = 'Maaf deskripsi produk dibuat kosong karena alasan tertentu. Harap chat untuk info lebih detail'
            stored_descriptions = nan_string

        self.output_df['description'].append(stored_descriptions)

        return parsed_data, stored_descriptions

    def convert_bangood_to_toped(self, path=None, index=None, description=None):
        pass

    def export_to_banggood_csv(self, path):
        df = pd.DataFrame(self.output_df)
        df.to_csv(path, index = False)
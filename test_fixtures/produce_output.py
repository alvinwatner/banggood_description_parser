import pandas as pd
from banggood_parser import BanggoodDescription


def produce_output(source_path = None, output_path = None):
    bangood_csv = pd.read_csv(source_path)
    bd = BanggoodDescription(bangood_csv)

    for index in range(len(bd)):

        html = bd[index]
        parsed_data, stored_descriptions = bd.parse_html(html)

        full_output_path = output_path + f'grount_truth.csv'
        bd.export_to_banggood_csv(full_output_path, index = index, description = stored_descriptions)


data_version = 'v1'
produce_output(source_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/inputs/product_info_{data_version}.csv',
           output_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/outputs/{data_version}/',
           )


data_version = 'v2'
produce_output(source_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/inputs/product_info_{data_version}.csv',
           output_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/outputs/{data_version}/',
           )

import pandas as pd
from tqdm import tqdm
from banggood_parser import BanggoodDescription

def produce_output(source_path = None, output_path = None):
    bangood_csv = pd.read_csv(source_path)
    bd = BanggoodDescription(bangood_csv)

    for index in tqdm(range(len(bd))):

        html = bd[index]
        _, _ = bd.parse_html(html)

    full_output_path = output_path + f'output.csv'
    bd.export_to_banggood_csv(full_output_path)

#
# data_version = 'v1'
# produce_output(source_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/inputs/input_{data_version}.csv',
#            output_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/outputs/{data_version}/',
#            )
#
#
# data_version = 'v2'
# produce_output(source_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/inputs/input_{data_version}.csv',
#            output_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/outputs/{data_version}/',
#            )
#

data_version = 'v3'
produce_output(source_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/inputs/input_{data_version}.csv',
           output_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/outputs/{data_version}/',
           )


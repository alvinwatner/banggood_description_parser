import pandas as pd
from tqdm import tqdm
from banggood_parser import BanggoodDescription


def compare_outputs_with_ground_truths(output_path = None, ground_truth_path = None):
    gt_csv = pd.read_csv(ground_truth_path)
    output_csv = pd.read_csv(output_path)

    gt_bd = BanggoodDescription(gt_csv)
    o_bd = BanggoodDescription(output_csv)

    #step 1 : check length
    assert len(gt_bd) == len(o_bd)

    #step 2 : check string data

    for index in tqdm(range(len(gt_bd)), desc='[TESTING]'):

        gt_description_data = gt_bd[index]
        o_description_data = o_bd[index]

        assert gt_description_data == o_description_data


data_version = 'v1'
output_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/outputs/{data_version}/output.csv'
ground_truth_path = f'/home/alvinwatner/banggood_description_parser/test_fixtures/ground_truths/{data_version}/grount_truth.csv'

compare_outputs_with_ground_truths(output_path=output_path, ground_truth_path=ground_truth_path)
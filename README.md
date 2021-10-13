## Banggood Description Parser
The purpose of this repository is to parse the 'product_info.csv' that you can obtained from banggood marketplace and do the following
* Read the html script
* Extract the content within the title that we care about (e.g., Features, Specifications)


## Sanity Check Mechanism
The current mechanism to evaluate any updated algorithm is by using the <bold>test/test_compare_output_with_gt.py</bold> script. This script simply compare if the updated script 'outputs' == 'grount_truths'. 

To update the 'grount_truths', it should satisfied the following :
1) Failed to run testing script.
2) The reason it is failed is because the updated script result in an 'outputs' contents that is better than the previous 'ground_truths'.

To determine if it is better or worse is :
1) It is better : When the ouput contents is less-truncated and more readable.
2) It is worse : When the ouput contents get truncated more and less readable.


# pArborist
A Seed for Privacy - semi-automatic privacy-revealing data detection in databases and data streams

All nessesary parts to run pArborist are included in this repository.

## Datasets
(1)  The labeled datasets are in the labeled_datasets folder.

(2) The public datasets used for pArborist are partially cached in binary files to run pArborist, but not directly accessible here in order to clarify the credits of their original producers. Please find them in their original websites/research [1], [2], [3], [4]. 

(3) Only the datasets labeled or produced by us are directly provided here as promised.

## Run pArborist
(1) pArborist is implemented in Python.

(2) A requirements.py is attached. All used packages can be loaded via pip, no specific requirements for their versions.

### Mode 1 - for Users of pArborist:
1. Use the default seeds randomly generated in input_seeds.txt. OR Replace the contents in input_seeds with your own seeds. One row each. The format of a seed must be:

   <div align="center">
    number   event1   event2   event3...
    </div>

2. Execute detect_p_r_queries.py
3. Check natural language results in output.txt and pandas.datafram results in output_csv.csv OR directly check the console.

The output.txt stores the results in natural language for users.

The output_csv.csv stores the results in pandas.DataFrame format for developers.

### Mode 2 - for Experiements:

1. Execute expr.py for python.
2. Check natural language results in output_expr.txt and pandas.datafram results in output_expr_csv.csv OR directly check the console.

The output_expr.txt stores the results in natural language.

The output_expr_csv.csv stores the results in pandas.DataFrame format.

Due to the size limit of github, only the cache of a portion of the datasets are utilized. This produce the same results as a full-scale experiments, since the cache follows the same distribution and schema of the original dataset, see [1], [2], [3], [4].

## Reference
[1] Albert Kim and Adriana Escobedo-Land. 2015. OkCupid Data for Introductory
Statistics and Data Science Courses. Journal of Statistics Education 23 (07 2015).
https://doi.org/10.1080/10691898.2015.11889737

[2] IBRAHIM Sabuncu. 2020. USA Nov. 2020 Election 20 Mil. Tweets (with Sentiment
and Party Name Labels) Dataset (2020). URL https://dx. doi. org/10.21227/25te-j338
(2020).

[3] Dingqi Yang, Bingqing Qu, Jie Yang, and Philippe Cudre-Mauroux. 2019. Revis-
iting user mobility and social relationships in lbsns: a hypergraph embedding
approach. In The world wide web conference. 2147–2157.

[4] Dingqi Yang, Bingqing Qu, Jie Yang, and Philippe Cudré-Mauroux. 2020.
Lbsn2vec++: Heterogeneous hypergraph embedding for location-based social
networks. IEEE Transactions on Knowledge and Data Engineering 34, 4 (2020),
1843–1855.

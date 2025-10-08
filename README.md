# pArborist
A Seed for Privacy - semi-automatic privacy-revealing data detection in databases and data streams.

## Datasets and Folders
(1) See the datasets labeled by us in **labeled_datasets** folder. 

(2) Only the datasets labeled or produced by us are directly provided here as promised. The public datasets used for pArborist are partially cached in binary files to run pArborist, but not directly accessible here in order to clarify the credits of their original producers. Please find them in their original websites/research [1], [2], [3], [4]. 

(3) **outputs_back_up** contains the stored outputs for a quick review and providea a quick overview of the outputs.

## Run pArborist
(1) pArborist is implemented in Python.

(2) A **requirements.py** is attached. All used packages can be loaded via pip, no specific requirements for their versions.

### Mode 1: for Experiements:
1. Execute **expr.py** via python. The default mode is **Data Stream Mode**. Run **Database Mode** by executing **expr.py** with **--mode=1**.
2. Check the results(natural language) in **output_expr.txt** and results(pandas.DataFrame) in **output_expr_csv.csv** OR directly check the console. Examples can be seen in **outputs_back_up** folder.
   
   For example (parts of **outputs_back_up/output_expr (DATA STREAM).txt**):
   ```
   ... ... ...
   ______________________________________________________
   ++++++++++++  MODE: DATA STREAM ++++++++++++
   ++++++       New data incoming!!!      ++++++
                New incoming data: 100
                New derived queries: 0
                Now number of data: 800
                Now number of derived queries: 217
   Recall: 0.638 Precision: 0.9908
   ______________________________________________________
   ______________________________________________________
   ______________________________________________________
   +++++++ MODE: DATA STREAM (updated) +++++++
   ++++++       New data incoming!!!      ++++++
                New incoming data: 100
                New derived queries: 78
                Now number of data: 900
                Now number of derived queries: 295
   Recall: 0.8754 Precision: 1.0
   ______________________________________________________
   ______________________________________________________
   ... ... ...
   ```
3. (Optional) Compare the results with the labeled data in **labeled_datasets** folder.

**FYI**:
   
The **output_expr.txt** stores the results and a brief report in natural language.

The **output_expr_detailed.txt** stored the concrete derived queries in natural language.

The **output_expr_csv.csv** stores the results in pandas.DataFrame format.

### Mode 2: for Users of pArborist:
1. Use the default seeds randomly generated in **input_seeds.txt**. OR Replace its contents with your own seeds. One row each. The format of a seed must be:

   <div align="center">
    number   event1   event2   event3...
    </div>

2. Run **detect_p_r_queries.py**
3. Check the results(natural language) in **output.txt** and results(pandas.DataFrame) in **output_csv.csv** OR directly check the console.

**FYI**:

The **output.txt** stores the results and a brief report in natural language.

The **output_detailed.txt** stored the concrete derived queries in natural language.

The **output_csv.csv** stores the results in pandas.DataFrame format for developers.

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

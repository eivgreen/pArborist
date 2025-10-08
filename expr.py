# -*- coding: utf-8 -*-

from derive_queries import select_a_pair
from derive_queries import derive_pairs
from derive_queries import translate_results
from derive_queries import translate_seed
from cons_pArbo import corrCheckK
from cons_pArbo import queryPairs
from cons_pArbo import condIndeCheck

import pandas as pd
import random
import sys
import argparse
import pickle

#produce recall and precision
def check_derived_pairs(derived_results, labeled_pairs):    
    positive = 0
    negative = 0
    for derived_result in derived_results:
        find = False
        for labeled_pair in labeled_pairs:
            if derived_result[2:] == labeled_pair[2:]:
                find = True
        if find:
            positive = positive + 1
        else:
            negative = negative + 1
    return [positive, negative]

if __name__ == '__main__':
    with open("output_expr_detailed.txt", "w") as text_file:
        text_file.write("______________________________________________________\n")
        
    with open("output_expr.txt", "w") as text_file:
        text_file.write("______________________________________________________\n")
        
    expr_seed = 567
    max_num_seeds = 8
    mode = 1
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=int, 
                        nargs='?', default = mode)
    parser.add_argument("--numSeeds", type=int, 
                        nargs='?', default = max_num_seeds - 1)
    parser.add_argument("--randomSeed", type=int, 
                        nargs='?', default = expr_seed)
       
    args = parser.parse_args()
    mode = args.mode
    num_seeds = args.numSeeds
    random.seed(args.randomSeed)
    
    
    df_expr = pd.read_csv('original_dataset.csv', sep = ",", nrows = 1000)
    
    if args.randomSeed == expr_seed:
        recall_precision = True
        with open("cache/labeled_data", "rb") as fp:   # Unpickling
            recall_precision_data = pickle.load(fp)
    else:
        recall_precision = False
        
    column_names = ["name", "venue", "long", "lati", "brand", "country", "time"]
    print_n_l = False
    
    import pickle
    import copy
    with open("cache/que_res", "rb") as fp:   # Unpickling
       que_res = pickle.load(fp)
    with open("cache/tree", "rb") as fp:   # Unpickling
       tree = pickle.load(fp)
    
    n = max_num_seeds
    if mode == 0:
        min_n = max_num_seeds - 1
    else:
        min_n = 1
        
    for num_s in range(min_n, n):
        random.seed(args.randomSeed)
        seed_pairs = []
        for i in range(num_s):
            num_layer = random.randint(1, 7)
            selected_attrs = random.sample(column_names, k = num_layer)
            num_seed = random.randint(1, 999)
            seed_temp = select_a_pair(df_expr, num_seed, selected_attrs)
            seed_pairs.append(seed_temp)

        if mode == 0:
            num = 10
        else:
            num = 1
            
        unit = int(len(df_expr)/num)
        num_derived_pairs_temp = 0
        for counter_parts in range(num):
            df_i = df_expr[: (counter_parts+1)*unit]
            que_res_temp = copy.deepcopy(que_res)
            for i1 in range(len(que_res_temp)):
                for i2 in range(len(que_res_temp[i1])):
                    que_res_temp[i1][i2] = [x for x in que_res_temp[i1][i2] if x < (counter_parts+1)*unit]
                    # for i3 in range(len(que_res_temp[i1][i2])):
                    #     if que_res_temp[i1][i2][i3] > unit:
                    #         print("before")
                    #         print(que_res_temp[i1][i2][i3], unit)
                    #         print(que_res_temp[i1][i2])
                    #         que_res_temp[i1][i2].remove(que_res_temp[i1][i2][i3])
                    #         print("after")
                    #         print(que_res_temp[i1][i2])
                            
            derived_pairs_list = derive_pairs(seed_pairs, que_res_temp, df_i, repeat = False)
    
            all_shown_derived_pairs = []
            
            num_derived_pairs = 0
            for derived_pairs in derived_pairs_list:
                for result in derived_pairs:
                    show_results = []
                    for counter in range(len(result)):
                        if counter >=2:
                            if result[counter][-1] == 'name':
                                result[counter][0] = str(int(result[counter][0]))
                            if result[counter][-1] == 'long':
                                result[counter][0] = str(round(float(result[counter][0]), 6))
                                result[counter][1] = str(round(float(result[counter][1]), 6))
                            if result[counter][-1] == 'lati':
                                result[counter][0] = str(round(float(result[counter][0]), 6))
                                result[counter][1] = str(round(float(result[counter][1]), 6))
                            if result[counter][-1] == 'time':
                                result[counter][0] = str(int(result[counter][0]))
                                result[counter][1] = str(int(result[counter][1]))
                            show_results.append((result[counter]))
                        else:
                            show_results.append((result[counter]))
                    all_shown_derived_pairs.append(show_results)
                num_derived_pairs = num_derived_pairs + len(derived_pairs)
            
            if recall_precision:
                results = check_derived_pairs(all_shown_derived_pairs, recall_precision_data)
                recall = round(results[0]/len(recall_precision_data), 4)
                if len(all_shown_derived_pairs) == 0:
                    precision = "N/A"
                else:
                    precision = round(1 - results[1]/len(all_shown_derived_pairs), 4)
            
            new_num_derived_pairs = num_derived_pairs - num_derived_pairs_temp
            num_derived_pairs_temp = num_derived_pairs
            if counter_parts == 0 and mode == 0:
                print("Warm-up ... Start!")
            if num == 1:
                print("++++++   MODE: DATABASE with " + str(num_s) + " seeds.  ++++++")
            elif new_num_derived_pairs == 0:
                print("++++++++++++  MODE: DATA STREAM", " ++++++++++++")
            else:
                print("+++++++ ", "MODE: DATA STREAM (updated)", " +++++++")
            print("++++++       New data incoming!!!      ++++++")
            print("             New incoming data: ", unit)
            print("             New derived queries: ", new_num_derived_pairs)
            print("             Now number of data: ", (counter_parts + 1)*unit)
            print("             Now number of derived queries: ", num_derived_pairs)
            if recall_precision:
                print("Recall: ", recall, " Precision: ", precision)
            if counter_parts == 0 and mode == 0:
                print("Warm-up .. Completed!")
            print("______________________________________________________")
            print("______________________________________________________")
            
            
            
            with open("output_expr.txt", "a") as text_file:
                text_file.write("______________________________________________________\n")
                if counter_parts == 0 and mode == 0:
                    text_file.write("Warm-up ... Start!\n")
                if num == 1:
                    text_file.write("++++++   MODE: DATABASE with " + str(num_s) + " seeds.  ++++++\n")
                elif new_num_derived_pairs == 0:
                    text_file.write("++++++++++++  MODE: DATA STREAM ++++++++++++\n")
                else:
                    text_file.write("+++++++ MODE: DATA STREAM (updated) +++++++\n")
                text_file.write("++++++       New data incoming!!!      ++++++\n")
                text_file.write("             New incoming data: " + str(unit))
                text_file.write("\n             New derived queries: " + str(new_num_derived_pairs))
                text_file.write("\n             Now number of data: " + str((counter_parts + 1)*unit))
                text_file.write("\n             Now number of derived queries: " + str(num_derived_pairs))
                if recall_precision:
                    text_file.write("\nRecall: " + str(recall) + " Precision: " + str(precision))
                if counter_parts == 0 and mode == 0:
                    text_file.write("\nWarm-up .. Completed!")
                text_file.write("\n______________________________________________________\n")
                text_file.write("______________________________________________________\n")
                
            with open("output_expr_detailed.txt", "a") as text_file:
                text_file.write("______________________________________________________\n")
                if counter_parts == 0 and mode == 0:
                    text_file.write("Warm-up ... Start!\n")
                if num == 1:
                    text_file.write("++++++   MODE: DATABASE with " + str(num_s) + " seeds.  ++++++\n")
                elif new_num_derived_pairs == 0:
                    text_file.write("++++++++++++  MODE: DATA STREAM ++++++++++++\n")
                else:
                    text_file.write("+++++++ MODE: DATA STREAM (updated) +++++++\n")
                text_file.write("++++++       New data incoming!!!      ++++++\n")
                text_file.write("             New incoming data: " + str(unit))
                text_file.write("\n             New derived queries: " + str(new_num_derived_pairs))
                text_file.write("\n             Now number of data: " + str((counter_parts + 1)*unit))
                text_file.write("\n             Now number of derived queries: " + str(num_derived_pairs))
                if recall_precision:
                    text_file.write("\nRecall: " + str(recall) + " Precision: " + str(precision))
                if counter_parts == 0 and mode == 0:
                    text_file.write("\nWarm-up .. Completed!")
                text_file.write("\n______________________________________________________\n")
                text_file.write("______________________________________________________\n")
            
            if new_num_derived_pairs != 0 or counter_parts == num - 1:
                translated_results = translate_results(all_shown_derived_pairs)
                
                df_temp = pd.DataFrame(derived_pairs_list)
            
                labeled_data_output = copy.deepcopy(derived_pairs_list)
                for i in range(len(labeled_data_output)):
                    # if i%100 == 0:
                    #     print(i)
                    for j in range(len(labeled_data_output[i])):
                        labeled_data_output[i][j] = labeled_data_output[i][j][2:]
                seeds_output = pd.Series(seed_pairs)
                output_temp = pd.DataFrame(labeled_data_output)
                
                length = len(output_temp.columns)
                columns = ['input']
                for i in range(length):
                    columns.append('privacy-revealing query ' + str(i+1))
                output = pd.concat([seeds_output, output_temp], axis = 1)
                output.columns = columns
                output.to_csv('output_expr_csv.csv', index = False)
                        
                with open("output_expr_detailed.txt", "a") as text_file:
                    for i in range(len(seed_pairs)):
                        seed = seed_pairs[i]
                        text_file.write("___________________________________________\n")
                        text_file.write("Privacy Requirements " + str(i+1) + " " + translate_seed(seed))
                        text_file.write("\n___________________________________________\n")
                    for i in range(len(translated_results)):
                        text_file.write("___________________________________________\n")
                        text_file.write("(" + str(i+1) + ") " + translated_results[i] + "\n")
                        
                if print_n_l:
                    for i in range(len(seed_pairs)):
                        seed = seed_pairs[i]
                        print("___________________________________________")
                        print("Requirements (" + str(i+1) + ") " + translate_seed(seed))
                        print("___________________________________________")
                    
                    for i in range(len(translated_results)):
                        print("___________________________________________")
                        print("(" + str(i+1) + ") " + translated_results[i])
                    #print(data)
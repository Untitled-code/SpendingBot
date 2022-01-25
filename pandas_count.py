import pandas as pd

def count_results(input_file):
    pd.set_option('float_format', '{:.2f}'.format)
    dt = pd.read_csv(input_file)
    print(dt.info())
    recipt_count = dt[["recipt_name", "amount"]].groupby("recipt_name").sum()/1000
    recipt_count_sort = recipt_count.sort_values("amount", ascending=False).head(10)
    print('Найбільше трансакцій з цим розпорядникам мали фірми: (тис. грн.')
    print(recipt_count_sort)
    payers_count = dt[["payers_name", "amount"]].groupby("payers_name").sum()/1000
    payers_count_sort = payers_count.sort_values("amount", ascending=False).head(10)
    print('Найбільше трансакцій з цим розпорядникам мали фірми: (тис. грн.')
    print(payers_count_sort)
    return recipt_count_sort, payers_count_sort


# count_results(output_file_csv)
# count_results('dir_959676595/output_2022-01-24_14-56-47.csv')
from collections import Counter

#clean data

#Aux Functions
#break down each column by row types which are a string into a list and concat them Ex: "AI, FinTech, Life Sciences" -->> ["AI, FinTech, Life Sciences"]
def count_verticals(data, col_name):    

    verticals_list = []
    #iterate over the entire "verticals" column
    for index, row in data.iterrows():
        #accevalue_countstical value

        verticals_list = verticals_list + (row[col_name].replace(", ", ",").replace("*", "").split(","))

    return Counter(verticals_list)  

words_to_del_list = [' TMT', 'TMT', ' SaaS', 'SaaS', 'Artificial Intelligence & Machine Learning', '', ' Mobile', 'Mobile', ' Artificial Intelligence & Machine Learning', ' Mobile Commerce']

def delete_non_rel_vert(counts, list_=words_to_del_list):
    for word in list_:
        del counts[word]
    return counts
    
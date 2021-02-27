import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
    

#plotting functions
def bar_plot(data, col_name):

    plt.figure(figsize = (15, 10))

    col_data = data[col_name].value_counts()
    x = list(col_data.index)
    y = list(col_data.values)

    plt.xlabel(col_name)
    plt.ylabel("Frequency")
    plt.title(col_name + "Bar Plot")
    plt.bar(x=x, height=y, width=0.9, color='#86bf91')

    col_data_percent = (col_data)/(col_data.sum())*100
    df = pd.DataFrame([col_data, col_data_percent])
    df.index = [col_name, "% of Total"]
    plt.xticks(rotation=90);
    
    return df


def hist_plot(title, col, col_name, bins):
    ax = col.hist(bins=bins, grid=False, figsize=(8,6), color='#86bf91', zorder=2, rwidth=0.9)
    
    # Despine
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.figure(figsize = (15, 10))
    # Draw horizontal axis lines
    vals = ax.get_yticks()
    for tick in vals:
        ax.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Remove title
    ax.set_title(title, weight='bold', size=16)

    # Set x-axis label
    ax.set_xlabel(col_name, labelpad=20, weight='bold', size=12)

    # Set y-axis label
    ax.set_ylabel("Frequency", labelpad=20, weight='bold', size=12)
    
    series = col.value_counts()
    series_percent = (series)/(series.sum())*100
    exit_df = pd.DataFrame([series, series_percent])
    exit_df.index = [col_name, "% of Total"]
    plt.xticks(rotation=90);
    
    return exit_df

def plot_stacked(data, seed, early, later, col_name, counts):    
    HQ_10_df = data[col_name].value_counts().index[:counts]
    HQ_10_seed = seed.loc[seed[col_name].isin(HQ_10_df)]
    HQ_10_early = early.loc[early[col_name].isin(HQ_10_df)]
    HQ_10_later = later.loc[later[col_name].isin(HQ_10_df)]
    plt.figure(figsize = (15, 10))
    #edit seed HQ so shapes are all equal
    HQ_10_seed = HQ_10_seed[col_name].value_counts().sort_index()
    if col_name == 'HQ Location':
        MV = pd.Series([0], index=["Mountain View, CA"])
        HQ_10_seed = HQ_10_seed.append(MV).sort_index()
    
    HQ_10_early = HQ_10_early[col_name].value_counts().sort_index()
    HQ_10_later = HQ_10_later[col_name].value_counts().sort_index()

    d = {'Seed' : HQ_10_seed, 
          'Early' : HQ_10_early,
        'Later' : HQ_10_later} 
    
    df_grouped = pd.DataFrame(d)
    if col_name == 'Year Founded':
        df_grouped.index = df_grouped.index.map(str)

    fields = ['Seed','Early','Later']
    colors = ['#1D2F6F', '#8390FA', '#86bf91']
    labels = ['Seed','Early','Later']
    # figure and axis
    fig, ax = plt.subplots(1, figsize=(12, 10))
    # plot bars
    left = len(df_grouped) * [0]
    for idx, name in enumerate(fields):
        plt.barh(df_grouped.index, df_grouped[name], left = left, color=colors[idx])
        left = left + df_grouped[name]
    # title, legend, labels
    plt.legend(labels, bbox_to_anchor=([0.55, 1, 0, 0]), ncol=4, frameon=False)
    plt.xlabel('Frequency')
    # remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # adjust limits and draw grid lines
    plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    plt.show()
    
    
def plot_stacked_vert(data_seed, data_early, data_later, col_name):   
    data_seed.fillna("", inplace=True)
    data_early.fillna("", inplace=True)
    data_later.fillna("", inplace=True)
    counts_seed = count_verticals(data_seed, col_name)
    counts_seed = delete_non_rel_vert(counts_seed)
    #order data by most common verticals
    verticals_seed = counts_seed.most_common(20)
    verticals_seed

    counts_early = count_verticals(data_early, col_name)
    counts_early = delete_non_rel_vert(counts_early)
    #order data by most common verticals
    verticals_early = counts_early.most_common(20)
    verticals_early


    counts_later = count_verticals(data_later, col_name)
    counts_later = delete_non_rel_vert(counts_later)
    #order data by most common verticals
    verticals_later = counts_later.most_common(20)

    df_seed = pd.DataFrame(verticals_seed, columns=[col_name, "Seed"])
    df_early = pd.DataFrame(verticals_early, columns=[col_name, "Early"])
    df_later = pd.DataFrame(verticals_later, columns=[col_name, "Later"])

    # df_seed
    df_all = pd.merge(df_seed, df_early,on=[col_name])
    df_all = pd.merge(df_all, df_later,on=[col_name])
    df_all.set_index(col_name, inplace=True)
    df_all

    df_grouped = df_all.copy()
    fields = ['Seed','Early','Later']
    colors = ['#1D2F6F', '#8390FA', '#86bf91']
    labels = ['Seed','Early','Later']
    # figure and axis
    fig, ax = plt.subplots(1, figsize=(12, 10))
    # plot bars
    left = len(df_grouped) * [0]
    for idx, name in enumerate(fields):
        plt.barh(df_grouped.index, df_grouped[name], left = left, color=colors[idx])
        left = left + df_grouped[name]
    # title, legend, labels
    plt.legend(labels, bbox_to_anchor=([0.55, 1, 0, 0]), ncol=4, frameon=False)
    plt.xlabel('Frequency')
    # remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # adjust limits and draw grid lines
    plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    plt.show()
    
    
def hist_distribution(data_seed, data_early, data_later, col_name):
    seed = data_seed[col_name]
    early = data_early[col_name]
    later = data_later[col_name]
    print("Seed Average {} and Median are: {} and {}".format(col_name, seed.sum()/len(seed), seed.median()))
    print("Early (A/B) Average {} and Median are: {} and {}".format(col_name , early.sum()/len(early), early.median()))
    print("Later (C+) Average {} and Median are: {} and {}".format(col_name, later.sum()/len(later), later.median()))
    bins = np.linspace(0, 100, 20)
    plt.figure(figsize = (15, 10))
    plt.hist(seed, bins, alpha=0.8, label='Seed stage')
    plt.hist(early, bins, alpha=0.6, label='Early Stage (A/B)')
    plt.hist(later, bins, alpha=0.4, label='Later Stage (C+)')
    plt.legend(loc='upper right')
    plt.xlabel(col_name+" $ (M)")
    plt.ylabel("Frequency")
    plt.title("{} Distributions for Different Stages".format(col_name));


# helper functions
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind


def filter_data(df, is_ud, is_stem, is_abstract, is_written):
    df = df[df['isUD'].apply(lambda x: x==is_ud)]
    df = df[df['isSTEM'].apply(lambda x: x==is_stem)]
    if is_stem:
        df = df[df['isAbstract'].apply(lambda x: x==is_abstract)]
    else:
        df = df[df['isWritten'].apply(lambda x: x==is_written)]

    return df[df['isPreGPT'].apply(lambda x: x==True)], df[df['isPreGPT'].apply(lambda x: x==False)]

def plot_dist(pre_gpt, post_gpt):
    plt.figure(figsize=(20, 12))

    plt.subplot(2,2,1)
    sns.histplot(
        pre_gpt['Avg Grade Received'],
        kde=True,
        color='blue',
        label='Pre-GPT',
        bins=20
    )
    sns.histplot(
        post_gpt['Avg Grade Received'],
        kde=True,
        color='orange',
        label='Post-GPT',
        bins=20
    )
    plt.title('Distribution of Avg. Grades Received (Unormalized)')
    plt.legend()

    plt.subplot(2,2,2)
    sns.histplot(
        pre_gpt['Avg Grade Received'],
        kde=True,
        color='blue',
        label='Pre-GPT',
        stat='probability',
        bins=20
    )
    sns.histplot(
        post_gpt['Avg Grade Received'],
        kde=True,
        color='orange',
        label='Post-GPT',
        stat='probability',
        bins=20
    )
    plt.title('Distribution of Avg. Grades Received (Normalized)')
    plt.legend()

    plt.subplot(2,2,3)
    sns.boxplot(
        data={
            'Pre-GPT': pre_gpt['Avg Grade Received'],
            'Post-GPT': post_gpt['Avg Grade Received']
        },
        fill=False
    )
    plt.title('Boxplot of Avg. Grades Received')

    plt.show()

def bootstrap_ttest(group1, group2, n=1000):
    t_stats = []
    p_vals = []

    for _ in range(n):
        sample1 = np.random.choice(group1, size=len(group1), replace=True)
        sample2 = np.random.choice(group2, size=len(group2), replace=True)

        t_stat, p_val = ttest_ind(sample1, sample2, equal_var=False)

        t_stats.append(t_stat)
        p_vals.append(p_val)

    return t_stats, p_vals

def plot_bootstrap_test(t_stats, p_vals, alpha=0.05):
    plt.figure(figsize=(20, 6))

    temp = plt.subplot(1,2,1)
    sns.histplot(t_stats, kde=True, stat='probability')
    plt.title('Distribution of t-statistics')

    plt.subplot(1,2,2)
    sns.histplot(p_vals, kde=True, stat='probability', bins=100)
        # bins are manually set to 100 to avoid explosion in number of bins
    plt.axvline(x=0.05, color='r', linestyle='--', label='alpha')
    plt.title('Distribution of p-values')
    plt.legend()

    plt.show()
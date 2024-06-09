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


def bootstrap_ttest(
    group1,
    group2,
    p_nums = 1000,
    bootstrap_nums = 1000,
    equal_var = False
):
    observed_t, _ = ttest_ind(group1, group2, equal_var=equal_var)
    
    # convert group1 and group2 into numpy array
    group1 = group1.to_numpy()
    group2 = group2.to_numpy()
    total = np.concatenate((group1, group2))
    
    p_vals = []
    
    for _ in range(p_nums):
        # find bootstrapped t-stats
        bootstrap_t = []
        for _ in range(bootstrap_nums):
            sample1 = np.random.choice(total, size=len(group1), replace=True)
            sample2 = np.random.choice(total, size=len(group2), replace=True)

            t_stat, _ = ttest_ind(sample1, sample2)

            bootstrap_t.append(t_stat)
        
        # find actual p_val
        bootstrap_t = np.array(bootstrap_t)
        p_val = np.mean(np.abs(bootstrap_t) > np.abs(observed_t))
        p_vals.append(p_val)

    return observed_t, bootstrap_t, p_vals


def plot_bootstrap_test(observed_t, bootstrap_t, p_vals, alpha=0.05):
    plt.figure(figsize=(20, 6))

    plt.subplot(1,2,1)
    plt.hist(bootstrap_t, density=True, edgecolor='k', bins=20, alpha=0.7)
    plt.axvline(x=observed_t, color='r', linestyle='--', label='observed t-statistics')
    plt.title('Distribution of bootstrapped t-statistics in one simulation')
    plt.legend()

    plt.subplot(1,2,2)
    plt.hist(p_vals, density=True, edgecolor='k', alpha=0.7)
    plt.axvline(x=0.05, color='r', linestyle='--', label='alpha')
    plt.title('Distribution of p-values')
    plt.legend()

    plt.show()
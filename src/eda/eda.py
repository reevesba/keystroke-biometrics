''' Keystroke Biometrics Exploratory
    Data Analysis

Author: Bradley Reeves
Date: June 1, 2021

'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    dataset = pd.read_csv("../../dat/keystroke_biometrics.csv")

    # Peek the dataset
    print(dataset)

    # Check for outliers w/ boxplot
    boxplot_data = dataset.drop(["is_bot"], axis=1)
    sns.set(rc={"figure.figsize": (12, 8)})
    boxplot = sns.boxplot(
        x="variable",
        y="value",
        data=pd.melt(boxplot_data),
        dodge=False
    )
    boxplot.set(ylim=(0, 2000))
    boxplot.figure.savefig("../../out/eda_boxplot.png")
    plt.close()

    # View distributions and correlations
    pairplot = sns.pairplot(dataset, hue="is_bot")
    pairplot.savefig("../../out/eda_pairplot.png")
    plt.close()

    # Check the statistics for each group
    print(dataset.groupby("is_bot").describe())


if __name__ == "__main__":
    main()

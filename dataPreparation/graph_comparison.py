from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def compute_graph(df_to_graph: pd.DataFrame):
    fig, ax = plt.subplots()
    x1 = df_to_graph['year'].astype(str) + '-W' + df_to_graph['week'].astype(str)
    y1 = df_to_graph['incidence'].reset_index(drop=True)

    ax.plot(x1, y1, label='Inzidenz Entwicklung in {}'.format(df_to_graph['administrative_area_level_3'].iloc[0]))
    ax.set_xlabel('Zeit')
    ax.set_ylabel('Inzidenz')
    ax.set_title('Inzidenzverlauf')
    ax.set_xticks(np.arange(len(x1)))
    ax.set_xticklabels(x1, rotation=45)
    ax.legend()
    return fig

def compute_diff_graphs(actual_course: pd.DataFrame, alternate_course: pd.DataFrame):
    fig, ax = plt.subplots()

    x1 = actual_course['year'].astype(str) + '-W' + actual_course['week'].astype(str)
    x2 = alternate_course['year'].astype(str) + '-W' + alternate_course['week'].astype(str)
    y1 = actual_course['incidence'].reset_index(drop=True)
    y2 = alternate_course['incidence'].reset_index(drop=True)

    ax.plot(x1, y1, label='Reale Entwicklung')
    ax.plot(x2, y2, label='Alternative Entwicklung')
    ax.set_xlabel('Zeit')
    ax.set_ylabel('Inzidenz')
    ax.set_title('Inzidenzverlauf')
    ax.set_xticks(range(len(x1)))
    ax.set_xticklabels(x1, rotation=45)

    ax.fill_between(x1, y1, y2, color='green', alpha=0.5)
    ax.legend()
    return fig

def compute_integral(original_graph: pd.DataFrame, alternative_graph: pd.DataFrame):
    """
    Compute integral
    :param original_graph: df of the original course
    :param alternative_graph:df of the alternative course
    :return: diff integral between both scenario
    High positive values means: alternative course is better
    High negative values means: original course is better
    """
    incidence_one = original_graph['incidence']
    incidence_two = alternative_graph['incidence']
    return np.trapz(incidence_one - incidence_two)

def main():
    df_hamburg = pd.read_csv('data/Clean/Mockup/df_hamburg.csv')
    df_ahrweiler = pd.read_csv('data/Clean/Mockup/df_ahrweiler.csv')
    compute_graph(df_hamburg).show()
    compute_graph(df_ahrweiler).show()
    compute_diff_graphs(df_hamburg, df_ahrweiler).show()
    print(compute_integral(df_hamburg, df_ahrweiler))

if __name__ == '__main__':
    main()

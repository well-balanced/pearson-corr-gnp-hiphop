
import pandas as pd
import matplotlib.pylab as plt
import csv
from utils import load_data_as_dict

def visualize():
    gnp_dict = load_data_as_dict('gnp.csv')
    preference_dict = load_data_as_dict('preference.csv')

    if gnp_dict.keys() == preference_dict.keys():
        gnp_list = list(map(float, gnp_dict.values()))
        preference_list = list(map(float, preference_dict.values()))

        # Make data frame
        body = pd.DataFrame(
            {'GNP': gnp_list, 'Hip-Hop preference': preference_list}
        )
        
        print_pearson_corr_result(body)

        # Draw scatter
        plt.scatter(body['GNP'], body['Hip-Hop preference'], label = 'data')
        plt.legend(loc = 'best')
        plt.xlabel('GNP')
        plt.ylabel('Hip-Hop preference')
        plt.show()

    else:
        print('data consistency was away')

def print_pearson_corr_result(body):
    """
                            GNP  Hip-Hop preference
    GNP                 1.000000           -0.283328
    Hip-Hop preference -0.283328            1.000000

    a negative weak correlation = lower GNP, higher hip-hop preference.
    """
    corr = body.corr(method='pearson')
    print(corr)

visualize()
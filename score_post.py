from ILAMB import Post
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import matplotlib as mpl
import os

def time_basic_score(samples):
    [samples1, samples2, samples3, samples4] = samples
    model_score = []
    for i, (stddev, corrcoef) in enumerate(samples1):
        model_score.append(corrcoef)  # /abs(stddev-1))
    for i, (stddev, corrcoef) in enumerate(samples2):
        model_score[i] += corrcoef  # /abs(stddev-1)
    for i, (stddev, corrcoef) in enumerate(samples3):
        model_score[i] += corrcoef  # / abs(stddev - 1)
    for i, (stddev, corrcoef) in enumerate(samples4):
        model_score[i] += corrcoef  # / abs(stddev - 1)
        model_score[i] /= 4.0
    return model_score

class score_system(object):
    def __init__(self, mainfiledir, site_name, models_name, variable_list, variable_scores, repsonse_score):
        self.filedir = mainfiledir
        self.site_name = site_name
        self.models_name = models_name
        self.variable_list = variable_list
        self.variable_scores = variable_scores # variable, scoretype, site, models
        self.response_score = repsonse_score
        self.type_score = (variable_scores[:,0,:,:]+variable_scores[:,1,:,:])/2


    def plot_summary(self):
        for j, site in enumerate(self.site_name):
            print('Process score_' + ''.join(site) + '_No.' + str(j) + '!')
            figname = self.filedir + 'score' + '/' + ''.join(site) + 'summary_score.png'
            data = (self.type_score[:, j, :]+ self.type_score[:, j, :]) # how to define this caculations???
            # print(data123.shape,len(self.models_name), len(self.variable_list))
            Post.BenchmarkSummaryFigure(self.models_name, self.variable_list, data, figname)
            plt.close('all')

    def plot_summary_all(self):

        fig, axes = plt.subplots(len(self.site_name), len(self.models_name), sharex=True, sharey=True, figsize=(15,2*len(self.site_name)))
        fig.subplots_adjust(wspace=0.03, hspace=0.03)
        color_vals = [-1, 0, 1]
        # my_norm = mpl.colors.Normalize(-1, 1)  # maps your data to the range [0, 1]
        # my_cmap = mpl.cm.get_cmap('RdBu', len(color_vals))  # can pick your color map
        ax_cb = fig.add_axes([.91, .3, .03, .4])
        for i in range(len(self.site_name)): # site
            for j in range(len(self.models_name)): # models
                array = self.type_score[:, i, j]  ## Put n variables in each site
                # array = [15, 30, 45, 10]
                df_cm = pd.DataFrame(array)
                # ax.pie(array, autopct=lambda(p): '{v:d}'.format(p * sum(list(array)) / 100), startangle=90,colors=my_cmap(my_norm(color_vals)))
                sn.heatmap(df_cm, annot=True, cbar=i == 0, ax=axes[i][j],
                           vmin=0, vmax=1,
                           cbar_ax=None if i else ax_cb)
                # print(i, j)
                if j == 0:
                    axes[i][j].set_ylabel(''.join(self.site_name[i]))
                if i == len(self.site_name) - 1:
                    axes[i][j].set_xlabel(self.models_name[j])
                # axes[i][j].axis('off')
                axes[i][j].set_yticklabels([])
                axes[i][j].set_xticklabels([])
        fig.savefig(self.filedir + 'summary.png')

    def plot_all(self):
        directory = self.filedir + 'score' + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.plot_summary()
        self.plot_summary_all()
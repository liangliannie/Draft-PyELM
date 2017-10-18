import matplotlib.pyplot as plt
import numpy as np
from score_post import time_basic_score
from taylorDiagram import plot_daylor_graph
from taylorDiagram import plot_daylor_graph_new
fontsize = 14

def plot_categories(fig0, obs, mod, j):
    [h_obs, d_obs, m_obs, y_obs, h_t_obs, d_t_obs, m_t_obs, y_t_obs] = obs
    [h_mod, d_mod, m_mod, y_mod, h_t_mod, d_t_mod, m_t_mod, y_t_mod] = mod
    plt.rcParams.update({'font.size': 16})
    data1 = h_obs[j, :][~h_obs[j, :].mask]
    data2 = d_obs[j, :][~d_obs[j, :].mask]
    data3 = m_obs[j, :][~m_obs[j, :].mask]
    data4 = y_obs[j, :][~y_obs[j, :].mask]
    h_t_obs, d_t_obs, m_t_obs, y_t_obs = h_t_obs[~h_obs[j, :].mask], d_t_obs[~d_obs[j, :].mask], m_t_obs[~m_obs[j, :].mask], y_t_obs[~y_obs[j, :].mask]
    models1, models2, models3, models4 = [], [], [], []
    for i in range(len(d_mod)):
        models1.append(h_mod[i][j, :][~h_obs[j, :].mask])
        models2.append(d_mod[i][j, :][~d_obs[j, :].mask])
        models3.append(m_mod[i][j, :][~m_obs[j, :].mask])
        models4.append(y_mod[i][j, :][~y_obs[j, :].mask])
    fig0, sample1 = plot_daylor_graph(data1, models1, fig0, 422)
    fig0, sample2 = plot_daylor_graph(data2, models2, fig0, 424)
    fig0, sample3 = plot_daylor_graph(data3, models3, fig0, 426)
    fig0, sample4 = plot_daylor_graph(data4, models4, fig0, 428)
    ax0 = fig0.add_subplot(4, 2, 1)
    ax1 = fig0.add_subplot(4, 2, 3)
    ax2 = fig0.add_subplot(4, 2, 5)
    ax3 = fig0.add_subplot(4, 2, 7)
    # print(type(data1))
    ax0.plot(h_t_obs, data1, 'k-', label='Observed')
    ax1.plot(d_t_obs, data2, 'k-', label='Observed')
    ax2.plot(m_t_obs, data3, 'k-', label='Observed')
    ax3.plot(y_t_obs, data4, 'k-', label='Observed')
    for i in range(len(h_mod)):
        ax0.plot(h_t_obs, models1[i], '-', label= "Model "+str(i+1))
        ax1.plot(d_t_obs, models2[i], '-', label= "Model "+str(i+1))
        ax2.plot(m_t_obs, models3[i], '-', label= "Model "+str(i+1))
        ax3.plot(y_t_obs, models4[i], '-', label= "Model "+str(i+1))
    return fig0, ax0, ax1, ax2, ax3, [sample1, sample2, sample3, sample4]


def plot_new_categories(fig0, obs, mod, j, rect1, rect2, rect3, rect4, rect, ref_times):
    [h_obs, d_obs, m_obs, y_obs, h_t_obs, d_t_obs, m_t_obs, y_t_obs] = obs
    [h_mod, d_mod, m_mod, y_mod, h_t_mod, d_t_mod, m_t_mod, y_t_mod] = mod
    plt.rcParams.update({'font.size': 16})
    data1 = h_obs[j, :][~h_obs[j, :].mask]
    data2 = d_obs[j, :][~d_obs[j, :].mask]
    data3 = m_obs[j, :][~m_obs[j, :].mask]
    data4 = y_obs[j, :][~y_obs[j, :].mask]
    h_t_obs, d_t_obs, m_t_obs, y_t_obs = h_t_obs[~h_obs[j, :].mask], d_t_obs[~d_obs[j, :].mask], m_t_obs[~m_obs[j, :].mask], y_t_obs[~y_obs[j, :].mask]
    models1, models2, models3, models4 = [], [], [], []
    for i in range(len(d_mod)):
        models1.append(h_mod[i][j, :][~h_obs[j, :].mask])
        models2.append(d_mod[i][j, :][~d_obs[j, :].mask])
        models3.append(m_mod[i][j, :][~m_obs[j, :].mask])
        models4.append(y_mod[i][j, :][~y_obs[j, :].mask])
    # fig0, sample1 = plot_daylor_graph(data1, models1, fig0, 422)
    # fig0, sample2 = plot_daylor_graph(data2, models2, fig0, 424)
    # fig0, sample3 = plot_daylor_graph(data3, models3, fig0, 426)
    # fig0, sample4 = plot_daylor_graph(data4, models4, fig0, 428)
    fig0, samples1, samples2, samples3, samples4 = plot_daylor_graph_new(data1, data2, data3, data4, models1, models2, models3, models4, fig0, rect=rect, ref_times=ref_times)

    ax0 = fig0.add_subplot(rect1)
    ax1 = fig0.add_subplot(rect2)
    ax2 = fig0.add_subplot(rect3)
    ax3 = fig0.add_subplot(rect4)

    ax0.plot(h_t_obs, data1, 'k-', label='Observed')
    ax1.plot(d_t_obs, data2, 'k-', label='Observed')
    ax2.plot(m_t_obs, data3, 'k-', label='Observed')
    ax3.plot(y_t_obs, data4, 'k-', label='Observed')
    for i in range(len(h_mod)):
        ax0.plot(h_t_obs, models1[i], '-', label="Model " + str(i + 1))
        ax1.plot(d_t_obs, models2[i], '-', label= "Model " + str(i + 1))
        ax2.plot(m_t_obs, models3[i], '-', label= "Model " + str(i + 1))
        ax3.plot(y_t_obs, models4[i], '-', label= "Model " + str(i + 1))
    # fig0.legend(line,labels, loc='upper left')
    ax0.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    return fig0, ax0, ax1, ax2, ax3, [samples1, samples2, samples3, samples4]


class basic_post(object):

    def __init__(self, variable, site_name, filedir):
        self.variable = variable
        self.sitename = site_name
        self.filedir = filedir


    def plot_basic_time_series_for_each_site(self, hour_obs, hour_mod, day_obs, day_mod, month_obs, month_mod, year_obs, year_mod):
        [h_obs, h_t_obs, h_unit_obs] = hour_obs
        [h_mod, h_t_mod, h_unit_mod] = hour_mod
        [m_obs, m_t_obs, m_unit_obs] = month_obs
        [m_mod, m_t_mod, m_unit_mod] = month_mod
        [d_obs, d_t_obs, d_unit_obs] = day_obs
        [d_mod, d_t_mod, d_unit_mod] = day_mod
        [y_obs, y_t_obs, y_unit_obs] = year_obs
        [y_mod, y_t_mod, y_unit_mod] = year_mod

        scores = []
        for j, site in enumerate(self.sitename):
            # if j==2: break
            # fig0, ax0 = plt.subplots(nrows=4, ncols=2)
            fig0 = plt.figure(figsize=(14, 18))
            print('Process on time_basic_' + ''.join(site) + '_No.' + str(j) + '!')
            obs = [h_obs, d_obs, m_obs, y_obs, h_t_obs, d_t_obs, m_t_obs, y_t_obs]
            mod = [h_mod, d_mod, m_mod, y_mod, h_t_mod, d_t_mod, m_t_mod, y_t_mod]

            # fig0, ax0, ax1, ax2, ax3, samples = plot_categories(fig0, obs, mod, j)
            fig0, ax0, ax1, ax2, ax3, samples = plot_new_categories(fig0, obs, mod, j, 411, 412, 425, 427, 224, 5)

            model_score = time_basic_score(samples)
            scores.append(model_score)


            # plt.suptitle(self.variable + '( ' + h_unit_obs + ' )', fontsize=20)
            ax0.set_xlabel('Time',fontsize=fontsize)
            ax0.set_ylabel(self.variable + '( ' + h_unit_obs + ' )', fontsize=fontsize)
            ax1.set_xlabel('Time',fontsize=fontsize)
            ax1.set_ylabel(self.variable + '( ' + d_unit_obs + ' )', fontsize=fontsize)
            ax2.set_xlabel('Time',fontsize=fontsize)
            ax2.set_ylabel(self.variable + '( ' + m_unit_obs + ' )', fontsize=fontsize)
            ax3.set_xlabel('Time',fontsize=fontsize)
            ax3.set_ylabel(self.variable + '( ' + y_unit_obs + ' )', fontsize=fontsize)

            ax0.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax1.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax2.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax3.legend(loc='upper right', shadow=False, fontsize='medium')

            # plt.tight_layout()
            # plt.show()
            fig0.savefig(self.filedir + self.variable + '/' + ''.join(site)+'_' + 'time_basic' +'_' + self.variable + '.png')
            plt.close('all')
            # print(model_score)
        # print(scores)
        # assert False
        scores = np.asarray(scores)
        return scores


    def plot_pdf(self, hour_obs, hour_mod, day_obs, day_mod, month_obs, month_mod, year_obs, year_mod):
        [h_obs, h_t_obs, h_unit_obs] = hour_obs
        [h_mod, h_t_mod, h_unit_mod] = hour_mod
        [m_obs, m_t_obs, m_unit_obs] = month_obs
        [m_mod, m_t_mod, m_unit_mod] = month_mod
        [d_obs, d_t_obs, d_unit_obs] = day_obs
        [d_mod, d_t_mod, d_unit_mod] = day_mod
        [y_obs, y_t_obs, y_unit_obs] = year_obs
        [y_mod, y_t_mod, y_unit_mod] = year_mod
        scores = []
        for j, site in enumerate(self.sitename):
            print('Process on PDF_' + ''.join(site) + '_No.' + str(j) + '!')
            fig1 = plt.figure(figsize=(8, 15))
            h_obs_sorted = np.ma.sort(h_obs[j, :]).compressed()
            d_obs_sorted = np.ma.sort(d_obs[j, :]).compressed()
            m_obs_sorted = np.ma.sort(m_obs[j, :]).compressed()
            y_obs_sorted = np.ma.sort(y_obs[j, :]).compressed()
            # print(h_obs[j,:].shape)
            # print(h_obs_sorted)
            p1_data = 1. * np.arange(len(h_obs_sorted)) / (len(h_obs_sorted) - 1)
            p2_data = 1. * np.arange(len(d_obs_sorted)) / (len(d_obs_sorted) - 1)
            p3_data = 1. * np.arange(len(m_obs_sorted)) / (len(m_obs_sorted) - 1)
            p4_data = 1. * np.arange(len(y_obs_sorted)) / (len(y_obs_sorted) - 1)
            ax4 = fig1.add_subplot(4, 1, 1)
            ax5 = fig1.add_subplot(4, 1, 2)
            ax6 = fig1.add_subplot(4, 1, 3)
            ax7 = fig1.add_subplot(4, 1, 4)

            ax4.plot(h_obs_sorted, p1_data, label='Observed')
            ax5.plot(d_obs_sorted, p2_data, label='Observed')
            ax6.plot(m_obs_sorted, p3_data, label='Observed')
            ax7.plot(y_obs_sorted, p4_data, label='Observed')

            for i in range(len(d_mod)):
                ax4.plot(np.ma.sort((h_mod[i][j, :][~h_obs[j, :].mask])), p1_data, label="Model "+str(i+1))
                ax5.plot(np.ma.sort((d_mod[i][j, :][~d_obs[j, :].mask])), p2_data, label="Model "+str(i+1))
                ax6.plot(np.ma.sort((m_mod[i][j, :][~m_obs[j, :].mask])), p3_data, label="Model "+str(i+1))
                ax7.plot(np.ma.sort((y_mod[i][j, :][~y_obs[j, :].mask])), p4_data, label="Model "+str(i+1))

            # fig1, ax4, ax5, ax6, ax7 = plot_categories(fig1, obs, mod, j)
            ax4.set_ylabel('CDF',fontsize=12)
            ax4.set_xlabel(self.variable + '( ' + h_unit_obs + ' )', fontsize=12)
            ax5.set_ylabel('CDF',fontsize=12)
            ax5.set_xlabel(self.variable + '( ' + d_unit_obs + ' )', fontsize=12)
            ax6.set_ylabel('CDF',fontsize=12)
            ax6.set_xlabel(self.variable + '( ' + m_unit_obs + ' )', fontsize=12)
            ax7.set_ylabel('CDF',fontsize=12)
            ax7.set_xlabel(self.variable + '( ' + y_unit_obs + ' )', fontsize=12)

            ax4.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax5.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax6.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax7.legend(loc='upper right', shadow=False, fontsize='medium')

            fig1.savefig(self.filedir + self.variable + '/' + ''.join(site) + '_' + 'pdf' + '_' + self.variable + '.png')
            plt.close('all')
        scores = np.asarray(scores)
        return scores



def time_analysis(variable_name, h_site_name_obs, filedir, hour_obs, hour_mod, day_obs, day_mod, month_obs, month_mod, year_obs, year_mod):
    f1 = basic_post(variable_name, h_site_name_obs, filedir)
    scores_time_series = f1.plot_basic_time_series_for_each_site(hour_obs, hour_mod, day_obs, day_mod, month_obs, month_mod, year_obs, year_mod)
    scores_pdf = f1.plot_pdf(hour_obs, hour_mod, day_obs, day_mod, month_obs, month_mod, year_obs, year_mod)
    return scores_time_series, scores_pdf
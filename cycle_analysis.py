from basic_post import plot_categories
from basic_post import plot_new_categories
from score_post import time_basic_score
import numpy as np
import matplotlib.pyplot as plt

class cycle_post(object):
    def __init__(self, variable, site_name, filedir,h_unit_obs, d_unit_obs,m_unit_obs, y_unit_obs):
        self.variable = variable
        self.sitename = site_name
        self.filedir = filedir
        self.h_unit_obs, self.d_unit_obs, self.m_unit_obs, self.y_unit_obs = h_unit_obs, d_unit_obs,m_unit_obs, y_unit_obs


    def plot_days_cycle_for_each_site(self, hour_np_s1, hour_np_s2, hour_np_s3, hour_np_s4, mhour_np_s1, mhour_np_s2, mhour_np_s3, mhour_np_s4):
        hour_mean_np_s1, hour_error_np_s1 = hour_np_s1.mean(axis=0), hour_np_s1.std(axis=0)
        hour_mean_np_s2, hour_error_np_s2 = hour_np_s2.mean(axis=0), hour_np_s2.std(axis=0)
        hour_mean_np_s3, hour_error_np_s3 = hour_np_s3.mean(axis=0), hour_np_s3.std(axis=0)
        hour_mean_np_s4, hour_error_np_s4 = hour_np_s4.mean(axis=0), hour_np_s4.std(axis=0)
        mhour_mean_np_s1, mhour_mean_np_s2, mhour_mean_np_s3, mhour_mean_np_s4 = [], [], [], []
        Time_scale = np.arange(0, 24)
        m_xasix = []
        for m in range(len(mhour_np_s1)):
            mhour_mean_np_s1.append(mhour_np_s1[m].mean(axis=0))
            mhour_mean_np_s2.append(mhour_np_s2[m].mean(axis=0))
            mhour_mean_np_s3.append(mhour_np_s3[m].mean(axis=0))
            mhour_mean_np_s4.append(mhour_np_s4[m].mean(axis=0))
            m_xasix.append(Time_scale)

        obs = [hour_mean_np_s1, hour_mean_np_s2, hour_mean_np_s3, hour_mean_np_s4, Time_scale, Time_scale, Time_scale, Time_scale]
        mod = [mhour_mean_np_s1, mhour_mean_np_s2, mhour_mean_np_s3, mhour_mean_np_s4, m_xasix, m_xasix, m_xasix,
               m_xasix]
        scores = []
        for j, site in enumerate(self.sitename):
            fig0 = plt.figure(figsize=(15, 18))
            print('Process on day_cycle_' + ''.join(site) + '_No.' + str(j) + '!')

            ''' Observations data need to use masked '''
            # obs = [mhour_mean_np_s1[0], mhour_mean_np_s2[0], mhour_mean_np_s3[0], mhour_mean_np_s4[0], m_xasix[0], m_xasix[0], m_xasix[0], m_xasix[0]]

            # fig0, ax0, ax1, ax2, ax3, samples = plot_categories(fig0, obs, mod, j)

            fig0, ax0, ax1, ax2, ax3, samples = plot_new_categories(fig0, obs, mod, j, 421, 422, 423, 424, 212, 12)
            # print(samples)
            model_score = time_basic_score(samples)
            scores.append(model_score)

            ax0.fill_between(Time_scale, hour_mean_np_s1[j, :] - hour_error_np_s1[j, :],
                                   hour_mean_np_s1[j, :] + hour_error_np_s1[j, :], alpha=0.75, edgecolor='#1B2ACC',
                                   facecolor='#089FFF',
                                   linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax0.set_title('DJF')
            ax1.fill_between(Time_scale, hour_mean_np_s2[j, :] - hour_error_np_s2[j, :],
                                   hour_mean_np_s2[j, :] + hour_error_np_s2[j, :], alpha=0.75, edgecolor='#1B2ACC',
                                   facecolor='#089FFF',
                                   linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax1.set_title('MAM')
            ax2.fill_between(Time_scale, hour_mean_np_s3[j, :] - hour_error_np_s3[j, :],
                                   hour_mean_np_s3[j, :] + hour_error_np_s3[j, :], alpha=0.75, edgecolor='#1B2ACC',
                                   facecolor='#089FFF',
                                   linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax2.set_title('JJA')
            ax3.fill_between(Time_scale, hour_mean_np_s4[j, :] - hour_error_np_s4[j, :],
                                   hour_mean_np_s4[j, :] + hour_error_np_s4[j, :], alpha=0.75, edgecolor='#1B2ACC',
                                   facecolor='#089FFF',
                                   linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax3.set_title('Annual: SON')
            # plt.suptitle(self.variable, fontsize=8)
            ax0.set_xlabel('Time'+ '(DJF)')
            ax0.set_ylabel(self.variable + '('+ self.h_unit_obs+')' )
            ax1.set_xlabel('Time' + '(MAM)')
            ax1.set_ylabel(self.variable + '('+ self.h_unit_obs+')')
            ax2.set_xlabel('Time' + '(JJA)')
            ax2.set_ylabel(self.variable + '('+ self.h_unit_obs+')')
            ax3.set_xlabel('Time'+ '(SON)')
            ax3.set_ylabel(self.variable + '('+ self.h_unit_obs+')' )

            ax0.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax1.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax2.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax3.legend(loc='upper right', shadow=False, fontsize='medium')
            # plt.tight_layout()
            fig0.savefig(self.filedir  + self.variable + '/' + ''.join(site) + '_' + 'day_' + self.variable + '.png')
            plt.close('all')
        scores = np.asarray(scores)
        return scores

    def plot_mean_and_dev_four_cycle(self, hour_np, day_np, month_np, season_np, mhour_np, mday_np, mmonth_np,
                                     mseason_np):
        # print(hour_np.shape, day_np.shape, month_np.shape, season_np.shape)

        hour_mean_np, hour_error_np = hour_np.mean(axis=1), hour_np.std(axis=1)
        day_mean_np, day_error_np = day_np.mean(axis=1), day_np.std(axis=1)
        month_mean_np, month_error_np = month_np.mean(axis=1), month_np.std(axis=1)
        season_mean_np, season_error_np = season_np.mean(axis=2).T, season_np.std(axis=2).T

        mhour_mean_np, mday_mean_np, mmonth_mean_np, mseason_mean_np = [], [], [], []
        m_xasix1, m_xasix2, m_xasix3, m_xasix4 = [],[],[],[]
        hour_time = np.arange(0, 24)
        day_time  = np.arange(1, 366)
        month_time = np.arange(1, 13)#np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov', 'Dec'])
        season_time  = np.arange(1, 5)#np.array(['DJF', 'MMA', 'JJA', 'SON'])
        for m in range(len(mhour_np)):
            mhour_mean_np.append(mhour_np[m].mean(axis=1))
            mday_mean_np.append(mday_np[m].mean(axis=1))
            mmonth_mean_np.append(mmonth_np[m].mean(axis=1))
            mseason_mean_np.append(mseason_np[m].mean(axis=2).T)
            m_xasix1.append(hour_time)
            m_xasix2.append(day_time)
            m_xasix3.append(month_time)
            m_xasix4.append(season_time)
            """ plot the mean and deviation timeseries  """
        # print(mseason_mean_np)
        obs = [hour_mean_np, day_mean_np, month_mean_np, season_mean_np, hour_time,
               day_time, month_time, season_time]
        mod = [mhour_mean_np, mday_mean_np, mmonth_mean_np, mseason_mean_np, m_xasix1, m_xasix2, m_xasix3,
               m_xasix4]
        scores = []
        for j, site in enumerate(self.sitename):
            # if j==1:
            #     break
            # print(j, site)
            fig1 = plt.figure(figsize=(15, 18))
            print('Process on four_cycles_' + ''.join(site) + '_No.' + str(j) + '!')

            ''' Observations data need to use masked '''
            # fig1, ax0, ax1, ax2, ax3, samples = plot_categories(fig1, obs, mod, j)
            fig1, ax0, ax1, ax2, ax3, samples = plot_new_categories(fig1, obs, mod, j, 421, 422, 423, 424, 212, 12)

            model_score = time_basic_score(samples)
            scores.append(model_score)

            ax0.fill_between(hour_time, hour_mean_np[j, :] - hour_error_np[j, :],
                                hour_mean_np[j, :] + hour_error_np[j, :], alpha=0.2, edgecolor='#1B2ACC',
                                facecolor='#089FFF',
                                linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax0.set_title('Hourly mean and standard deviation')
            ax1.fill_between(day_time, day_mean_np[j, :] - day_error_np[j, :],
                                day_mean_np[j, :] + day_error_np[j, :], alpha=0.2, edgecolor='#1B2ACC',
                                facecolor='#089FFF',
                                linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax1.set_title('Daily mean and standard deviation')
            ax2.fill_between(month_time, month_mean_np[j, :] - month_error_np[j, :],
                                month_mean_np[j, :] + month_error_np[j, :], alpha=0.2, edgecolor='#1B2ACC',
                                facecolor='#089FFF',
                                linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax2.set_title('Monthly mean and standard deviation')
            ax3.fill_between(season_time, season_mean_np[j, :] - season_error_np[j, :],
                                season_mean_np[j, :] + season_error_np[j, :], alpha=0.2, edgecolor='#1B2ACC',
                                facecolor='#089FFF',
                                linewidth=0.5, linestyle='dashdot', antialiased=True)
            # ax3.set_title('Yearly mean and standard deviation')

            # plt.suptitle(self.variable, fontsize=8)
            ax0.set_xlabel('Hour of a day')
            ax0.set_ylabel(self.variable + '('+ self.h_unit_obs+')')
            ax1.set_xlabel('Day of a year')
            ax1.set_ylabel(self.variable + '('+ self.d_unit_obs+')')
            ax2.set_xlabel('Month of a year')
            ax2.set_ylabel(self.variable + '('+ self.m_unit_obs+')')
            ax3.set_xlabel('Season of a year')
            ax3.set_ylabel(self.variable + '('+ self.m_unit_obs+')')
            ax0.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax1.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax2.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax3.legend(loc='upper right', shadow=False, fontsize='medium')
            # plt.tight_layout()
            fig1.savefig(self.filedir  + self.variable + '/' + ''.join(site) + '_time_series_' + self.variable + '.png')
            plt.close('all')
        scores = np.asarray(scores)
        return scores

    def plot_season_cycle(self, o_seasonly_data, m_seasonly_data):

        mhour_mean_np_s1, mhour_mean_np_s2, mhour_mean_np_s3, mhour_mean_np_s4 = [], [], [], []
        m_xasix = []
        year =len(o_seasonly_data[0, 0, :])
        for m in range(len(m_seasonly_data)):
            mhour_mean_np_s1.append(m_seasonly_data[m][0,:,:])
            mhour_mean_np_s2.append(m_seasonly_data[m][1,:,:])
            mhour_mean_np_s3.append(m_seasonly_data[m][2,:,:])
            mhour_mean_np_s4.append(m_seasonly_data[m][3,:,:])
            m_xasix.append(np.arange(0, year))

        obs = [o_seasonly_data[0, :, :], o_seasonly_data[1, :, :], o_seasonly_data[2, :, :], o_seasonly_data[3, :, :],np.arange(0, year), np.arange(0, year),
               np.arange(0,year), np.arange(0, year)]
        mod = [mhour_mean_np_s1, mhour_mean_np_s2, mhour_mean_np_s3, mhour_mean_np_s4, m_xasix, m_xasix, m_xasix,
               m_xasix]
        scores = []
        for j, site in enumerate(self.sitename):
            print('Process on season_cycle_' + ''.join(site) + '_No.' + str(j) + '!')
            fig5 = plt.figure(figsize=(15, 18))
            # fig5, ax0, ax1, ax2, ax3, samples = plot_categories(fig5, obs, mod, j)
            fig5, ax0, ax1, ax2, ax3, samples = plot_new_categories(fig5, obs, mod, j, 421, 422, 423, 424, 212, 3)

            model_score = time_basic_score(samples)
            scores.append(model_score)

            ax0.set_ylabel(self.variable + '(' + self.m_unit_obs+')')
            ax0.set_xlabel('Year' + 'DJF')
            ax1.set_ylabel(self.variable + '(' + self.m_unit_obs+')')
            ax1.set_xlabel('Year'+ 'MAM')
            ax2.set_ylabel(self.variable + '(' + self.m_unit_obs+')')
            ax2.set_xlabel('Year'+ 'JJA')
            ax3.set_ylabel(self.variable + '(' + self.m_unit_obs+')')
            ax3.set_xlabel('Year' + 'SON')
            ax0.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax1.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax2.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax3.legend(loc='upper right', shadow=False, fontsize='medium')
            # plt.tight_layout()
            fig5.savefig(self.filedir + self.variable + '/' + ''.join(site) + '_season_' + self.variable + '.png')
            plt.close('all')
        scores = np.asarray(scores)
        return scores

def cycle_analysis(variable_name, h_unit_obs, d_unit_obs,m_unit_obs, y_unit_obs, h_site_name_obs, filedir, o_h_s1, o_h_s2, o_h_s3, o_h_s4, m_h_s1, m_h_s2, m_h_s3, m_h_s4, o_hour_data, o_daily_data, o_monthly_data, o_seasonly_data, m_hour_data, m_daily_data, m_monthly_data, m_seasonly_data):

    f1 = cycle_post(variable_name, h_site_name_obs, filedir, h_unit_obs, d_unit_obs,m_unit_obs, y_unit_obs)
    scores_day_cycle = f1.plot_days_cycle_for_each_site(o_h_s1, o_h_s2, o_h_s3, o_h_s4, m_h_s1, m_h_s2, m_h_s3, m_h_s4)
    scores_fourcycle =f1.plot_mean_and_dev_four_cycle(o_hour_data, o_daily_data, o_monthly_data, o_seasonly_data, m_hour_data, m_daily_data, m_monthly_data, m_seasonly_data)
    scores_seassoncycle =f1.plot_season_cycle(o_seasonly_data, m_seasonly_data)

    return scores_day_cycle, scores_fourcycle, scores_seassoncycle

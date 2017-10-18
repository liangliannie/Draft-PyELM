from taylorDiagram import plot_daylor_graph
import matplotlib.pyplot as plt
import pyhht
import waipy
import numpy as np
from pyhht.visualization import plot_imfs
plt.rcParams.update({'font.size': 12})
fontsize = 14

def plot_imfs(signal, imfs, time_samples = None, fig=None):

    '''Author jaidevd https://github.com/jaidevd/pyhht/blob/dev/pyhht/visualization.py'''
    '''Original function from pyhht, but without plt.show()'''
    n_imfs = imfs.shape[0]
    # print(np.abs(imfs[:-1, :]))
    # axis_extent = max(np.max(np.abs(imfs[:-1, :]), axis=0))

    # Plot original signal
    ax = plt.subplot(n_imfs + 1, 1, 1)
    ax.plot(time_samples, signal)
    ax.axis([time_samples[0], time_samples[-1], signal.min(), signal.max()])
    ax.tick_params(which='both', left=False, bottom=False, labelleft=False,
                   labelbottom=False)
    ax.grid(False)
    ax.set_ylabel('Signal')
    ax.set_title('Empirical Mode Decomposition')

    # Plot the IMFs
    for i in range(n_imfs - 1):
        # print(i + 2)
        ax = plt.subplot(n_imfs + 1, 1, i + 2)
        ax.plot(time_samples, imfs[i, :])
        # ax.axis([time_samples[0], time_samples[-1], -axis_extent, axis_extent])
        ax.tick_params(which='both', left=False, bottom=False, labelleft=False,
                       labelbottom=False)
        ax.grid(False)
        ax.set_ylabel('imf' + str(i + 1))

    # Plot the residue
    ax = plt.subplot(n_imfs + 1, 1, n_imfs + 1)
    ax.plot(time_samples, imfs[-1, :], 'r')
    ax.axis('tight')
    ax.tick_params(which='both', left=False, bottom=False, labelleft=False,
                   labelbottom=False)
    ax.grid(False)
    ax.set_ylabel('res.')
    return ax

class spectrum_post(object):

    def __init__(self, filedir, h_site_name_obs, day_obs, day_mod, variable_name):
        [d_obs, d_t_obs, d_unit_obs] = day_obs
        [d_mod, d_t_mod, d_unit_mod] = day_mod
        self.d_obs = d_obs
        self.d_mod = d_mod
        self.d_t_obs = d_t_obs
        self.d_unit_obs = d_unit_obs
        self.sitename = h_site_name_obs
        self.variable = variable_name
        self.filedir = filedir

    def plot_imf(self):
        d_obs = self.d_obs
        d_mod = self.d_mod
        d_t_obs = self.d_t_obs
        scores = []
        for j, site in enumerate(self.sitename):
            print('Process on IMF_' + ''.join(site) + '_No.' + str(j) + '!')

            decomposer1 = pyhht.emd.EmpiricalModeDecomposition(d_obs[j, :].compressed())
            # print(decomposer)
            # print(d_obs[j, :])
            # print('*************************')
            # print(d_mod[0][j, :])
            time = d_t_obs[~d_obs[j, :].mask]

            imfs1 = decomposer1.decompose()

            fig6 = plt.figure(figsize=(10, 5))
            s = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
            col = ['b', 'g', 'c', 'm', 'y',  'k', 'w','b', 'g', 'c', 'm', 'y',  'k', 'w']
            # name=[]
            # label=[]
            if len(imfs1) >= 3:
                ax6 = fig6.add_subplot(1, 2, 1)
                ax6.plot(time, imfs1[len(imfs1) - 1], 'k.', label="Observed")
                ax6.plot(time, (imfs1[len(imfs1) - 2] + imfs1[len(imfs1) - 1]), 'k.',
                         time, (imfs1[len(imfs1) - 3] + imfs1[len(imfs1) - 1] + imfs1[len(imfs1) - 2]), 'k.')
                # d_t_obs, d_obs[j, :], 'b'
                # name.append(ob1)
                # label.append('Oobserved')
            data1 = imfs1[len(imfs1) - 1]
            models1 = []
            for m in range(len(d_mod)):
                decomposer2 = pyhht.emd.EmpiricalModeDecomposition(d_mod[m][j, :][~d_obs[j, :].mask])
                imfs2 = decomposer2.decompose()
                # time = d_t_obs[~d_mod[m][j, :].mask]
                if len(imfs2) >= 3:
                    ax6.plot(time, imfs2[len(imfs2) - 1], col[m]+s[0],label= "Model "+str(m+1))
                    ax6.plot(time, (imfs2[len(imfs2) - 2] + imfs2[len(imfs2) - 1]), col[m]+s[1],
                             time, (imfs2[len(imfs2) - 3] + imfs2[len(imfs2) - 1] + imfs2[len(imfs2) - 2]), col[m]+s[2])
                    # d_t_obs, d_mod[m][j, :], 'b'
                # name.append(mod2)
                # label.append("Model"+str(m))

                models1.append(imfs2[len(imfs2) - 1])
            ax6.set_xlabel('Time', fontsize=fontsize)
            ax6.set_ylabel(''+self.variable + '('+ self.d_unit_obs+')', fontsize=fontsize)
            ax6.legend(loc='upper right', shadow=False, fontsize='medium')

            plot_daylor_graph(data1, models1, fig6, 122)
            # plt.legend(name, label)
            fig6.savefig(self.filedir  + self.variable + '/' + ''.join(site) + '_' + 'IMF' + '_' + self.variable + '.png')
            plt.close('all')
        return scores

    def plot_decomposer_imf(self):
        d_obs = self.d_obs
        d_mod = self.d_mod
        d_t_obs = self.d_t_obs
        scores = []

        for j, site in enumerate(self.sitename):
            print('Process on Decomposer_IMF_' + ''.join(site) + '_No.' + str(j) + '!')

            fig6 = plt.figure(figsize=(15*len(d_mod), 25))

            time = d_t_obs[~d_obs[j, :].mask]

            decomposer= pyhht.emd.EmpiricalModeDecomposition(d_obs[j, :].compressed())
            imfs = decomposer.decompose()

            n_imfs = imfs.shape[0]
            ax = fig6.add_subplot(n_imfs + 1, (len(d_mod) +1), 1)
            ax.plot(time, d_obs[j, :].compressed())
            ax.set_ylabel('Signal')
            for i in range(n_imfs - 1):
                ax = fig6.add_subplot(n_imfs + 1, (len(d_mod) +1),  (i+1)*(len(d_mod) +1) + 1)
                ax.plot(time, imfs[i, :])
                ax.set_ylabel('imf' + str(i + 1))
            ax = fig6.add_subplot(n_imfs + 1, (len(d_mod) +1), n_imfs*(len(d_mod) +1) + 1)
            ax.plot(time, imfs[-1, :], 'r')
            ax.set_ylabel('res.')

            for m in range(len(d_mod)):
                decomposer=pyhht.emd.EmpiricalModeDecomposition(d_mod[m][j, :][~d_obs[j, :].mask])
                imfs = decomposer.decompose()
                n_imfs = imfs.shape[0]

                ax = fig6.add_subplot(n_imfs + 1, (len(d_mod) + 1), m+2)
                ax.plot(time, d_mod[m][j, :][~d_obs[j, :].mask])
                ax.set_ylabel('Model' + str(m+1))
                for i in range(n_imfs - 1):
                    ax = fig6.add_subplot(n_imfs + 1, (len(d_mod) + 1), (i + 1) * (len(d_mod) + 1) +m+2)
                    ax.plot(time, imfs[i, :])
                    ax.set_ylabel('imf' + str(i + 1))
                ax = fig6.add_subplot(n_imfs + 1, (len(d_mod) + 1), n_imfs * (len(d_mod) + 1) +m+2)
                ax.plot(time, imfs[-1, :], 'r')
                ax.set_ylabel('res.')
            fig6.savefig(self.filedir + self.variable + '/' + ''.join(
                site) + 'observed' + '_Decompose_IMF_' + self.variable + '.png')
            # imfs1 = decomposer1.decompose()
            #
            # plot_imfs(d_obs[j, :].compressed(), imfs1, time, fig6)
            #
            #
            #
            #     imfs2 = decomposer2.decompose()
            #     fig7 = plt.figure(figsize=(8, 8))
            #     # if j == 17:
            #     #     print(d_mod[m][j, :][~d_obs[j, :].mask])
            #         # break
            #     plot_imfs(d_mod[m][j, :][~d_obs[j, :].mask], imfs2, time, fig7)
            #     fig7.savefig(self.filedir  + self.variable + '/' + ''.join(site) + 'model' + str(m) + '_Decompose_IMF_' + self.variable + '.png')
            plt.close('all')
        return scores

    def plot_wavelet(self):
        d_obs = self.d_obs
        d_mod = self.d_mod
        d_t_obs = self.d_t_obs

        """ plot data wavelet """
        scores = []
        for j, site in enumerate(self.sitename):
            print('Process on Wavelet_' + ''.join(site) + '_No.' + str(j) + '!')
            fig3 = plt.figure(figsize=(8, 8))
            # ax3 = fig6.add_subplot(1, 2, 1)
            # fig3, ax3 = plt.subplots()
            data = d_obs[j, :].compressed()
            time_data = d_t_obs[~d_obs[j, :].mask]
            # time_data = d_t_obs
            result = waipy.cwt(data, 1, 1, 0.125, 2, 4 / 0.125, 0.72, 6, mother='Morlet', name='Data')
            waipy.wavelet_plot('Data', time_data, data, 0.03125, result, fig3)
            fig3.savefig(self.filedir + self.variable + '/' + ''.join(site) + '_Wavelet_' + self.variable + '.png')
            for m in range(len(d_mod)):
                fig4 = plt.figure(figsize=(8, 8))
                data = d_mod[m][j, :][~d_obs[j, :].mask] - d_obs[j, :].compressed()
                # time_data = d_mod[m][j, :]
                result = waipy.cwt(data, 1, 1, 0.125, 2, 4 / 0.125, 0.72, 6, mother='Morlet', name='Data')
                waipy.wavelet_plot('Data', time_data, data, 0.03125, result, fig4)
                fig4.savefig(self.filedir  + self.variable + '/' + ''.join(site) + 'model' + str(m) + '_wavelet_' + self.variable + '.png')
            plt.close('all')
        return scores


    def plot_spectrum(self):
        import waipy, math
        import numpy as np
        import matplotlib.pyplot as plt
        d_obs = self.d_obs
        d_mod = self.d_mod
        d_t_obs = self.d_t_obs
        scores = []
        """ Plot global wavelet spectrum """
        for j, site in enumerate(self.sitename):
            print('Process on Spectrum_' + ''.join(site) + '_No.' + str(j) + '!')
            data = d_obs[j, :].compressed()
            result = waipy.cwt(data, 1, 1, 0.125, 2, 4 / 0.125, 0.72, 6, mother='Morlet', name='Data')
            fig4 = plt.figure(figsize=(8, 8))
            ax4 = fig4.add_subplot(1, 1, 1)
            # f1, sxx1 = waipy.fft(data)
            # ax.plot(np.log2(1 / f1 * result['dt']), sxx1, 'red', label='Fourier spectrum')
            # plt.suptitle(self.variable + ' ( ' + self.d_unit_obs + ' )', fontsize=8)
            ax4.plot(np.log2(result['period']), result['global_ws'], 'k-', label='Wavelet spectrum')
            ax4.plot(np.log2(result['period']), result['global_signif'], 'r--', label='95% confidence spectrum')

            for m in range(len(d_mod)):
                data = d_mod[m][j, :][~d_obs[j, :].mask]
                result_temp = waipy.cwt(data, 1, 1, 0.125, 2, 4 / 0.125, 0.72, 6, mother='Morlet', name='Data')
                ax4.plot(np.log2(result_temp['period']), result_temp['global_ws'], label='Model' + str(m))

            ax4.legend(loc=0)
            ax4.set_ylim(0, 1.25 * np.max(result['global_ws']))
            ax4.set_ylabel('Power', fontsize=12)
            ax4.set_title('Global Wavelet Spectrum', fontsize=12)
            yt = range(int(np.log2(result['period'][0])), int(
                np.log2(result['period'][-1]) + 1))  # create the vector of periods
            Yticks = [float(math.pow(2, p)) for p in yt]  # make 2^periods
            ax4.set_xticks(yt)
            ax4.set_xticklabels(Yticks)
            ax4.set_xlim(xmin=(np.log2(np.min(result['period']))), xmax=(np.log2(np.max(result['period']))))
            plt.tight_layout()
            fig4.savefig(self.filedir  + self.variable + '/' + ''.join(site) + '_spectrum_' + self.variable + '.png')
            plt.close('all')
        return scores


    def plot_taylor_gram(self):
        d_obs = self.d_obs
        d_mod = self.d_mod
        d_t_obs = self.d_t_obs
        scores = []
        """  Taylor diagram """
        for j, site in enumerate(self.sitename):
            print('Process on Taylor_' + ''.join(site) + '_No.' + str(j) + '!')
            data1 = d_obs[j, :].compressed()
            models1 = []
            fig7 = plt.figure(figsize=(8, 8))
            for m in range(len(d_mod)):
                models1.append(d_mod[m][j, :][~d_obs[j, :].mask])

            # print(data1.shape, models1[0].shape)
            plot_daylor_graph(data1, models1, fig7, 111)
            fig7.savefig(self.filedir + self.variable + '/' + ''.join(site) + '_taylor_' + self.variable + '.png')
            plt.close('all')
        return scores



def spectrum_analysis(filedir,h_site_name_obs, day_obs, day_mod, variable_name):
    f2 = spectrum_post(filedir,h_site_name_obs, day_obs, day_mod, variable_name)
    scores_imf = f2.plot_imf()
    scores_decomposeimf = f2.plot_decomposer_imf()
    score_wavelet = f2.plot_wavelet()
    score_spectrum = f2.plot_spectrum()
    score_taylor_gram = f2.plot_taylor_gram()
    return scores_imf, scores_decomposeimf, score_wavelet, score_spectrum, score_taylor_gram
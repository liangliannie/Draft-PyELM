import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
import os
from netCDF4 import Dataset


def read_file(Root_Dir, name):
    return Dataset(Root_Dir + name)

def data_extract(o, variable):
    ''' Read a certain variable for obs return np.masked.array for only data,
     time is not masked '''
    data = o.variables[variable][:]
    unit = o.variables[variable].units
    time = o.variables['time'][:]
    data = np.ma.masked_invalid(data)
    return data, time, unit

def models_data_extract(o, m, variable):
    ''' Read multiple models for a certain variable, return list of models data,
     model data is masked based on the observed data '''
    data1, time1, unit1 = [],[],[]
    for i in range(len(m)):
        data, time, unit = data_extract(m[i], variable)
        np.ma.masked_where(np.ma.getmask(o), data)
        test = True
        ''' The models should be changed back here '''
        if test:
            data = o + np.random.rand(data.shape[0],data.shape[1])*0.00000005
        data1.append(data)
        time1.append(time)
        unit1.append(unit)
    return data1, time1, unit1


def binPlot(X, Y, label, ax=None, numBins=8, xmin=None, xmax=None):

    '''  Adopted from  http://peterthomasweir.blogspot.com/2012/10/plot-binned-mean-and-mean-plusminus-std.html '''
    if xmin is None:
        xmin = X.min()
    if xmax is None:
        xmax = X.max()
    bins = np.linspace(xmin, xmax, numBins + 1)
    xx = np.array([np.mean((bins[binInd], bins[binInd + 1])) for binInd in range(numBins)])
    yy = np.array([np.mean(Y[(X > bins[binInd]) & (X <= bins[binInd + 1])]) for binInd in range(numBins)])
    yystd = np.array([np.std(Y[(X > bins[binInd]) & (X <= bins[binInd + 1])]) for binInd in range(numBins)])
    ax.plot(xx, yy, label=label)
    ax.errorbar(xx, yy, yerr=yystd, fmt='o', elinewidth=2, capthick=1, capsize=4, color='k')
    # patchHandle.set_facecolor([.8, .8, .8])
    # patchHandle.set_edgecolor('none')
    return xx, yy, yystd

def plot(variable1, variable2, ax0, ax1,label):
    x, y = variable1, variable2
    ir = IsotonicRegression()
    y_ = ir.fit_transform(x, y)
    lr = LinearRegression()
    lr.fit(x[:, np.newaxis], y)  # x needs to be 2d for LinearRegression
    # #############################################################################
    # Plot result
    segments = [[[i, y[i]], [i, y_[i]]] for i in range(len(x))]
    lc = LineCollection(segments, zorder=0)
    lc.set_array(np.ones(len(y)))
    lc.set_linewidths(0.5 * np.ones(len(x)))
    if label== 'Observed':
        ax0.plot(x, y, 'k.', markersize=12, label=label)
        # ax8[number].plot(x, y_, 'g.-', markersize=12)
        ax0.plot(x, lr.predict(x[:, np.newaxis]), 'k-',label='Linear' + label)
    else:
        ax0.plot(x, y, '.', markersize=12, label=label)
        # ax8[number].plot(x, y_, 'g.-', markersize=12)
        ax0.plot(x, lr.predict(x[:, np.newaxis]), '-',label='Linear' + label)
    # plt.gca().add_collection(lc)
    binPlot(x, y, label, ax1, 15)


# site_name = ['AU-Tum', 'AT-Neu']
def plot_all_response(filedir,h_site_name_obs1, h_o, d_o, m_o, y_o, h_models, d_models, m_models, y_models, variable_list1, variable_list2):
    directory = filedir + 'response' + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    scores = []
    for i in range(len(variable_list1)):
        variable1, variable2 = variable_list1[i], variable_list2[i]
        h_obs1, h_t_obs1, h_unit_obs1 = data_extract(h_o, variable1)
        h_mod1, h_t_mod1, h_unit_mod1 = models_data_extract(h_obs1, h_models, variable1)
        d_obs1, d_t_obs1, d_unit_obs1 = data_extract(d_o, variable1)
        d_mod1, d_t_mod1, d_unit_mod1 = models_data_extract(d_obs1, d_models, variable1)
        m_obs1, m_t_obs1, m_unit_obs1 = data_extract(m_o, variable1)
        m_mod1, m_t_mod1, m_unit_mod1 = models_data_extract(m_obs1, m_models, variable1)
        y_obs1, y_t_obs1, y_unit_obs1 = data_extract(y_o, variable1)
        y_mod1, y_t_mod1, y_unit_mod1 = models_data_extract(y_obs1, y_models, variable1)

        h_obs2, h_t_obs2, h_unit_obs2 = data_extract(h_o, variable2)
        h_mod2, h_t_mod2, h_unit_mod2 = models_data_extract(h_obs2, h_models, variable2)
        d_obs2, d_t_obs2, d_unit_obs2 = data_extract(d_o, variable2)
        d_mod2, d_t_mod2, d_unit_mod2 = models_data_extract(d_obs2, d_models, variable2)
        m_obs2, m_t_obs2, m_unit_obs2 = data_extract(m_o, variable2)
        m_mod2, m_t_mod2, m_unit_mod2 = models_data_extract(m_obs2, m_models, variable2)
        y_obs2, y_t_obs2, y_unit_obs2 = data_extract(y_o, variable2)
        y_mod2, y_t_mod2, y_unit_mod2 = models_data_extract(y_obs2, y_models, variable2)


        h_mod1.append(h_obs1), d_mod1.append(d_obs1), m_mod1.append(m_obs1), y_mod1.append(y_obs1)
        h_mod2.append(h_obs2), d_mod2.append(d_obs2), m_mod2.append(m_obs2), y_mod2.append(y_obs2)

        for j, site in enumerate(h_site_name_obs1):
            print('Process on response_' + ''.join(site) + '_No.' + str(j) + '!')
            fig8 = plt.figure(figsize=(9, 9))
            fig9 = plt.figure(figsize=(9, 9))
            ax80 = fig8.add_subplot(411)
            ax90 = fig9.add_subplot(411)
            ax81 = fig8.add_subplot(412)
            ax91 = fig9.add_subplot(412)
            ax82 = fig8.add_subplot(413)
            ax92 = fig9.add_subplot(413)
            ax83 = fig8.add_subplot(414)
            ax93 = fig9.add_subplot(414)
            for m in range(len(h_mod1)):
                # print(m)
                h1, h2, d1, d2 = h_mod1[m][j, :], h_mod2[m][j, :], d_mod1[m][j, :], d_mod2[m][j, :]
                m1, m2, y1, y2 = m_mod1[m][j, :], m_mod2[m][j, :], y_mod1[m][j, :], y_mod2[m][j, :]
                # print(h1.mask, h2.mask)
                mask1 = h1.mask | h2.mask
                mask2 = d1.mask | d2.mask
                mask3 = m1.mask | m2.mask
                mask4 = y1.mask | y2.mask
                h1 = np.ma.masked_where(mask1, h1)
                h2 = np.ma.masked_where(mask1, h2)
                d1 = np.ma.masked_where(mask2, d1)
                d2 = np.ma.masked_where(mask2, d2)
                m1 = np.ma.masked_where(mask3, m1)
                m2 = np.ma.masked_where(mask3, m2)
                y1 = np.ma.masked_where(mask4, y1)
                y2 = np.ma.masked_where(mask4, y2)
                # print(h1.mask, h2.mask)
                # print(h1.compressed().shape, h2.compressed().shape)
                if m == len(h_mod1)-1:
                    plot(h1.compressed(), h2.compressed(), ax80, ax90, label= 'Observed')
                    plot(d1.compressed(), d2.compressed(), ax81, ax91, label= 'Observed')
                    plot(m1.compressed(), m2.compressed(), ax82, ax92, label= 'Observed')
                    plot(y1.compressed(), y2.compressed(), ax83, ax93, label= 'Observed')
                else:
                    plot(h1.compressed(), h2.compressed(), ax80, ax90,label= "Model "+str(m+1))
                    plot(d1.compressed(), d2.compressed(), ax81, ax91,label= "Model "+str(m+1))
                    plot(m1.compressed(), m2.compressed(), ax82, ax92,label= "Model "+str(m+1))
                    plot(y1.compressed(), y2.compressed(), ax83, ax93,label= "Model "+str(m+1))
            # plt.suptitle(variable1 + 'vs' + variable2, fontsize=8)
            ax80.set_xlabel(variable1+' (' + h_unit_obs1+' )')
            ax81.set_xlabel(variable1+' (' + d_unit_obs1+' )')
            ax82.set_xlabel(variable1+' (' + m_unit_obs1+' )')
            ax83.set_xlabel(variable1+' (' + y_unit_obs1+' )')
            ax80.set_ylabel(variable2+' (' + h_unit_obs2+' )')
            ax81.set_ylabel(variable2+' (' + d_unit_obs2+' )')
            ax82.set_ylabel(variable2+' (' + m_unit_obs2+' )')
            ax83.set_ylabel(variable2+' (' + y_unit_obs2+' )')

            ax90.set_xlabel(variable1+' (' + h_unit_obs1+' )')
            ax91.set_xlabel(variable1+' (' + d_unit_obs1+' )')
            ax92.set_xlabel(variable1+' (' + m_unit_obs1+' )')
            ax93.set_xlabel(variable1+' (' + y_unit_obs1+' )')
            ax90.set_ylabel(variable2+' (' + h_unit_obs2+' )')
            ax91.set_ylabel(variable2+' (' + d_unit_obs2+' )')
            ax92.set_ylabel(variable2+' (' + m_unit_obs2+' )')
            ax93.set_ylabel(variable2+' (' + y_unit_obs2+' )')
            ax80.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax81.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax82.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax83.legend(loc='upper right', shadow=False, fontsize='medium')
            ax90.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax91.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax92.legend(loc='upper right', shadow=False, fontsize='medium')
            # ax93.legend(loc='upper right', shadow=False, fontsize='medium')
            fig8.savefig(filedir + 'response' + '/' + ''.join(site) +'_' + variable1 + '_vs_' + variable2 + '_Response' + '.png')
            fig9.savefig(filedir + 'response' + '/' + ''.join(site) +'_' + variable1 + '_vs_' + variable2 + '_Response_Bin' + '.png')
            plt.close('all')
        return scores
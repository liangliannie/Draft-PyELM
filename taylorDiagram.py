#!/usr/bin/env python
# Copyright: This document has been placed in the public domain.

"""
Taylor diagram (Taylor, 2001) test implementation.
http://www-pcmdi.llnl.gov/about/staff/Taylor/CV/Taylor_diagram_primer.htm
"""

__version__ = "Time-stamp: <2012-02-17 20:59:35 ycopin>"
__author__ = "Yannick Copin <yannick.copin@laposte.net>"

import numpy as NP
import matplotlib.pyplot as PLT


class TaylorDiagram(object):
    """Taylor diagram: plot model standard deviation and correlation
    to reference (data) sample in a single-quadrant polar plot, with
    r=stddev and theta=arccos(correlation).
    """

    def __init__(self, refstd, fig=None, rect=111, label='_', ax=None, ref_times=5):
        """Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using mpl_toolkits.axisartist.floating_axes. refstd is
        the reference standard deviation to be compared to.
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF

        self.refstd = refstd  # Reference standard deviation

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = NP.concatenate((NP.arange(10) / 10., [0.95, 0.99]))
        tlocs = NP.arccos(rlocs)  # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)  # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str, rlocs))))

        # Standard deviation axis extent
        self.smin = 0
        self.smax = ref_times * self.refstd

        ghelper = FA.GridHelperCurveLinear(tr,
                                           extremes=(0, NP.pi / 2,  # 1st quadrant
                                                     self.smin, self.smax),
                                           grid_locator1=gl1,
                                           tick_formatter1=tf1,
                                           )
        if ax is None:
            if fig is None:
                fig = PLT.figure()
            ax = FA.FloatingSubplot(fig, rect, grid_helper=ghelper)
            fig.add_subplot(ax)

        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")

        ax.axis["left"].set_axis_direction("bottom")  # "X axis"
        ax.axis["left"].label.set_text("Normalized standard deviation")

        ax.axis["right"].set_axis_direction("top")  # "Y axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction("left")

        ax.axis["bottom"].set_visible(False)  # Useless

        # Contours along standard deviations
        ax.grid(True)

        self._ax = ax  # Graphical axes
        self.ax = ax.get_aux_axes(tr)  # Polar coordinates

        # Add reference point and stddev contour
        # print "Reference std:", self.refstd
        l, = self.ax.plot([0], self.refstd, 'k*',
                          ls='', ms=10, label=label)
        t = NP.linspace(0, NP.pi / 2)
        r = NP.zeros_like(t) + self.refstd
        self.ax.plot(t, r, 'k--', label='_')

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]

    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """Add sample (stddev,corrcoeff) to the Taylor diagram. args
        and kwargs are directly propagated to the Figure.plot
        command."""

        l, = self.ax.plot(NP.arccos(corrcoef), stddev,
                          *args, **kwargs)  # (theta,radius)
        self.samplePoints.append(l)

        return l

    def add_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours."""

        rs, ts = NP.meshgrid(NP.linspace(self.smin, self.smax),
                             NP.linspace(0, NP.pi / 2))
        # Compute centered RMS difference
        rms = NP.sqrt(self.refstd ** 2 + rs ** 2 - 2 * self.refstd * rs * NP.cos(ts))

        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)

        return contours


def plot_daylor_graph(data, models, fig, rect):
    # Reference dataset

    refstd_un = data.std(ddof=1)  # Reference standard deviation
    normalize = True


    # Models
    # Compute stddev and correlation coefficient of models
    if normalize:
        # print([[m.std(ddof=1)/refstd_un, NP.ma.corrcoef(data, m)[0, 1]] for m in models])
        samples = NP.array([[m.std(ddof=1)/refstd_un, abs(NP.ma.corrcoef(data, m)[0, 1])] for m in models])
        # print(samples)
        refstd = 1

    # fig = PLT.figure(figsize=(10, 4))

    # ax1 = fig.add_subplot(1, 2, 1, xlabel='X', ylabel='Y')
    # Taylor diagram
    dia = TaylorDiagram(refstd, fig=fig, rect=rect, label="Reference")
    colors = PLT.matplotlib.cm.jet(NP.linspace(0, 1, len(samples)))

    # ax1.plot(x, data, 'ko', label='Data')
    # for i, m in enumerate(models):
    #     ax1.plot(x, m, c=colors[i], label='Model %d' % (i + 1))
    # ax1.legend(numpoints=1, prop=dict(size='small'), loc='best')

    # Add samples to Taylor diagram
    marker = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd',
              '|', '_', '.', ',']

    for i, (stddev, corrcoef) in enumerate(samples):
        dia.add_sample(stddev, corrcoef, marker=marker[i], ls='', c=colors[i], markersize=20,
                       label="Model %d" % (i + 1))

    # Add RMS contours, and label them
    contours = dia.add_contours(colors='0.5')
    PLT.clabel(contours, inline=1, fontsize=10)

    # Add a figure legend
    fig.legend(dia.samplePoints,
               [p.get_label() for p in dia.samplePoints],
               numpoints=1, prop=dict(size='large'), loc='upper right')

    return fig, samples


def plot_daylor_graph_new(data1, data2, data3, data4, model1, model2, model3, model4, fig, rect, ref_times):
    # Reference dataset

    refstd_un1 = data1.std(ddof=1)  # Reference standard deviation
    refstd_un2 = data2.std(ddof=1)  # Reference standard deviation
    refstd_un3 = data3.std(ddof=1)  # Reference standard deviation
    refstd_un4 = data4.std(ddof=1)  # Reference standard deviation

    normalize = True


    # Models
    # Compute stddev and correlation coefficient of models
    if normalize:
        # print([[m.std(ddof=1)/refstd_un, NP.ma.corrcoef(data, m)[0, 1]] for m in models])
        samples1 = NP.array([[m.std(ddof=1)/refstd_un1, abs(NP.ma.corrcoef(data1, m)[0, 1])] for m in model1])
        samples2 = NP.array([[m.std(ddof=1)/refstd_un2, abs(NP.ma.corrcoef(data2, m)[0, 1])] for m in model2])
        samples3 = NP.array([[m.std(ddof=1)/refstd_un3, abs(NP.ma.corrcoef(data3, m)[0, 1])] for m in model3])
        samples4 = NP.array([[m.std(ddof=1)/refstd_un4, abs(NP.ma.corrcoef(data4, m)[0, 1])] for m in model4])

        # print(samples)
        refstd = 1

    # fig = PLT.figure(figsize=(10, 4))

    # ax1 = fig.add_subplot(1, 2, 1, xlabel='X', ylabel='Y')
    # Taylor diagram
    dia = TaylorDiagram(refstd, fig=fig, label="Reference", rect=rect, ref_times=ref_times)
    colors = PLT.matplotlib.cm.jet(NP.linspace(0, 1, 4))
    marker = ['o', 'v', '^', '<', '>', '1', '2', '3','4', '8','s','p','P','*','h','H','+','x','X','D','d','|','_', '.', ',']
    # ax1.plot(x, data, 'ko', label='Data')
    # for i, m in enumerate(models):
    #     ax1.plot(x, m, c=colors[i], label='Model %d' % (i + 1))
    # ax1.legend(numpoints=1, prop=dict(size='small'), loc='best')
    markersize = 20
    # Add samples to Taylor diagram
    for i, (stddev, corrcoef) in enumerate(samples1):
        dia.add_sample(stddev, corrcoef, marker = marker[i], ls='', c=colors[0], markersize=markersize,
                    label="Hourly Model %d" % (i + 1))
    for i, (stddev, corrcoef) in enumerate(samples2):
        dia.add_sample(stddev, corrcoef, marker= marker[i], ls='', c=colors[1], markersize=markersize,
                   label="Dayily Model %d" % (i + 1))
    for i, (stddev, corrcoef) in enumerate(samples3):
        dia.add_sample(stddev, corrcoef, marker= marker[i], ls='', c=colors[2], markersize=markersize,
                    label="Monthly Model %d" % (i + 1))
    for i, (stddev, corrcoef) in enumerate(samples4):
        dia.add_sample(stddev, corrcoef, marker= marker[i], ls='', c=colors[3], markersize=markersize,
                   label="Annully Model %d" % (i + 1))

                # Add RMS contours, and label them
    contours = dia.add_contours(colors='0.5')
    PLT.clabel(contours, inline=1, fontsize=12)

    # Add a figure legend
    # PLT.legend(bbox_to_anchor=(0., 1.02), loc=3, ncol=1, mode="expand", borderaxespad=0.)
    fig.legend(dia.samplePoints,
               [p.get_label() for p in dia.samplePoints],
               numpoints=1, prop=dict(size='medium'), loc='upper right') #

    return fig, samples1, samples2, samples3, samples4





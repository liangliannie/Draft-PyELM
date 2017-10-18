from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap
from cycle_analysis import cycle_analysis
from spectrum_analysis import spectrum_analysis
from basic_post import time_analysis
from html_post import final_post
import os

''' Obtain observations data from files'''
def read_file(Root_Dir, name):
    return Dataset(Root_Dir + name)

def site_name_extract(o, variable):
    return o.variables['site_name'][:]

def site_address_extract(o, variable):
    return o.variables['lon'][:], o.variables['lat'][:]

def data_extract(o, variable):
    ''' Read a certain variable for obs return np.masked.array for only data,
     time is not masked '''
    data = o.variables[variable][:]
    data = np.ma.masked_invalid(data)
    unit = o.variables[variable].units
    time = o.variables['time'][:]
    return data, time, unit

''' Obtain models data from files'''
def models_data_extract(o, m, variable):
    ''' Read multiple models for a certain variable, return list of models data,
     model data is masked based on the observed data '''
    data1, time1, unit1 = [],[],[]
    for i in range(len(m)):
        data, time, unit = data_extract(m[i], variable)
        np.ma.masked_where(np.ma.getmask(o), data)
        test = False
        ''' The models should be changed back here '''
        if test:
            data = o + np.random.rand(data.shape[0],data.shape[1])*0.00000005
        data1.append(data)
        time1.append(time)
        unit1.append(unit)
    return data1, time1, unit1


''' Obtain hourly season cycle from dataset'''
def hourly_process(data):
    # hour_data return shape ( site, day, hour)
    # hour_data s1 return shape ( day, site, hour)
    ''' hour_cycle based on four seasons, return four seasons data data,
         model data is masked based on the observed data '''
    hour_data = data.reshape(len(data), len(data[0])/24, 24)
    hour_data_s1, hour_data_s2, hour_data_s3, hour_data_s4 =[],[],[],[]
    for y in range(len(data[0])/24/365):
        for d in range(0, 365):
            if d <= 58:
                hour_data_s1.append(hour_data[0:len(data),y*365+d, 0:24])
            elif d <= 151:
                hour_data_s2.append(hour_data[0:len(data),y*365+d, 0:24])
            elif d <= 242:
                hour_data_s3.append(hour_data[0:len(data),y*365+d, 0:24])
            elif d <= 334:
                hour_data_s4.append(hour_data[0:len(data),y*365+d, 0:24])
            else:
                hour_data_s1.append(hour_data[0:len(data),y*365+d, 0:24])
    hour_data_s1 = np.asarray(hour_data_s1)
    hour_data_s2 = np.asarray(hour_data_s2)
    hour_data_s3 = np.asarray(hour_data_s3)
    hour_data_s4 = np.asarray(hour_data_s4)
    hour_data_s1 = np.ma.masked_invalid(hour_data_s1)
    hour_data_s2 = np.ma.masked_invalid(hour_data_s2)
    hour_data_s3 = np.ma.masked_invalid(hour_data_s3)
    hour_data_s4 = np.ma.masked_invalid(hour_data_s4)
    return hour_data_s1, hour_data_s2, hour_data_s3, hour_data_s4, hour_data

def models_hourly_process(m):
    hour_data_s1, hour_data_s2, hour_data_s3, hour_data_s4, hour_data = [],[],[],[],[]
    for i in range(len(m)):
        s1,s2,s3,s4,s = hourly_process(m[i])
        hour_data_s1.append(s1)
        hour_data_s2.append(s2)
        hour_data_s3.append(s3)
        hour_data_s4.append(s4)
        hour_data.append(s)
    return hour_data_s1, hour_data_s2, hour_data_s3, hour_data_s4, hour_data

''' Obtain daily cycle from dataset'''
def daily_process(data):
    # return shape ( site, year, day)
    # print(data.shape)
    data = data.reshape(len(data), len(data[0])/365, 365)
    # print(data.shape)
    return data

def models_daily_process(m):
    day_data = []
    for i in range(len(m)):
        day_data.append(daily_process(m[i]))
    return day_data

''' Obtain monthly cycle from dataset'''

def monthly_process(data):
    # return shape ( site, year, month)

    data = data.reshape(len(data),len(data[0])/12, 12)
    return data


def models_monthly_process(m):
    month_data = []
    for i in range(len(m)):
        month_data.append(monthly_process(m[i]))
    return month_data

''' Obtain seasonly cycle from dataset'''
def seasonly_process(data):
    # return shape (season, site, year)
    # data = data.reshape(len(data),len(data[0])/12, 4, 3)
    m, n =len(data), len(data[0])/12
    data = data.reshape(m,n, 12)
    # season_data = np.ma.zeros(m,n, 4)
    season1 = (data[0:m, 0:n, 0]+data[0:m, 0:n, 10]+data[0:m, 0:n, 11])/3
    season2 = (data[0:m, 0:n, 1]+data[0:m, 0:n, 2]+data[0:m, 0:n, 3])/3
    season3 = (data[0:m, 0:n, 4]+data[0:m, 0:n, 5]+data[0:m, 0:n, 6])/3
    season4 = (data[0:m, 0:n, 7]+data[0:m, 0:n, 8]+data[0:m, 0:n, 9])/3

    season_data = [season1,season2,season3,season4]
    season_data = np.asarray(season_data)
    season_data= np.ma.masked_invalid(season_data)
    return season_data

def models_seasonly_process(m):
    month_data = []
    for i in range(len(m)):
        month_data.append(seasonly_process(m[i]))
    return month_data


def output_all_figs(filedir, variable_name, h_o, d_o, m_o, y_o, h_models, d_models, m_models, y_models, h_site_name_obs):
    # Process hourly cycle
    if variable_name == 'FSH_EFLX_LH_TOT':
        variable1, variable2 = 'FSH', 'EFLX_LH_TOT'
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
        h_mod, d_mod, m_mod, y_mod =[],[],[],[]

        h_obs, h_t_obs, h_unit_obs  = np.divide(h_obs1,h_obs2), h_t_obs1, h_unit_obs1+'/'+ h_unit_obs2
        d_obs, d_t_obs, d_unit_obs  = np.divide(d_obs1,d_obs2), d_t_obs1, d_unit_obs1+'/'+ d_unit_obs2
        m_obs, m_t_obs, m_unit_obs  = np.divide(m_obs1,m_obs2), m_t_obs1, m_unit_obs1+'/'+ m_unit_obs2
        y_obs, y_t_obs, y_unit_obs  = np.divide(y_obs1,y_obs2), y_t_obs1, y_unit_obs1+'/'+ y_unit_obs2

        h_t_mod, h_unit_mod = h_t_mod1, h_unit_mod1
        d_t_mod, d_unit_mod = d_t_mod1, d_unit_mod1
        m_t_mod, m_unit_mod = m_t_mod1, m_unit_mod1
        y_t_mod, y_unit_mod = y_t_mod1, y_unit_mod1
        for m in range(len(h_mod1)):
            h_mod.append(np.divide(h_mod1[m],h_mod2[m]))
            d_mod.append(np.divide(d_mod1[m],d_mod2[m]))
            m_mod.append(np.divide(m_mod1[m],m_mod2[m]))
            y_mod.append(np.divide(y_mod1[m],y_mod2[m]))
    else:
        h_obs, h_t_obs, h_unit_obs = data_extract(h_o, variable_name)
        h_mod, h_t_mod, h_unit_mod = models_data_extract(h_obs, h_models, variable_name)
        # Process Daily cycle
        d_obs, d_t_obs, d_unit_obs = data_extract(d_o, variable_name)
        d_mod, d_t_mod, d_unit_mod = models_data_extract(d_obs, d_models, variable_name)
        # Process Monthly cycle
        m_obs, m_t_obs, m_unit_obs = data_extract(m_o, variable_name)
        m_mod, m_t_mod, m_unit_mod = models_data_extract(m_obs, m_models, variable_name)
        # Process yearly cycle
        y_obs, y_t_obs, y_unit_obs = data_extract(y_o, variable_name)
        y_mod, y_t_mod, y_unit_mod = models_data_extract(y_obs, y_models, variable_name)



    ''' This function extract the hourly cycle of all data'''
    o_h_s1, o_h_s2, o_h_s3, o_h_s4, o_hour_data = hourly_process(h_obs)
    m_h_s1, m_h_s2, m_h_s3, m_h_s4, m_hour_data = models_hourly_process(h_mod)
    ''' This function extract the daily cycle of all data'''
    o_daily_data = daily_process(d_obs)
    m_daily_data = models_daily_process(d_mod)
    ''' This function extract the monthly cycle of all data'''
    o_monthly_data = monthly_process(m_obs)
    m_monthly_data = models_monthly_process(m_mod)
    ''' This function extract the seasonly cycle of all data'''
    # Process Seasonly cycle
    o_seasonly_data = seasonly_process(m_obs)
    m_seasonly_data = models_seasonly_process(m_mod)


    # compress data transmit
    hour_obs = [h_obs, h_t_obs, h_unit_obs]
    hour_mod = [h_mod, h_t_mod, h_unit_mod]
    day_obs = [d_obs, d_t_obs, d_unit_obs]
    day_mod = [d_mod, d_t_mod, d_unit_mod]
    month_obs = [m_obs, m_t_obs, m_unit_obs]
    month_mod = [m_mod, m_t_mod, m_unit_mod]
    year_obs = [y_obs, y_t_obs, y_unit_obs]
    year_mod = [y_mod, y_t_mod, y_unit_mod]

    ''' This function output the time_series with the taylor gram'''
    scores_time_series, scores_pdf = time_analysis(variable_name, h_site_name_obs, filedir, hour_obs, hour_mod, day_obs, day_mod, month_obs, month_mod, year_obs, year_mod)
    ''' This function output the different cycles with the taylor gram'''
    scores_day_cycle, scores_fourcycle, scores_seassoncycle = cycle_analysis(variable_name, h_unit_obs, d_unit_obs,m_unit_obs, y_unit_obs, h_site_name_obs, filedir, o_h_s1, o_h_s2, o_h_s3, o_h_s4, m_h_s1, m_h_s2, m_h_s3, m_h_s4, o_hour_data, o_daily_data, o_monthly_data, o_seasonly_data, m_hour_data, m_daily_data, m_monthly_data, m_seasonly_data)
    # ''' This function output the different frequency with the taylor gram'''
    scores_imf, scores_decomposeimf, score_wavelet, score_spectrum, score_taylor_gram = spectrum_analysis(filedir,h_site_name_obs, day_obs, day_mod, variable_name)

    return scores_time_series, scores_pdf, scores_day_cycle, scores_fourcycle, scores_seassoncycle, scores_imf, scores_decomposeimf, score_wavelet, score_spectrum, score_taylor_gram


""" The following start with one_variable_different_site """
mainfiledir = '/Users/lli51/Documents/ornl_project/'
Root_Dir = mainfiledir + '171002_parmmods_'
h_o, d_o, m_o, y_o = read_file(Root_Dir, 'hourly_obs.nc'), read_file(Root_Dir, 'daily_obs.nc'), read_file(Root_Dir, 'monthly_obs.nc'), read_file(Root_Dir, 'annual_obs.nc')
h_m1, d_m1, m_m1, y_m1 = read_file(Root_Dir, 'hourly_model.nc'), read_file(Root_Dir, 'daily_model.nc'), read_file(Root_Dir, 'monthly_model.nc'), read_file(Root_Dir, 'annual_model.nc') # output the list of models and observations
h_m2, d_m2, m_m2, y_m2 = read_file(Root_Dir, 'hourly_model.nc'), read_file(Root_Dir, 'daily_model.nc'), read_file(Root_Dir, 'monthly_model.nc'), read_file(Root_Dir, 'annual_model.nc') # output the list of models and observations


h_models = [h_m1, h_m2]
d_models = [d_m1, d_m2]
m_models = [m_m1, m_m2]
y_models = [y_m1, y_m2]

models = []
models_name =['Model 1', 'Model 2']


site_name_obs = site_name_extract(h_o, 'NEE')
lon, lat = site_address_extract(h_o, 'NEE')
variable_list = ['FSH', 'NEE' ] # for value output caculation
variable_list1, variable_list2 = ['GPP', 'GPP'], ['NEE', 'ER'] # for response caculation

variable_scores = []
for variable_name in variable_list:
    directory = './output/' + variable_name + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    variable_scores.append(output_all_figs('./output/', variable_name, h_o, d_o, m_o, y_o, h_models, d_models, m_models, y_models,site_name_obs))

variable_scores = np.asarray(variable_scores)
'''Plot all response figs'''
from response_post import plot_all_response
scores_reponse = plot_all_response('./output/',site_name_obs, h_o, d_o, m_o, y_o, h_models, d_models, m_models, y_models, variable_list1, variable_list2)

from score_post import score_system
score = score_system('./output/', site_name_obs, models_name, variable_list, variable_scores, scores_reponse)
score.plot_all()


print('Posting HTML')
final_post(mainfiledir, lon, lat, site_name_obs, variable_list, variable_list1, variable_list2, len(h_models))




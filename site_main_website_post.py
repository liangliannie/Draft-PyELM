import os

def strToFile(text, web_dir, web_name):
    """Write a file with the given name and the given text."""
    output = open(web_dir + web_name, "w")
    output.write(text)
    output.close()

def browseLocal(webpageText, web_dir, web_name):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, web_dir, web_name)
    webbrowser.open(os.path.abspath(web_dir + web_name))  # elaborated for Mac

def add_figure_link(Fig_name, Fig_dir, Fig_alt, href, width=150, height=120):
    data_uri = open(Fig_dir, 'rb').read().encode('base64').replace('\n', '')

    return '<div class="imgContainer"> <figure> <figcaption> %s </figcaption> <a href = "%s" > <img border = "0" alt = "%s" src = "data:image/png;base64,%s" width = "%d" height = "%d" ></a><figure></div>' %(Fig_name, href, Fig_alt, data_uri, width, height)

def table_link(maindir, site, category, variable):

    table_front = '''<table border="0.1" width="20" style="margin-left:30%;float:top;"> 
            <tr>'''
    for v in variable:
        s = './output/websites/'+site+category+v+'.html'
        table_front +=  '''<td><p><a href="%s"> %s </a></p></td>''' %(s, v)

    table_end = '''</tr> </table>'''
    table = table_front + table_end
    return table

def table_link2(maindir, site, variable1, variable2):
    table_front = '''<table border="0.1" width="20" style="margin-left:30%;float:top;"> 
            '''
    for i in range(len(variable1)):
        s = './output/websites/'+'response'+site+variable1[i]+'vs'+variable2[i]+'.html'
        table_front +=  '''<tr><td><p><a href="%s"> %s </a></p></td></tr>''' %(s, variable1[i]+'_vs_'+variable2[i])

    table_end = '''  </table>'''
    table = table_front + table_end
    return table

def generate_post_site(site, variable, mainfiledir, variable1, variable2):
    page_front = '''<!DOCTYPE html>
    <html>
        <head>
        <base href="'''+mainfiledir+'''"></base>
    <style>
    * {
        box-sizing: border-box;
    }

          /* Optional: Makes the sample page fill the window. */
          html, body {
            height: 100%;
            margin: 20;
            padding: 0;
          }

    /* Create two equal columns that floats next to each other */
    .columnleft {
        float: left;
        width: 40%;
        /*height: 100%;  Should be removed. Only for demonstration */
    }

    .columnright {
        float: right;
        width: 60%;
        /*height: 100%;  Should be removed. Only for demonstration */
    }
    /* Clear floats after the columns */
    .row:after {
        content: "";
        display: table;
        clear: both;
    }
        .headertekst {
      text-align: center;
    }
    
    .imgContainer{
    float:left;
}

    </style>
    </head>

    <body>'''
    page_body_left = '''   <div  class="columnleft"> <h2>Site Analysis </h2> <p> {instruction} </p> 
    '''

    page_body_right = ''' </div> <div class="columnright"> '''



    page_tail = '''</div>
    </body>
    </html>'''
    instruction = 'This website shows the site analysis, where we explore the difference between observations and models. Four sections of data is listed.'


    page_body_left = page_body_left.format(**locals())
    page_body_left  += add_figure_link('Score', 'output/score/'+site+'summary_score.png','scores', 'output/main_website.html',width=350, height=500)

    table_time = table_link('output/websites/', site, 'time_series', variable)
    page_body_right += add_figure_link('Time series Analysis' + table_time, 'output/'+variable[0]+'/'+site+'_time_series_'+variable[0]+'.png', 'time_series', './output/websites/'+site+'time_series'+variable[0]+'.html')

    table_pdf = table_link('output/websites/', site, 'pdf', variable)
    page_body_right += add_figure_link('PDF and Cycle Analysis'+ table_pdf, 'output/'+variable[0]+'/'+site+'_pdf_'+variable[0]+'.png', 'pdf', './output/websites/'+site+'pdf'+variable[0]+'.html')

    table_frequency = table_link('output/websites/', site, 'wavelet', variable)
    page_body_right += add_figure_link('Frequency Analysis'+table_frequency, 'output/'+variable[0]+'/'+site+'_wavelet_'+variable[0]+'.png', 'wavelet', './output/websites/'+site+'wavelet'+variable[0]+'.html')

    table_frequency = table_link('output/websites/', site, 'imf', variable)
    page_body_right += add_figure_link('Spectrum Analysis'+table_frequency, 'output/'+variable[0]+'/'+site+'_imf_'+variable[0]+'.png', 'imf', './output/websites/'+site+'imf'+variable[0]+'.html')

    table_frequency = table_link('output/websites/', site, 'spectrum', variable)
    page_body_right += add_figure_link('Spectrum Analysis'+table_frequency, 'output/'+variable[0]+'/'+site+'_spectrum_'+variable[0]+'.png', 'spectrum', './output/websites/'+site+'spectrum'+variable[0]+'.html')

    table_response = table_link2('output/websites/', site, variable1, variable2)
    page_body_right += add_figure_link('Response Analysis'+table_response, 'output/'+'response'+'/'+site+'_'+variable1[0]+'_vs_'+variable2[0]+'_Response.png', 'time_series', './output/websites/'+'response'+site+variable1[0]+'vs'+variable2[0]+'.html')
    page_body_right += add_figure_link('Response Bin'+table_response, 'output/'+'response'+'/'+site+'_'+variable1[0]+'_vs_'+variable2[0]+'_Response_Bin.png', 'time_series', './output/websites/'+'response'+site+variable1[0]+'vs'+variable2[0]+'.html')
    contents = page_front + page_body_left + page_body_right + page_tail
    browseLocal(contents, 'output/websites/', site+'local.html')
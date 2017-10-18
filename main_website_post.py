
def add_figure(fig_dir, fig_name, body):
    import datetime
    img_id = str(datetime.datetime.now())
    '''Add a figure to the website '''
    data_uri = open(fig_dir + fig_name, 'rb').read().encode('base64').replace('\n', '')
    # data_uri = fig_dir + fig_name
    # body += '<button onclick = button_img("%s")> Click to hide/view the picture </button>' % img_id[-6:]
    body += '<div class="columnright" style="text-align: center;">  <img src="data:image/png;base64,%s" height="1600" width="400" > </div>' % data_uri
    # body += '<div class="columnright" style="text-align: center;">  <img src="%s" height="1600" width="600" > </div>' % data_uri

    return body

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

def generate_post(fig_dir, fig_name, site, lon, lat):
    ''' generate the html '''
    page_front = '''<!DOCTYPE html>
    <html>
    <head>
    <style>
    * {
        box-sizing: border-box;
    }

     #map {
            height: 150%;
          }

          /* Optional: Makes the sample page fill the window. */
          html, body {
            height: 100%;
            margin: 0;
            padding: 0;
          }

    /* Create two equal columns that floats next to each other */
    .columnleft {
        float: left;
        width: 60%;
        height: 2000pt; /*height: 100%;  Should be removed. Only for demonstration */
    }

    .columnright {
        float: right;
        width: 40%;
        height: 2000pt; 
        top: 200pt; /*height: 100%;  Should be removed. Only for demonstration */
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

    </style>
    </head>
    <body>'''

    page_body = '''<h2 class="headertekst" >Main website</h2>
      <div  class="columnleft" id="map"> <h2>Google Maps</h2> </div> '''

    page_tail1 = '''
        <script>
    // The following example creates complex markers to indicate beaches near
    // Sydney, NSW, Australia. Note that the anchor is set to (0,32) to correspond
    // to the base of the flagpole.

    function initMap() {
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: 40, lng: 0}
      });

      setMarkers(map);
    }

    // Data for the markers consisting of a name, a LatLng and a zIndex for the
    // order in which these markers should display on top of each other.
   '''
    page_tail2 = '''
    var site ={site};

    var lon = {lon};

    var lat = {lat};
'''

    page_tail3 = '''function setMarkers(map) {
  // Adds markers to the map.

  // Marker sizes are expressed as a Size of X,Y where the origin of the image
  // (0,0) is located in the top left of the image.

  // Origins, anchor positions and coordinates of the marker increase in the X
  // direction to the right and in the Y direction down.


  var image = {
    url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
    // This marker is 20 pixels wide by 32 pixels high.
    size: new google.maps.Size(40, 32),
    // The origin for this image is (0, 0).
    origin: new google.maps.Point(9, 9),
    // The anchor for this image is the base of the flagpole at (0, 32).
    anchor: new google.maps.Point(0, 32)

  };
  // Shapes define the clickable region of the icon. The type defines an HTML
  // <area> element 'poly' which traces out a polygon as a series of X,Y points.
  // The final coordinate closes the poly by connecting to the first coordinate.
  var shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: 'poly'
  };
  for (var i = 0; i < site.length; i++) {
      var content ='<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h1 id="firstHeading" class="firstHeading">'+site[i]+'</h1>'+
            '<div id="bodyContent">'+
            '<p><b>'+site[i]+'</b>, also referred to as <b>Ayers Rock</b></p>'+
            '<p>Attribution can be viewed here, <a href='+'./websites/'+site[i]+'local.html'+'>'+
            site[i]+'(Site Analysis)'+
            '</p>'+
            '</div>'+
            '</div>';
/*    var infowindow = new google.maps.InfoWindow({
          content: contentString
        });*/
    var marker = new google.maps.Marker({
      position: {lat: lat[i], lng: lon[i]},
      map: map,
      icon: image,
      shape: shape,
      label: {
        text: site[i],
        color: 'red',
        fontSize: '8px'}
             });
//      map.setCenter(marker.getPosition())
/*    marker.addListener('click', function() {
          infowindow.open(map, marker);
        }); */
      var infowindow = new google.maps.InfoWindow()

      google.maps.event.addListener(marker,'click', (function(marker,content,infowindow){ 
    return function() {
        infowindow.setContent(content);
        infowindow.open(map,marker);
    };
})(marker,content,infowindow))

  }
}

        </script>
    <script src="https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js">
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAH39vavrp239Xpe-tOApYbghr2AgHE708&callback=initMap">
    </script>
  </body>
</html>    '''

    page_tail2 = page_tail2.format(**locals())
    page_body = add_figure(fig_dir, fig_name, page_body)
    contents = page_front + page_body + page_tail1+page_tail2+page_tail3
    browseLocal(contents, fig_dir, 'main_website.html')


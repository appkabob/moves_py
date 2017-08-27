import folium
from folium import plugins
from lib.PyMoves.moves import Moves
import constants


class Map:
    def get_moves_trackpoints(self, on_or_after, on_or_before):
        m = Moves(constants.CLIENT_ID, constants.CLIENT_SECRET, constants.CALLBACK_URL, constants.API_URL)
        dates = m.get_range(constants.ACCESS_TOKEN, '/user/storyline/daily', on_or_after, on_or_before)
        # dates.extend(m.get_range(constants.ACCESS_TOKEN, '/user/storyline/daily', '2017-07-17', '2017-07-23'))
        # dates.extend(m.get_range(constants.ACCESS_TOKEN, '/user/storyline/daily', '2017-08-17', '2017-08-23'))
        trackpoints = []
        for date in dates:
            for segment in date['segments']:
                if not 'activities' in segment: segment['activities'] = []
                for activity in segment['activities']:
                    for trackpoint in activity['trackPoints']:
                        trackpoints.append(tuple([trackpoint['lat'], trackpoint['lon']]))
        return trackpoints

    def save(self, filename, data_layers):
        """data_layers should be a dict of format {name: 'Airplane', color: 'blue', trackpoints: [[lat, lon]]}"""
        map = folium.Map(location=[38.58, -99.09], zoom_start=3, tiles="Mapbox Bright")
        for layer in data_layers:
            fgp = folium.FeatureGroup(name=layer['name'])

            if layer['name'] == 'Airplane':
                attr = {'font-weight': 'bold', 'font-size': '20', 'opacity': 0.5}
                plane_line = folium.PolyLine(layer['trackpoints'], color=layer['color'], weight=1, opacity=0.5)
                plane_line1 = plugins.PolyLineTextPath(
                    plane_line,
                    '\u2708                 ',
                    repeat=True,
                    offset=8,
                    attributes=attr
                )
                fgp.add_child(plane_line)
                fgp.add_child(plane_line1)
            else:
                fgp.add_child(folium.PolyLine(layer['trackpoints'], color=layer['color'], weight=2.5, opacity=0.5))
            map.add_child(fgp)
        map.add_child(folium.LayerControl())
        map.save(filename)

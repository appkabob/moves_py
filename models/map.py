import folium
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

    def save(self, filename, polyline_data):
        map = folium.Map(location=[38.58, -99.09], zoom_start=3, tiles="Mapbox Bright")
        fgp = folium.FeatureGroup(name="Paths")
        fgp.add_child(folium.PolyLine(polyline_data, color="blue", weight=2.5, opacity=0.5))
        map.add_child(fgp)
        map.add_child(folium.LayerControl())
        map.save(filename)

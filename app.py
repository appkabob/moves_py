from models.map import Map


map = Map()
data = map.get_moves_trackpoints('2017-07-10', '2017-07-16')
map.save("output/Map1.html", data)

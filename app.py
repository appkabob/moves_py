from datetime import datetime
from dateutil.relativedelta import relativedelta
from database import Database
from models.map import Map
from models.storyline import Storyline

Database.initialize()

storylines = Storyline.all_from_mongo()
map = Map()
map.save("output/Map1.html", [
    {'name': 'Airplane', 'color': 'black', 'trackpoints': [storyline.trackpoints('airplane') for storyline in storylines]},
    {'name': 'Walking', 'color': 'green', 'trackpoints': [storyline.trackpoints('walking') for storyline in storylines]},
    {'name': 'Car', 'color': 'blue', 'trackpoints': [storyline.trackpoints('car') for storyline in storylines]},
    {'name': 'Bus', 'color': 'purple', 'trackpoints': [storyline.trackpoints('bus') for storyline in storylines]},
    {'name': 'Train', 'color': 'orange', 'trackpoints': [storyline.trackpoints('train') for storyline in storylines]},
    {'name': 'Boat', 'color': 'yellow', 'trackpoints': [storyline.trackpoints('boat') for storyline in storylines]},
    {'name': 'Bicycle', 'color': 'brown', 'trackpoints': [storyline.trackpoints('bike') for storyline in storylines]},
])


def fetch_storylines_from_moves_and_save_in_mongo():
    initial_date = datetime.strptime('2017-05-14', '%Y-%m-%d')
    for i in range(0, 55):
        end_date = initial_date + relativedelta(days=6)
        print('INITIAL_DATE', initial_date)
        print('END_DATE', end_date)
        storylines = Storyline.fetch_by_date_range(initial_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        for storyline in storylines:
            print(storyline)
            storyline.save_to_mongo()
        initial_date += relativedelta(days=7)

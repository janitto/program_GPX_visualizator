import gpxpy
import pandas as pd
import folium
import os
import time
from folium import plugins

init_coordinates = [48.205, 17.10]

m = folium.Map(location=init_coordinates, zoom_start=12, tiles="Stamen Terrain")
test_mark = '<head><meta http-equiv="Content-Type" content="text/html; charset=windows-1250"></head>'
m.get_root().html.add_child(folium.Element(test_mark))

workouts_group = folium.FeatureGroup(name="All workout")
points_group = folium.FeatureGroup(name="Points of Interest")
m.add_child(workouts_group)
m.add_child(points_group)

workouts = os.listdir("workouts")
colors = ['purple', 'black', 'blue', 'yellow',
          'orange', 'darkgreen', 'darkpurple', 'darkred',
          'gray', 'green', 'pink', 'lightgray',
          'lightgreen', 'lightred', 'darkblue', 'lightblue',
          'purple', 'red', 'white', "beige"]

i = 0
for workout in workouts:
    group = plugins.FeatureGroupSubGroup(workouts_group, f"Workout{i}")
    m.add_child(group)
    i += 1
    start_time = time.time()
    print(f"Processing {i}/{len(workouts)}...")
    gpx_file = open(f'workouts/{workout}', 'r')
    gpx = gpxpy.parse(gpx_file)

    #   print(len(gpx.tracks))                          # kolko mam workoutov v subore
    #   print(gpx.tracks[0].get_time_bounds().start_time)
    #   print(gpx.tracks[0].length_3d())
    #   print(gpx.tracks[0].get_duration())
    #   print(gpx.tracks[0].get_moving_data().max_speed)
    #   print(gpx.tracks[0].segments[0].length_3d())
    #   print(gpx.tracks[0].segments[0].get_speed(40))
    #   print(len(gpx.tracks[0].segments[0].points))    # tu su body segmentu

    data = gpx.tracks[0].segments[0].points
    #   print(data[0])                                  # prvy bod segmentu
    #   print(data[-1])                                 # posledny bod segmentu

    df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])    # napln pandas dataframe datami z GPX
    for idx, point in enumerate(data):
        df = df.append({'lon': point.longitude,
                        'lat': point.latitude,
                        'alt': point.elevation,
                        'time': point.time},
                       ignore_index=True)

    x = folium.PolyLine(df[["lat", "lon"]],
                        color=colors[i-1],
                        weight=2.5,
                        opacity=1).add_to(group)

    end_time = time.time()
    duration = end_time - start_time
    print(f"File {i} processed in {round(duration,1)} sec.")

folium.LayerControl(collapsed=False).add_to(m)

with open("PointsOfInterest.txt", "r") as f:
    poi = f.read().rstrip("\n").split("\n")
    for x in poi:
        folium.Marker([x.split(";")[1], x.split(";")[2]], tooltip=x.split(";")[0]).add_to(points_group)
    f.close()

m.save("MyMap.html")

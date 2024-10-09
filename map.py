import pandas
import folium

data = pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
name = list(data["NAME"])
elev = list(data["ELEV"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


def color_by_elevation(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


feature_group = folium.FeatureGroup(name="Volcanoes")
feature_group_pop = folium.FeatureGroup(name="Population")

map = folium.Map(location=[6.666, -6.666], zoom_start=13)
feature_group.add_child(
    folium.Marker(
        location=[6.280767, -75.549380],
        popup="Hi it's my house",
        icon=folium.Icon(color="red"),
    )
)

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    feature_group.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            popup=folium.Popup(iframe),
            fillColor=color_by_elevation(el),
            color="grey",
            fillOpacity=0.7,
        )
    )

feature_group_pop.add_child(
    folium.GeoJson(
        data=open(
            "world.json",
            "r",
            encoding="utf-8-sig").read(),
            style_function=lambda x: {
                "fillColor": "green"
                if x["properties"]["POP2005"] < 10000000
                else "orange" 
                if 10000000 <= x["properties"]["POP2005"] < 20000000
                else "red"
            },
        )
    )

map.add_child(feature_group)
map.add_child(feature_group_pop)
map.add_child(folium.LayerControl())

map.save("Map.html")

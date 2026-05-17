import osmnx as ox

tags = {
    "railway": "station"
}

stations = ox.features_from_place(
    "Sydney, New South Wales, Australia",
    tags
)

stations = stations[["name", "geometry"]]

stations.to_file(
    "sydney_stations.geojson",
    driver="GeoJSON"
)

print(stations[["name"]].head())
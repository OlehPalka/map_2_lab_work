"""
Module which makes operations with map and coordinates.
"""


import folium
import haversine
from geopy.exc import GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

mapp = folium.Map(tiles="CartoDB dark_matter")
geolocator = Nominatim(user_agent="sotiy_try.")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def find_country_by_coordinates(coordinates):
    """
    This function finds country where your coordinates are setted.
    """
    location = geolocator.reverse(coordinates, language='en')
    return location.address.split(",")[-1]


def possible_films(country, year):
    """
    This function makes list of possible films using setted
    year and country you entered.
    """
    result = list()
    with open("locations.list") as file:
        for line in file:
            if year in line:
                line = line[:-1]
                line = line.split("\t")
                if country in line[-1]:
                    if line[-1] != ")":
                        result.append(line)
    return result


def possible_films_2(year):
    """
    This function is used when there are no films in your country at exact year.
    It finds possible films only by year.
    """
    result = list()
    with open("locations.list") as file:
        for line in file:
            if year in line:
                line = line[:-1]
                line = line.split("\t")
                if line[-1] != ")":
                    result.append(line)
                    if len(result) == 50:
                        return result
    return result


def distance_counct(coordinates, list_of_films):
    """
    This fucntion finds coordinations for each place in list_of_films,
    where the film was made.
    """
    your_coordinates = coordinates.split(",")
    for i in range(2):
        your_coordinates[i] = float(your_coordinates[i])
    counter = 0
    while True:
        distance = haversine.haversine(your_coordinates,
                                       list(list_of_films[counter][-1]))
        list_of_films[counter].append(distance)
        counter += 1
        if len(list_of_films) == counter:
            break
    return list_of_films


def main_function(coordinates, your_year):
    """
    Main function set 10 points on the map, which are 10 films,
    which are the closest to you.
    """
    year = "(" + str(your_year) + ")"
    country = find_country_by_coordinates(coordinates)
    if country == " United States":
        country = "USA"
    if country == " United Kingdom":
        country = "UK"
    list_of_films = possible_films(country, year)
    if len(list_of_films) == 0:
        list_of_films = possible_films_2(year)
    counter = 0
    while True:
        try:
            location = geolocator.geocode(list_of_films[counter][-1])
            list_of_films[counter].append(
                (location.latitude, location.longitude))
            counter += 1
        except (AttributeError, GeocoderUnavailable, ValueError):
            del list_of_films[counter]
            continue
        if counter == len(list_of_films):
            break
    list_of_films = list_of_films[:counter]
    list_of_films = distance_counct(coordinates, list_of_films)
    list_of_films = sorted(list_of_films, key=lambda x: x[-1])[:10]
    for coordinate in list_of_films:
        folium.Marker(
            location=coordinate[-2], popup=coordinate[0],
            icon=folium.Icon(color='gray')).add_to(mapp)
    points = []
    lenth = len(list_of_films)
    for i in range(lenth):
        points.append(list_of_films[i][-2])
    folium.PolyLine(points, color='red').add_to(mapp)
    mapp.save("lol.html")
    return "Finished. Please have look at the map lol.html"


if __name__ == '__main__':
    coordinatess = input("Please enter your location (format: lat, long):")
    yearr = input("Please enter a year you would like to have a map for:")
    print("""Map is generating...
Please wait...""")
    print(main_function(coordinatess, yearr))


# print(main_function("48.287312, 25.1738", 1998))

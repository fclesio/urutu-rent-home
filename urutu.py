import sys
import requests
import pandas as pd
import folium

from datetime import datetime


extraction_date = datetime.today().strftime("%Y%m%d_%H%M%S")

HEADERS = {
    "accept": "application/json; charset=utf-8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-length": "0",
    "content-type": "application/json; charset=utf-8",
    "origin": "https://www.immobilienscout24.de",
    "referer": "https://www.immobilienscout24.de/Suche/radius/wohnung-mieten?centerofsearchaddress=Berlin;10829;;;;&geocoordinates=52.4856;13.36495;100.0&enteredFrom=one_step_search",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


def get_immo24_search_pages(headers=HEADERS):
    searchresults = []
    pageexists = True
    i = 1
    while pageexists:
        try:
            r = requests.post(
                f"https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?pagenumber={i}",
                headers=headers,
            )
            rdict = r.json()
            try:
                searchresults.append(
                    rdict["searchResponseModel"]["resultlist.resultlist"][
                        "resultlistEntries"
                    ][0]["resultlistEntry"]
                )
            except:
                sys.stdout.write(str("All pages fetched...") + '\n')
                pageexists = False
        except:
            sys.stdout.write(str("All pages fetched...") + '\n')
            pageexists = False
        i += 1
    return searchresults


def get_listings_detailed_info(searchresults):
    listing_results = []

    # Solution based in https://github.com/s0er3n/immobilienscout24-scraper/blob/master/immobilienscout24-scraper.py
    for d in searchresults:
        for x in d:

            try:
                home_id = x["@id"]
            except:
                home_id = "N/A"

            try:
                title = x["resultlist.realEstate"]["title"]
            except:
                title = "N/A"

            try:
                postcode = x["resultlist.realEstate"]["address"]["postcode"]
            except:
                postcode = "N/A"

            try:
                price = x["resultlist.realEstate"]["price"]["value"]
            except:
                price = "N/A"

            try:
                street = x["resultlist.realEstate"]["address"]["street"]
            except:
                street = "N/A"

            try:
                houseNumber = x["resultlist.realEstate"]["address"]["houseNumber"]
            except:
                houseNumber = "N/A"

            try:
                city = x["resultlist.realEstate"]["address"]["city"]
            except:
                city = "N/A"

            try:
                quarter = x["resultlist.realEstate"]["address"]["quarter"]
            except:
                quarter = "N/A"

            try:
                latitude = x["resultlist.realEstate"]["address"]["wgs84Coordinate"][
                    "latitude"
                ]
            except:
                latitude = "N/A"

            try:
                longitude = x["resultlist.realEstate"]["address"]["wgs84Coordinate"][
                    "longitude"
                ]
            except:
                longitude = "N/A"

            try:
                livingSpace = x["resultlist.realEstate"]["livingSpace"]
            except:
                livingSpace = "N/A"

            try:
                numberOfRooms = x["resultlist.realEstate"]["numberOfRooms"]
            except:
                numberOfRooms = "N/A"

            try:
                balcony = x["resultlist.realEstate"]["balcony"]
            except:
                balcony = "N/A"

            try:
                garden = x["resultlist.realEstate"]["garden"]
            except:
                garden = "N/A"

            try:
                monthlyRate = x["resultlist.realEstate"]["monthlyRate"]
            except:
                monthlyRate = "N/A"

            try:
                builtInKitchen = x["resultlist.realEstate"]["builtInKitchen"]
            except:
                builtInKitchen = "N/A"

            listing_results.append(
                (
                    home_id,
                    title,
                    postcode,
                    price,
                    street,
                    houseNumber,
                    city,
                    quarter,
                    latitude,
                    longitude,
                    livingSpace,
                    numberOfRooms,
                    balcony,
                    garden,
                    monthlyRate,
                    builtInKitchen,
                    f"https://www.immobilienscout24.de/expose/{home_id}",
                )
            )

    return listing_results


def get_df_with_columns(listing_results):
    df_listings = pd.DataFrame(listing_results)
    df_listings.columns = [
        "home_id",
        "title",
        "postcode",
        "price",
        "street",
        "houseNumber",
        "city",
        "quarter",
        "latitude",
        "longitude",
        "livingSpace",
        "numberOfRooms",
        "balcony",
        "garden",
        "monthlyRate",
        "builtInKitchen",
        "home_url",
    ]

    return df_listings


def save_df_to_disk(df_listings, extraction_date):
    df_listings.to_excel(f"immo24_listings_{extraction_date}.xlsx", index=False)
    df_listings.to_csv(f"immo24_listings_{extraction_date}.csv", index=False)


def generate_map(df_listings_filtered):
    folium_map = \
        folium.Map(location=[52.516266, 13.377775],
                   zoom_start=13,
                   tiles='OpenStreetMap',
                   )

    for index, row in df_listings_filtered.iterrows():
        title = row["title"]
        price = row["price"]
        livingSpace = row["livingSpace"]
        latitude = row["latitude"]
        longitude = row["longitude"]
        street = row["street"]
        quarter = row["quarter"]
        numberOfRooms = int(row["numberOfRooms"])
        balcony = row["balcony"]
        garden = row["garden"]
        monthlyRate = row["monthlyRate"]
        builtInKitchen = row["builtInKitchen"]
        home_url = row["home_url"]

        html = f'''
        <b>Title</b>: {title}<br>
        <b>Price</b>: {price} <br>
        <b>LivingSpace</b>: {livingSpace} <br>
        <b>Street</b>: {street} <br>
        <b>Quarter</b>: {quarter} <br>
        <b>NumberOfRooms</b>: {numberOfRooms} <br>
        <b>Balcony</b>: {balcony} <br>
        <b>Garden</b>: {garden} <br>
        <b>MonthlyRate</b>: {monthlyRate} <br>
        <b>BuiltInKitchen</b>: {builtInKitchen} <br>
        <b>home_url</b>: <a href="{home_url}">{home_url}</a> <br>
        '''

        iframe = folium.IFrame(html,
                               width=450,
                               height=250)

        popup = folium.Popup(iframe,
                             max_width=450)

        if numberOfRooms == 1:
            color = "#cc3139"  # Red
        elif numberOfRooms == 2:
            color = "#39cc31"  # Green
        elif numberOfRooms >= 3:
            color = "#3139cc"  # Blue
        else:
            color = "#cc3139"

        folium.CircleMarker(
            location=[latitude, longitude],
            radius=3,
            popup=popup,
            color=color,
            fill=True).add_to(folium_map)

    now = datetime.now().strftime("%H:%M:%S")
    legend = f'Urutu Find a Home. Last update: {now}'

    title_html = '''
                 <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                 '''.format(legend)

    folium_map.get_root().html.add_child(folium.Element(title_html))

    folium_map.save("index.html")


def main():
    sys.stdout.write(str("Execution started...") + '\n')

    sys.stdout.write(str("Search pages...") + '\n')
    searchresults = get_immo24_search_pages()

    sys.stdout.write(str("Processing listings results...") + '\n')
    listing_results = get_listings_detailed_info(searchresults)
    df_listings_with_columns = get_df_with_columns(listing_results)
    df_listings = df_listings_with_columns

    sys.stdout.write(str("Save results in csv...") + '\n')
    save_df_to_disk(df_listings, extraction_date)

    sys.stdout.write(str("Generate map with location data...") + '\n')
    df_listings_filtered_latitude \
        = df_listings_with_columns[df_listings_with_columns['latitude'] != 'N/A']

    df_listings_filtered_longitude \
        = df_listings_filtered_latitude[df_listings_filtered_latitude['longitude'] != 'N/A']

    df_listings_filtered = df_listings_filtered_longitude

    generate_map(df_listings_filtered)
    sys.stdout.write(str("Map generated...") + '\n')

    total_listings = df_listings.shape[0]
    total_listings_in_map = df_listings_filtered.shape[0]
    listings_offset = total_listings - total_listings_in_map

    sys.stdout.write(str("Stats ") + '\n')
    sys.stdout.write(str(f"Total Listings: {total_listings}") + '\n')
    sys.stdout.write(str(f"Total Listings in Map: {total_listings_in_map}") + '\n')
    sys.stdout.write(str(f"Total Listings not in the Map: {listings_offset}") + '\n')
    sys.stdout.write(str("Execution finished...") + '\n')


if __name__ == "__main__":
    main()

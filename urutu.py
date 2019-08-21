import multiprocessing  as mp
import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

# Get all listings for Berlin
wohnung_url = []

# Time tracking
start_time = time.time()

for page in range(200):
    PAGE_URL \
        = (f'https://www.immobilienscout24.de/Suche/S-T/P-{page}/Wohnung-Miete/Berlin/Berlin')

    res = requests.get(PAGE_URL)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    expose_keys = []

    href_links = soup.findAll('a')
    for link in href_links:
        expose_keys.append(link['href'])

    expose_keys = pd.Series(expose_keys)
    expose_keys = expose_keys[expose_keys.str.startswith("/expose/")]
    expose_keys = expose_keys.unique()
    expose_keys = [w.replace('/expose/', '') for w in expose_keys]

    for key in expose_keys:
        wohnung_url.append((page, f'https://www.immobilienscout24.de/expose/{key}'))

elapsed_time = time.time() - start_time
fetching_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print(f'Fetching listings time: {fetching_time}')
print(f'Number of listings: {len(wohnung_url)}')

# DF with listings
df_url_listings = pd.DataFrame(wohnung_url)
df_url_listings.columns = ['page', 'url']


# Get content of the listings
def get_listings_data(listing):
    try:
        res = requests.get(listing)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
    except:
        print('Listing Non-extistent')

    try:
        listing_address = soup.find(class_='block font-nowrap print-hide')
        listing_address = listing_address.contents
    except:
        listing_address = 'N/A'

    try:
        listing_zip_district = soup.find(class_='zip-region-and-country')
        listing_zip_district = listing_zip_district.contents
    except:
        listing_zip_district = 'N/A'

    try:
        listing_kalte = soup.find(class_='is24qa-kaltmiete is24-value font-semibold')
        listing_kalte = listing_kalte.contents
    except:
        listing_kalte = 'N/A'

    try:
        listing_zimmer = soup.find(class_='is24qa-zi is24-value font-semibold')
        listing_zimmer = listing_zimmer.contents
    except:
        listing_zimmer = 'N/A'

    try:
        listing_flaeche = soup.find(class_='is24qa-flaeche is24-value font-semibold')
        listing_flaeche = listing_flaeche.contents
    except:
        listing_flaeche = 'N/A'

    try:
        listing_bezugsfrei = soup.find(class_='is24qa-bezugsfrei-ab grid-item three-fifths')
        listing_bezugsfrei = listing_bezugsfrei.contents
    except:
        listing_bezugsfrei = 'N/A'

    try:
        listing_etage = soup.find(class_='is24qa-etage grid-item three-fifths')
        listing_etage = listing_etage.contents
    except:
        listing_etage = 'N/A'

    try:
        listing_zimmer_ii = soup.find(class_='is24qa-zimmer grid-item three-fifths')
        listing_zimmer_ii = listing_zimmer_ii.contents
    except:
        listing_zimmer_ii = 'N/A'

    try:
        listing_kalte_ii = soup.find(class_='is24qa-kaltmiete grid-item three-fifths')
        listing_kalte_ii = listing_kalte_ii.contents
    except:
        listing_kalte_ii = 'N/A'

    try:
        listing_nebenkosten = soup.find(class_='is24qa-nebenkosten grid-item three-fifths')
        listing_nebenkosten = listing_nebenkosten.contents
    except:
        listing_nebenkosten = 'N/A'

    try:
        listing_heizkosten = soup.find(class_='is24qa-heizkosten grid-item three-fifths')
        listing_heizkosten = listing_heizkosten.contents
    except:
        listing_heizkosten = 'N/A'

    try:
        listing_gesamtmiete = soup.find(class_='is24qa-gesamtmiete grid-item three-fifths font-bold')
        listing_gesamtmiete = listing_gesamtmiete.contents
    except:
        listing_gesamtmiete = 'N/A'

    try:
        listing_genossenschaftsanteile = soup.find(class_='is24qa-kaution-o-genossenschaftsanteile')
        listing_genossenschaftsanteile = listing_genossenschaftsanteile.contents
    except:
        listing_genossenschaftsanteile = 'N/A'

    try:
        listing_baujahr = soup.find(class_='is24qa-baujahr grid-item three-fifths')
        listing_baujahr = listing_baujahr.contents
    except:
        listing_baujahr = 'N/A'

    try:
        listing_sanierung = soup.find(class_='is24qa-modernisierung-sanierung grid-item three-fifths')
        listing_sanierung = listing_sanierung.contents
    except:
        listing_sanierung = 'N/A'

    try:
        listing_objektzustand = soup.find(class_='is24qa-objektzustand grid-item three-fifths')
        listing_objektzustand = listing_objektzustand.contents
    except:
        listing_objektzustand = 'N/A'

    try:
        listing_ausstattung = soup.find(class_='is24qa-qualitaet-der-ausstattung grid-item three-fifths')
        listing_ausstattung = listing_ausstattung.contents
    except:
        listing_ausstattung = 'N/A'

    try:
        listing_heizungsart = soup.find(class_='is24qa-heizungsart grid-item three-fifths')
        listing_heizungsart = listing_heizungsart.contents
    except:
        listing_heizungsart = 'N/A'

    try:
        listing_energietraeger = soup.find(class_='is24qa-wesentliche-energietraeger grid-item three-fifths')
        listing_energietraeger = listing_energietraeger.contents
    except:
        listing_energietraeger = 'N/A'

    try:
        listing_energieausweis = soup.find(class_='is24qa-energieausweis grid-item three-fifths')
        listing_energieausweis = listing_energieausweis.contents
    except:
        listing_energieausweis = 'N/A'

    try:
        listing_energieausweistyp = soup.find(class_='is24qa-energieausweistyp grid-item three-fifths')
        listing_energieausweistyp = listing_energieausweistyp.contents
    except:
        listing_energieausweistyp = 'N/A'

    try:
        listing_endenergieverbrauch = soup.find(class_='is24qa-endenergieverbrauch grid-item three-fifths')
        listing_endenergieverbrauch = listing_endenergieverbrauch.contents
    except:
        listing_endenergieverbrauch = 'N/A'

    return np.array((
        listing_zip_district[0],
        listing_address[0],
        listing_kalte[0],
        listing_zimmer[0],
        listing_flaeche[0],
        listing_bezugsfrei[0],
        listing_etage[0],
        listing_zimmer_ii[0],
        listing_kalte_ii[0],
        listing_nebenkosten[0],
        listing_heizkosten[0],
        listing_gesamtmiete[0],
        listing_genossenschaftsanteile[0],
        listing_baujahr[0],
        listing_sanierung[0],
        listing_objektzustand[0],
        listing_ausstattung[0],
        listing_heizungsart[0],
        listing_energietraeger[0],
        listing_energieausweis[0],
        listing_energieausweistyp[0],
        listing_endenergieverbrauch[0],
        listing,
    ))


# DF object that will store the data
df_wohnung_data = pd.DataFrame()
wohnung_listings = df_url_listings['url'].unique()


# Main function with Multiprocessing to fetch all data
def main(df):
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(get_listings_data, wohnung_listings)
    df = df.append(pd.DataFrame(result))
    return df


# Time tracking
start_time = time.time()

# Call the main wrapper with multiprocessing
df_wohnung_data = main(df_wohnung_data)

elapsed_time = time.time() - start_time
fetching_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print(f'Fetching Time: {fetching_time}')

# Column and data adjustments
df_wohnung_data.columns = [
    'zip_district',
    'address',
    'kalte',
    'zimmer',
    'flaeche',
    'bezugsfrei',
    'etage',
    'zimmer_ii',
    'kalte_ii',
    'nebenkosten',
    'heizkosten',
    'gesamtmiete',
    'genossenschaftsanteile',
    'baujahr',
    'sanierung',
    'objektzustand',
    'ausstattung',
    'heizungsart',
    'energietraeger',
    'energieausweis',
    'energieausweistyp',
    'endenergieverbrauch',
    'listing_url',
]

df__district_ = df_wohnung_data['zip_district'].str.split(',', expand=True)
df__district_ = df__district_[[0, 1]]
df_wohnung_data[['zipcode_city', 'District']] = df__district_
df__zipcode = df_wohnung_data['zipcode_city'].str.split(' ', expand=True)
df__zipcode = df__zipcode[[0, 1]]
df_wohnung_data[['zipcode', 'city']] = df__zipcode
df_wohnung_data['kalte'] = df_wohnung_data['kalte'].str.replace('€','')
df_wohnung_data['kalte'] = df_wohnung_data['kalte'].str.replace(' ','')
df_wohnung_data['kalte'] = df_wohnung_data['kalte'].str.replace('.','')
df_wohnung_data['kalte'] = df_wohnung_data['kalte'].str.replace(',','.')
df_wohnung_data['kalte_ii'] = df_wohnung_data['kalte_ii'].str.replace('€','')
df_wohnung_data['kalte_ii'] = df_wohnung_data['kalte_ii'].str.replace(' ','')
df_wohnung_data['kalte_ii'] = df_wohnung_data['kalte_ii'].str.replace('.','')
df_wohnung_data['kalte_ii'] = df_wohnung_data['kalte_ii'].str.replace(',','.')
df_wohnung_data['gesamtmiete'] = df_wohnung_data['gesamtmiete'].str.replace('€','')
df_wohnung_data['gesamtmiete'] = df_wohnung_data['gesamtmiete'].str.replace(' ','')
df_wohnung_data['flaeche'] = df_wohnung_data['flaeche'].str.replace('m²','')
df_wohnung_data['flaeche'] = df_wohnung_data['flaeche'].str.replace(' ','')

# Save to disk in excel and csv
df_wohnung_data.to_excel("immo24_urutu.xlsx", index=False)
df_wohnung_data.to_csv("immo24_urutu.csv", index=False)

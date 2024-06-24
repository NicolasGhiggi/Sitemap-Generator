# Author: Nicolas Ghiggi
# Version: 12.06.2024

import os
import requests # type: ignore
from datetime import datetime
from bs4 import BeautifulSoup # type: ignore
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.parse import urljoin, urlparse

def is_valid_url(url, base_url):
    parsed_url = urlparse(url)
    return (parsed_url.scheme in ('http', 'https') and parsed_url.netloc == urlparse(base_url).netloc)

def extract_links_from_page(url, base_url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(base_url, href)
            if is_valid_url(full_url, base_url):
                links.add(full_url)
        return links
    except requests.RequestException as e:
        print(f'Error during request: {e}')
        return set()

def crawl_site(start_url):
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(start_url))
    to_visit = {start_url}
    visited = set()
    all_links = set()
    counter = 0

    while to_visit:
        counter += 1
        current_url = to_visit.pop()
        print(f'{counter} - I found: {current_url}')
        
        if current_url not in visited:
            visited.add(current_url)
            links = extract_links_from_page(current_url, base_url)
            all_links.update(links)
            to_visit.update(links - visited)
    
    return list(all_links)

def create_sitemap(links, filename):
    root = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'
    })
    
    for link in links:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = link.replace(' ', '%20')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'daily'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.5'
    
    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_str)

def split_links(links, chunk_size):
    return [links[i:i + chunk_size] for i in range(0, len(links), chunk_size)]

def main(website_url):
    max_links_per_file = 10000

    all_links = crawl_site(website_url)

    obj = datetime.now()
    download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    new_folder_path = os.path.join(download_path, f'sitemap_files_{obj.day:02}-{obj.month:02}-{obj.year}_{obj.hour:02}-{obj.minute:02}-{obj.second:02}')

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    link_chunks = split_links(all_links, max_links_per_file)
    num_digit = len(str(len(link_chunks)))

    for i, chunk in enumerate(link_chunks):
        filename = os.path.join(new_folder_path, f'sitemap_{i+1:0{num_digit}}.xml')
        create_sitemap(chunk, filename)
        print(f'Sitemap file {filename} successfully created')

if __name__ == '__main__':
    website_url = input('Enter the website URL: ')
    main(website_url)

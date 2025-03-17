# Wikipedia Car Crawler
# Author: Demetreous Stillman

# Run with: scrapy crawl wikipedia -o output.json
#           or
#           scrapy crawl wikipedia -o output.jl
#           scrapy crawl wikipedia -o output.csv


import scrapy
import os
import requests
#from scrapy.http import Request
#from urllib.parse import urlparse, unquote

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        #"https://en.wikipedia.org/wiki/Dodge_Challenger",
        "https://en.wikipedia.org/wiki/Category:Muscle_cars",
        "https://en.wikipedia.org/wiki/Category:Luxury_vehicles",
        "https://en.wikipedia.org/wiki/List_of_sports_cars",
        "https://en.wikipedia.org/wiki/List_of_battery_electric_vehicles",
        "https://en.wikipedia.org/wiki/List_of_pickup_trucks",
        "https://en.wikipedia.org/wiki/List_of_sport_utility_vehicles",
        "https://en.wikipedia.org/wiki/Category:Roadsters",
        "https://en.wikipedia.org/wiki/Category:Executive_cars",
        "https://en.wikipedia.org/wiki/List_of_motorcycle_manufacturers",
        "https://en.wikipedia.org/wiki/Yugo"
    ]

    visited_urls = {}

    def parse(self, response):
        title = response.css("span.mw-page-title-main::text").get()
        paragraphs = response.css("div.mw-parser-output > p")
        page_url = response.url

        content = []
        for paragraph in paragraphs:
            text = paragraph.css("::text").getall()
            bold_text = paragraph.css("b::text").getall()
            content.append("".join(text + bold_text))

        # Extract image sources, considering lazy-loaded images
        image_urls = response.css("table.infobox img::attr(src), div.mw-parser-output img::attr(src), table.infobox img::attr(data-src)").getall()

        # Convert relative URLs to full URLs (handle protocol-less URLs)
        image_urls = [
            response.urljoin(img) if img.startswith("/") else f"https:{img}" if img.startswith("//") else img
            for img in image_urls
        ]

        # Filter out small icons (e.g., logos, flags)
        filtered_images = [img for img in image_urls if "wikimedia.org" in img and "thumb" in img]

        # Limit the number of stored images
        images = filtered_images[:10]

        # Extract article links
        article_links = response.css("div.mw-parser-output > p a::attr(href)").getall()
        category_links = response.css("div.mw-category a::attr(href)").getall()
        list_links = response.css("div.mw-parser-output ul li a::attr(href)").getall()
        table_links = response.css("table a::attr(href)").getall()
        
        all_links = article_links + category_links + list_links + table_links
        links = [response.urljoin(link) for link in all_links if link.startswith("/wiki/") and ":" not in link]

        car_keywords = {
            'abarth', 'ac_cars', 'ac_propulsion', 'acura', 'aeolus', 'aion', 'aiways', 'alfa_romeo', 'alfina',
            'alphine', 'amc', 'apex_motors', 'arcfox', 'aston_martin', 'aspark', 'audi', 'aurus', 'baojun',
            'beaumont_(automobile)', 'bentley', 'bestune', 'bizzarrii', 'bmw', 'brabus', 'bugatti', 'buick',
            'byd', 'cadillac', 'changan', 'chery', 'chevrolet', 'chrysler', 'citroen', 'citroën_e', 'corvette',
            'daihatsu', 'daewoo', 'daimler', 'delorean', 'dongfeng', 'dodge', 'ds', 'edsel', 'ferrari',
            'fiat', 'fisker', 'foday', 'foton', 'ford', 'freightliner', 'gmc', 'geely', 'genesis', 'haval',
            'hennessey', 'holden_monaro', 'honda', 'hongqi', 'hummer', 'hyundai', 'infiniti', 'isuzu',
            'jaguar', 'jeep', 'jmc', 'kaiser', 'kia', 'lamborghini', 'land_rover', 'landwind', 'leopaard', 'lexus',
            'lincoln', 'lucid', 'lynk_&_co', 'mahindra', 'maserati', 'maybach', 'mazda', 'mclaren', 'mercedes', 'mercury',
            'mitsubishi', 'morgan', 'naveco', 'neta', 'nissan', 'oldsmobile', 'opel', 'orion', 'pagani', 'packard',
            'peugeot', 'plymouth', 'polestar', 'pontiac', 'porsche', 'qoros', 'ram', 'rely', 'renault',
            'rivian', 'rolls_royce', 'saturn', 'scion', 'seres', 'shelby', 'siata', 'sinogold', 'sinotruk',
            'skoda', 'studebaker', 'subaru', 'suzuki', 'tesla', 'toyota', 'triumph', 'vinfast',
            'volkswagen', 'volvo', 'wuling', 'yudo', 'zotye', 'zoyte', 'stelato', 'denza', 'yangwang', 'fangchengbao', 
            'exeed', 'icar', 'jetour', 'jaecoo', 'omoda', 'luxeed', 'vauxhall', 'anteros', 'acrimoto', 'polaris', 'harley_davidson',
            'motomel', 'zanella', 'braaap', 'thumpstar', 'Brammo', 'rokon', 'métisse', 'yugo', 'zastava', 'moskvitch'
        }

        excluded_keywords = {
            'disambiguation', 'platform', 'engine', 'factory', 'history', 'chassis', 'tv', 'amc+', 'turbine', 'paganism', 'audio', 
            'morgana', 'rama', 'rame', 'ramo', 'ramó', 'center', 'park', 'school', 'college', 'university', 'rail'
            'railway', 'station', 'airport', 'airfield', 'airstrip', 'heliport', 'helipad', 'port', 'harbor', 'harbour',
            'city', 'town', 'village', 'municipality', 'county', 'province', 'region', 'building', 'theatre', 'theater',
            'club', 'restaurant', 'bar', 'pub', 'cafe', 'hotel', 'motel', 'inn', 'resort', 'hostel', 'museum', 'gallery',
            'library', 'bookstore', 'shop', 'store', 'market', 'mall', 'supermarket', 'grocery', 'bakery', 'butcher',
            'estate', 'dodger', 'aeroplane', 'court', 'bay', 'centre', 'coliseum', 'football', 'soccer', 'stadium', 'arena',
            'field', 'park', 'garden', 'zoo', 'aquarium', 'aquatic', 'golf', 'course', 'track', 'synagogue', 'Lincolnshire',
            'network', 'system', 'software', 'hardware', 'firmware', 'channel', 'tournament', 'transmission', 'complex', 'river'
            'assembly', 'plant', 'michigan','opelousa', 'kingsford', 'rocket', 'tractor', 'fordism', 'aircraft', 'jet', 'helicopter'
            'pharmaceutical', 'band', 'chemical', 'air', 'random-access', 'random_access', 'video', 'game', 'ramb', 'mie_honda_heat'
            'fordwich', 'Rams', 'tunnel', 'architecture', 'yugoslav'
        }

        filtered_links = []
        for link in links:
            clean_link = link.split("#")[0]  # Remove fragment identifiers for filtering
            lower_link = clean_link.lower()
            for brand in car_keywords:
                if f"/wiki/{brand}" in lower_link and not any(excluded in lower_link for excluded in excluded_keywords):
                    filtered_links.append(link)
                    break

        images = filtered_images 

        yield {
            "title": title,
            "content": " ".join(content).strip(),
            "page_url": page_url,
            "links": filtered_links[:4000],  # Limit stored links
            "images": images[:10],  # Limit the number of images stored per page
        }

        for link in filtered_links[:4000]:  
            if link not in self.visited_urls:
                self.visited_urls[link] = True
                yield response.follow(link, callback=self.parse)

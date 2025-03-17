# Wikipedia Web Crawler for Vehicles  

## Overview  
This project is a web crawler designed to scrape vehicle-related Wikipedia pages, extracting relevant data efficiently. It identifies and follows links to car-related pages while filtering out non-relevant content.  

## Crawling Strategy  

The crawler starts with a predefined list of URLs that categorize different vehicle types, such as muscle cars and sports cars. It follows these steps:  

### 1. Initial Scraping  
- Parses each starting URL.  
- Extracts **titles, content, the link to the page, and links to images on the page**.  

### 2. Link Filtering & Navigation  
- Identifies related Wikipedia pages within the `/wiki/` namespace.  
- Follows links formatted as `/wiki/{brand}_{model}`, as most car-related Wikipedia pages use this structure.  
- Excludes certain words (e.g., “chassis,” “history”) to avoid non-relevant pages.  

### 3. Crawling Method  
- Uses a **depth-first search (DFS)** approach, parsing a page before following up to **4,000 relevant links**.  
- Tracks visited pages in a dictionary to prevent redundant scraping.  
- Limits **image storage to 10 per page** and **link storage to 4,000 per page** to improve efficiency.  

### 4. Output  
The crawler extracts and saves the following information for each page:  

- **Title** of the page  
- **Content** of the page  
- **Link** to the page  
- **Links to images** found on the page (up to 10 images per page)  

Extracted data is stored in the format of the user's choice (**CSV, JSON, or JL**).  

This strategy ensures **scalability** (by limiting the number of images and links) and **relevance** (by prioritizing automotive content).  

---

## Getting Started  

### Dependencies  
The project has only one dependency: **Scrapy**. Install it using:  

```bash
pip install scrapy
```

### Running the Crawler  

To run the web crawler and save the output in your preferred format, use the following command:  

```bash
scrapy crawl wikipediav -o output.<file_type>
```

Replace <file_type> with one of the supported formats:
- CSV: output.csv
- JSON: output.json
- JSON Lines: output.jl

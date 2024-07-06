import aiohttp
import xml.etree.ElementTree as ET

class ArxivHandler:
    def __init__(self, environment):
        self.base_url = "http://export.arxiv.org/api/query"
        self.environment = environment

    async def search_papers(self, query):
        params = {
            "search_query": query,
            "start": 0,
            "max_results": 5
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.text()
                    return self.parse_search_results(data)
                else:
                    return ["Error fetching search results."]

    async def view_trending_papers(self, category):
        params = {
            "search_query": f"cat:{category}",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": 0,
            "max_results": 5
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.text()
                    return self.parse_search_results(data)
                else:
                    return ["Error fetching trending papers."]

    def parse_search_results(self, data):
        results = []
        root = ET.fromstring(data)
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            paper = {
                "id": entry.find("{http://www.w3.org/2005/Atom}id").text.split('/')[-1],
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
                "authors": ", ".join([author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]),
                "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
            }
            results.append(paper)
        return results

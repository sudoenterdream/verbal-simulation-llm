import asyncio
from environment.environment import State
from services.arxiv_handler import ArxivHandler

class ArxivApp(State):
    def __init__(self, name):
        self.handler = ArxivHandler()
        actions = {
            "search_papers": {
                "next_state": "view_list_of_papers",
                "params": {
                    "query": "string"
                }
            },
            "view_trending_papers": {
                "next_state": "view_list_of_papers",
                "params": {
                    "category": "string"
                }
            },
            "exit_arxiv": {
                "next_state": "phone",
                "params": {}
            }
        }
        super().__init__(name, "", actions)

    async def get_sensory_information(self):
        self.sensory_information = "You are using the Arxiv app. You can search for papers or view trending papers."
        return self.sensory_information

    async def perform_action(self, action, params=None):
        if action == "search_papers" and params:
            query = params.get('query')
            if query:
                search_results = await self.handler.search_papers(query)
                next_state = ViewListOfPapers("view_list_of_papers", search_results, self.handler)
                self.handler.environment.add_state(next_state)
                return "view_list_of_papers"
        elif action == "view_trending_papers" and params:
            category = params.get('category')
            if category:
                trending_results = await self.handler.view_trending_papers(category)
                next_state = ViewListOfPapers("view_list_of_papers", trending_results, self.handler)
                self.handler.environment.add_state(next_state)
                return "view_list_of_papers"
        elif action == "exit_arxiv":
            return "phone"
        return await super().perform_action(action)


class ViewListOfPapers(State):
    def __init__(self, name, papers, handler):
        self.papers = papers
        self.handler = handler
        actions = {
            f"view_abstract_{i}": {
                "next_state": f"view_abstract_{i}",
                "params": {
                    "paper_id": paper["id"]
                }
            } for i, paper in enumerate(papers)
        }
        actions["exit_list"] = {
            "next_state": "arxiv_app",
            "params": {}
        }
        super().__init__(name, "", actions)

    async def get_sensory_information(self):
        paper_list = "\n".join([f"{i+1}. {paper['title']}" for i, paper in enumerate(self.papers)])
        self.sensory_information = f"List of Papers:\n\n{paper_list}\n\nChoose a paper to view abstract or exit."
        return self.sensory_information

    async def perform_action(self, action, params=None):
        if action.startswith("view_abstract_"):
            paper_id = params.get('paper_id')
            paper = next((p for p in self.papers if p["id"] == paper_id), None)
            if paper:
                next_state = ViewAbstract(f"view_abstract_{paper_id}", paper, self.handler)
                self.handler.environment.add_state(next_state)
                return f"view_abstract_{paper_id}"
        elif action == "exit_list":
            return "arxiv_app"
        return await super().perform_action(action)


class ViewAbstract(State):
    def __init__(self, name, paper, handler):
        self.paper = paper
        self.handler = handler
        actions = {
            "read_full_paper": {
                "next_state": name,
                "params": {
                    "paper_id": paper["id"]
                }
            },
            "exit_abstract": {
                "next_state": "view_list_of_papers",
                "params": {}
            }
        }
        super().__init__(name, "", actions)

    async def get_sensory_information(self):
        self.sensory_information = f"Title: {self.paper['title']}\nAuthors: {self.paper['authors']}\n\nAbstract:\n{self.paper['abstract']}"
        return self.sensory_information

    async def perform_action(self, action, params=None):
        if action == "read_full_paper":
            await asyncio.sleep(600)  # Simulate reading full paper
            return self.name
        elif action == "exit_abstract":
            await asyncio.sleep(60)  # Simulate reading abstract
            return "view_list_of_papers"
        return await super().perform_action(action)

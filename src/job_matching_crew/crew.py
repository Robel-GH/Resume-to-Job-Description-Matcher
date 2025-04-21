from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from langchain_community.tools import DuckDuckGoSearchRun
import pdfplumber
import yaml
import time
import os
from dotenv import load_dotenv

from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  SerperDevTool
)

from litellm.exceptions import RateLimitError

# Load environment variables
load_dotenv()

def llm_with_retry(llm_func, max_attempts: int = 5):
    """
    Wrap an LLM call function to handle RateLimitError with retries.
    """
    def wrapped(*args, **kwargs):  # Changed to accept both args and kwargs
        for attempt in range(max_attempts):
            try:
                return llm_func(*args, **kwargs)  # Pass through all arguments
            except RateLimitError as e:
                retry_after = getattr(e, "retry_delay", None)
                wait = retry_after.seconds if retry_after else 2 ** attempt
                print(f"[LLM rate limit] retry {attempt+1}/{max_attempts} in {wait}s…")
                time.sleep(wait)
        raise RuntimeError(f"LLM rate-limit: exceeded {max_attempts} retries")
    return wrapped

@CrewBase
class JobMatchingCrew():
    """JobMatchingCrew crew"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.agents_config = 'config/agents.yaml'
        self.tasks_config = 'config/tasks.yaml'

        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.read_resume = FileReadTool(file_path='./src/job_matching_crew/data/inputs/dummy_cv.md')
        # self.semantic_search_resume = FileReadTool(file_path='./robel-gh-resume.pdf')

        self.llm = LLM(
            provider="google",  # Changed from "gemini" to "google"
            model=os.getenv("MODEL"),  # Use valid model name
            api_key=os.getenv("GEMINI_API_KEY")  # Ensure this matches your .env
        )

        self.llm.call = llm_with_retry(self.llm.call, max_attempts=5)

    @agent
    def cv_reader_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader_agent'],
            tools=[self.scrape_tool, self.search_tool, self.read_resume],
            llm=self.llm,
            verbose=True
        )

    @agent
    def job_parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_parser_agent'],
            tools=[self.scrape_tool, self.search_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def matcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher_agent'],
            llm=self.llm,
            verbose=True
        )

    @task
    def cv_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['cv_analysis_task'],
            output_file='./src/job_matching_crew/data/outputs/cv_report.md'
        )

    @task
    def job_parsing_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_parsing_task'],
            output_file='./src/job_matching_crew/data/outputs/job_report.md'
        )

    @task
    def matching_task(self) -> Task:
        return Task(
            config=self.tasks_config['matching_task'],
            context=[self.cv_analysis_task(), self.job_parsing_task()],
            output_file='./src/job_matching_crew/data/outputs/match_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JobMatchingCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

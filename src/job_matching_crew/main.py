#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from job_matching_crew.crew import JobMatchingCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs={
        "cv_path": "./src/job_matching_crew/data/inputs/dummy_cv.md",
        "job_urls": ["https://vuejobs.com/jobs/ralabs-senior-vue-js-engineer", "https://vuejobs.com/jobs/mozilla-full-stack-software-engineer",
                     "https://vuejobs.com/jobs/campaign-nucleus-2-ui-designer-frontend-dev-vue-js",
                     "https://vuejobs.com/jobs/trooptravel-front-end-engineer-vue3"]
    }
    
    try:
        JobMatchingCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs={
        "cv_path": "./src/job_matching_crew/data/inputs/dummy_cv.md",
        "job_urls": ["https://vuejobs.com/jobs/ralabs-senior-vue-js-engineer", 
                     "https://vuejobs.com/jobs/mozilla-full-stack-software-engineer",
                      "https://vuejobs.com/jobs/campaign-nucleus-2-ui-designer-frontend-dev-vue-js",
                     "https://vuejobs.com/jobs/trooptravel-front-end-engineer-vue3"]
    }
    try:
        JobMatchingCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        JobMatchingCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs={
        "cv_path": "./src/job_matching_crew/data/inputs/dummy_cv.md",
        "job_urls": ["https://vuejobs.com/jobs/ralabs-senior-vue-js-engineer", 
                     "https://vuejobs.com/jobs/mozilla-full-stack-software-engineer",
                      "https://vuejobs.com/jobs/campaign-nucleus-2-ui-designer-frontend-dev-vue-js",
                     "https://vuejobs.com/jobs/trooptravel-front-end-engineer-vue3"]
    }
    try:
        JobMatchingCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel
from . import GitRepository


class PullRequestReviewer(ABC):
    def __init__(self, llm: BaseChatModel, repository: GitRepository):
        self.llm = llm
        self.repository = repository

    @abstractmethod
    def review(self, pull_request_number: int) -> str:
        pass

    def _get_pull_request_content(self, pull_request_number: int) -> str:
        pr = self.repository.get_pull_request(pull_request_number)
        changes = self.repository.get_pull_request_changes(pull_request_number)
        header_content = f"Pull request title: {pr.title}"
        change_content = "\n\n\n".join([f"File: {change.file_path}\n{change.patch}" for change in changes])
        pr_content = f"{header_content}\n\nPull request changes:\n{change_content}"
        return pr_content

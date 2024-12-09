from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class FileContent:
    def __init__(self, file_path: str, content: str):
        self.file_path: str = file_path
        self.content: str  = content


class FilePatch:
    def __init__(self, file_path: str, patch: str):
        self.file_path: str = file_path
        self.patch: str = patch


class PullRequest:
    def __init__(self,
                 pull_request_number: int,
                 title: str,
                 description: str,
                 source_branch_label: str,
                 target_branch_label: str,
                 created_by: str,
                 created_at: datetime):
        self.id: int = pull_request_number
        self.title: str = title
        self.description: str = description
        self.source_branch_label = source_branch_label
        self.target_branch_label = target_branch_label
        self.created_by = created_by
        self.created_at = created_at


class GitRepository(ABC):
    @abstractmethod
    def get_files(self) -> List[FileContent]:
        pass

    @abstractmethod
    def get_pull_requests(self) -> List[PullRequest]:
        pass

    @abstractmethod
    def get_pull_request(self, pull_request_number: int) -> PullRequest:
        pass

    @abstractmethod
    def get_pull_request_changes(self, pull_request_number: int) -> List[FilePatch]:
        pass

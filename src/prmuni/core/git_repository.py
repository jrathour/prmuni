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
                 head_sha: str,
                 source_branch_label: str,
                 target_branch_label: str,
                 created_by: str,
                 created_at: datetime):
        self.id: int = pull_request_number
        self.title: str = title
        self.description: str = description
        self.head_sha: str = head_sha
        self.source_branch_label: str = source_branch_label
        self.target_branch_label: str = target_branch_label
        self.created_by: str = created_by
        self.created_at: datetime = created_at


class GitRepository(ABC):
    @abstractmethod
    def get_pull_requests(self) -> List[PullRequest]:
        pass

    @abstractmethod
    def get_pull_request_changes(self, pull_request: PullRequest) -> List[FilePatch]:
        pass

    # @abstractmethod
    # def get_repository_content_at_pull_request_head(self, pull_request: PullRequest) -> List[FileContent]:
    #     pass

from typing import List, Tuple
from urllib.parse import urlparse
from ghapi.all import GhApi, paged
from ..core import GitRepository, FileContent, PullRequest, FilePatch


class GitHubRepository(GitRepository):
    def __init__(self,repository_url: str,token: str):
        self.github_token: str = token
        self.owner, self.repo = GitHubRepository._parse_repository_url(repository_url)
        self.api = GhApi(
            owner=self.owner,
            repo=self.repo,
            token=self.github_token
        )

    def get_files(self) -> List[FileContent]:
        pass

    def get_pull_requests(self) -> List[PullRequest]:
        pull_requests = []
        pages = paged(self.api.pulls.list)
        for page in pages:
            for item in page:
                pr = PullRequest(
                    pull_request_number=item.number,
                    title=item.title,
                    description=item.body,
                    source_branch_label=item.head.label,
                    target_branch_label=item.base.label,
                    created_by=item.user.login,
                    created_at=item.created_at
                )
                pull_requests.append(pr)
        return pull_requests

    def get_pull_request(self, pull_request_number: int) -> PullRequest:
        item = self.api.pulls.get(pull_number=pull_request_number)
        pr = PullRequest(
            pull_request_number=item.number,
            title=item.title,
            description=item.body,
            source_branch_label=item.head.label,
            target_branch_label=item.base.label,
            created_by=item.user.login,
            created_at=item.created_at
        )
        return pr

    def get_pull_request_changes(self, pull_request_number: int) -> List[FilePatch]:
        patches = []
        pages = paged(self.api.pulls.list_files, pull_number=pull_request_number)
        for page in pages:
            for item in page:
                patch = FilePatch(file_path=item.filename, patch=item.patch)
                patches.append(patch)
        return patches

    @staticmethod
    def _parse_repository_url(url: str) -> Tuple[str,str]:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 2:
            owner: str = path_parts[0]
            repo: str = path_parts[1]
            return owner, repo
        else:
            raise ValueError("Invalid github repository url. "
                             "It must be in format https://github.com/<owner>/<repository name>")

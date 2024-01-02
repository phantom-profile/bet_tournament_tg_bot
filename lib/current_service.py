import dataclasses
from datetime import datetime

from lib.backend_client import BackendClient
from lib.base_client import CacheService


@dataclasses.dataclass
class Tournament:
    id: int
    members_count: int
    name: str
    members_limit: int
    member_cost: int
    duration: int
    created_at: datetime
    starts_at: datetime
    members_ids: set[str]

    @classmethod
    def from_dict(self, params: dict):
        return Tournament(
            id=params['id'],
            members_count=params['members_count'],
            name=params['name'],
            members_limit=params['members_limit'],
            member_cost=params['member_cost'],
            duration=params['duration'],
            created_at=datetime.fromisoformat(params['created_at']),
            starts_at=datetime.fromisoformat(params['starts_at']),
            members_ids=set(params['members_ids'])
        )

    def is_member(self, user_id) -> bool:
        return str(user_id) in self.members_ids

    def is_full(self) -> bool:
        return self.members_count >= self.members_limit


class CurrentTournamentsService:
    def __init__(self):
        self.client = BackendClient()
        self.cacher = CacheService()
        self.cacher.set_key('current-active-tournament')

    def call(self) -> dict[str, Tournament | None]:
        response = self.client.get_current_tournaments()
        if not response.is_successful:
            return self._response(None, response.body)

        if not response.body['open_tournament_exists']:
            return self._response(None, None)

        return self._response(self._build_tournament(response.body), None)

    def _response(self, tournament, errors):
        return {'tournament': tournament, 'errors': errors}

    def _build_tournament(self, response):
        tournament_params = response['tournaments'][0]
        ids = []
        for member in tournament_params['members']:
            if member['status'] != 'declined':
                ids.append(member['tg_id'])
        return Tournament.from_dict(tournament_params | {'members_ids': ids})

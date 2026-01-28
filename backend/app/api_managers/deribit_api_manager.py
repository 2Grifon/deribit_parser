import httpx
from app.core.api_manager.base import ApiManager


class DeribitAPIManager(ApiManager):
    base_url = "https://www.deribit.com/api/v2/"

    def get_index_price(self, currency: str) -> float:
        endpoint = f"{self.base_url}public/get_index_price"

        params = {"index_name": f"{currency}_usd"}
        response = httpx.get(endpoint, params=params)

        self.check_status_code(response)
        data = response.json()

        return data["result"]["index_price"]

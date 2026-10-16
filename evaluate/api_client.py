import requests


class TutorIAClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.chat_url = f"{self.base_url}/api/chat"

    def create_chat(self) -> int:
        response = requests.post(
            f"{self.chat_url}/",
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return data["id"]

    def send_message(self, chat_id: int, content: str) -> str:
        response = requests.post(
            f"{self.chat_url}/{chat_id}",
            json={"content": content},
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict) and "answer" in data:
            return data["answer"]

        return data

    def delete_chat(self, chat_id: int) -> None:
        response = requests.delete(
            f"{self.chat_url}/{chat_id}",
            timeout=10,
        )
        response.raise_for_status()

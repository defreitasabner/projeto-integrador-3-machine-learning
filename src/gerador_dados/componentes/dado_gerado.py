from datetime import datetime
from typing import Dict, Any


class DadoGerado:
    def __init__(self, 
        user_id: str, 
        device_id: str, 
        ipv4: str, 
        latitude: float, 
        longitude: float, 
        timestamp: datetime, 
        is_fraude: bool
    ):
        self.user_id = user_id
        self.device_id = device_id
        self.ipv4 = ipv4
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.is_fraude = is_fraude

    @classmethod
    def from_dict(cls, dados: Dict[str, Any]) -> "DadoGerado":
        if type(dados["timestamp"]) is str:
            dados["timestamp"] = datetime.fromisoformat(dados["timestamp"])
        return cls(
            user_id = dados["user_id"],
            device_id = dados["device_id"],
            ipv4 = dados["ipv4"],
            latitude = dados["latitude"],
            longitude = dados["longitude"],
            timestamp = dados["timestamp"],
            is_fraude = dados["is_fraude"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "device_id": self.device_id,
            "ipv4": self.ipv4,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "is_fraude": self.is_fraude,
        }
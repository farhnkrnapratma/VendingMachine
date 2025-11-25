"""Klien API untuk berkomunikasi dengan backend FSA"""
import requests
from typing import Dict, Any, Optional, List


class FSAClient:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BobaCLI/1.0.0'
        })

    def _get(self, endpoint: str) -> Dict[str, Any]:
        """Lakukan request GET"""
        response = self.session.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Lakukan request POST"""
        response = self.session.post(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    def get_info(self) -> Dict[str, Any]:
        """Dapatkan info konfigurasi FSA"""
        return self._get('/fsm/info')

    def get_states(self) -> List[Dict[str, Any]]:
        """Dapatkan semua state"""
        return self._get('/fsm/states')

    def get_state_details(self, state: str) -> Dict[str, Any]:
        """Dapatkan detail untuk state tertentu"""
        return self._get(f'/fsm/states/{state}')

    def process_string(self, input_string: str) -> Dict[str, Any]:
        """Proses string input melalui FSA"""
        return self._post('/fsm/process', {'inputString': input_string})

    def execute_transition(self, current_state: str, symbol: str) -> Dict[str, Any]:
        """Eksekusi transisi tunggal"""
        return self._post('/fsm/transition', {
            'currentState': current_state,
            'symbol': symbol
        })

    def validate_transition(self, from_state: str, symbol: str, to_state: str) -> Dict[str, Any]:
        """Validasi transisi"""
        return self._post('/fsm/validate', {
            'fromState': from_state,
            'symbol': symbol,
            'toState': to_state
        })

    def health_check(self) -> bool:
        """Cek apakah API dapat dijangkau"""
        try:
            self._get('/')
            return True
        except:
            return False

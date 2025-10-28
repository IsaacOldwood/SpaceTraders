from time import sleep
import requests


class Ship:
    def __init__(self, ship_id, api_key):
        self.API_KEY = api_key
        self.headers = {"Authorization": f"Bearer {self.API_KEY}"}
        self.ship_id = ship_id

    def mine(self):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/extract"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def jettison_cargo(self, item_id, units: int):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/jettison"
        payload = {"symbol": item_id, "units": units}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def navigate(self, waypoint):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/navigate"
        payload = {"waypointSymbol": waypoint}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def orbit(self):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/orbit"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def dock(self):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/dock"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def refuel(self):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/refuel"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def dock_fuel_orbit(self):
        self.dock()
        self.refuel()
        return self.orbit()

    def contract_deliver(self, contract_id, item_id, units: int):
        url = f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/deliver"
        payload = {"shipSymbol": self.ship_id, "tradeSymbol": item_id, "units": units}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def list_cargo(self):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/cargo"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def sell_cargo(self, item_id, units: int):
        url = f"https://api.spacetraders.io/v2/my/ships/{self.ship_id}/sell"
        payload = {"symbol": item_id, "units": units}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def auto_mine(self, keep_list: list[str], max_mines: int = 3):
        mine_info = None

        for mine_no in range(0, max_mines + 1):
            mine_info = self.mine()

            check_cargo = True
            mine_yield = mine_info["data"]["extraction"]["yield"]
            mine_symbol = mine_yield["symbol"]
            mine_units = mine_yield["units"]
            if mine_symbol not in keep_list:
                print(f"Mined {mine_symbol}, not in keep list, jettisoning...")
                self.jettison_cargo(mine_symbol, mine_units)
                sleep(1)
                check_cargo = False
            else:
                print(f"Mined {mine_units}x {mine_symbol}")

            if mine_no == max_mines:
                return mine_info

            if (
                check_cargo
                and mine_info["data"]["cargo"]["capacity"]
                == mine_info["data"]["cargo"]["units"]
            ):
                print("Cargo full, stopping auto-mine")
                return mine_info

            cooldown = mine_info["data"]["cooldown"]["remainingSeconds"]
            for i in range(cooldown, 0, -1):
                if i == 1:
                    print("\rCooldown complete          ")
                else:
                    print(f"\rWaiting {i}s for cooldown ", sep="", end="", flush=True)
                sleep(1.05)

        return mine_info

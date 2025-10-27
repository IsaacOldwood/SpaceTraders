import requests
from decouple import config
import json
from time import sleep

class Game:
    def __init__(self, api_key):
        self.API_KEY = api_key
        self.headers = {"Authorization": f"Bearer {self.API_KEY}"}

    def my_agent(self):
        url = "https://api.spacetraders.io/v2/my/agent"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def waypoint_info(self, waypoint: str):
        system = waypoint.split("-")[0] + "-" + waypoint.split("-")[1]
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def waypoint_market_info(self, waypoint: str):
        system = waypoint.split("-")[0] + "-" + waypoint.split("-")[1]
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/market"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def search_system_trait(self, system: str, trait: str):
        # If waypoint, filter for system id
        if system.count("-") == 2:
            system = system.split("-")[0] + "-" + system.split("-")[1]
        url = (
            f"https://api.spacetraders.io/v2/systems/{system}/waypoints?traits={trait}"
        )
        r = requests.get(url, headers=self.headers)
        return r.json()

    def search_system_type(self, system: str, waypoint_type: str):
        # If waypoint, filter for system id
        if system.count("-") == 2:
            system = system.split("-")[0] + "-" + system.split("-")[1]
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints?type={waypoint_type}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def list_contracts(self):
        url = "https://api.spacetraders.io/v2/my/contracts"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def accept_contract(self, contract_id):
        url = f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def orbit_ship(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/orbit"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def dock_ship(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/dock"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def refuel_ship(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/refuel"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def mine(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/extract"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def list_shipyard(self, waypoint: str):
        system = waypoint.split("-")[0] + "-" + waypoint.split("-")[1]
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/shipyard"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def my_ships(self):
        url = "https://api.spacetraders.io/v2/my/ships"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def buy_ship(self, waypoint, ship_type):
        url = "https://api.spacetraders.io/v2/my/ships"
        payload = {"shipType": ship_type, "waypointSymbol": waypoint}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def navigate(self, waypoint, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/navigate"
        payload = {"waypointSymbol": waypoint}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def sell(self, ship_id, item_id, units: int):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/sell"
        payload = {"symbol": item_id, "units": units}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def list_ship_cargo(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/cargo"
        r = requests.get(url, headers=self.headers)
        return r.json()
    
    def auto_mine(self, ship_id):
        mine_info = self.mine(ship_id)
        cooldown = mine_info["data"]["cooldown"]["remainingSeconds"]
        print(f"Waiting {cooldown}s for cooldown")
        sleep(cooldown + 1)
        return self.mine(ship_id)

def main():
    game = Game(config("API_KEY"))
    # url = ""
    # output = game.my_agent()
    hq = "X1-TK43-A1"

    # output = game.list_contracts()
    contract_waypoint = "X1-TK43-H51"
    # con_id = "cmh9aulp469psuo70c1mp587i"
    # output = game.accept_contract(con_id)

    # output = game.search_waypoint(hq, "SHIPYARD")
    moon = "X1-TK43-H52"

    # output = game.waypoint_info(contract_waypoint)

    # output = game.list_shipyard(moon)

    # output = game.buy_ship(moon, "SHIP_MINING_DRONE")
    mine_drone_id = "MOONFLASK-3"
    # output = game.search_system_type(hq, "ENGINEERED_ASTEROID")
    asteroid_symbol = "X1-TK43-DX5F"

    # output = game.orbit_ship(mine_drone_id)

    # output = game.navigate(asteroid_symbol, mine_drone_id)

    # output = game.dock_ship(mine_drone_id)

    # output = game.refuel_ship(mine_drone_id)

    # output = game.orbit_ship(mine_drone_id)

    output = game.mine(mine_drone_id)

    # output = game.list_ship_cargo(mine_drone_id)

    # output = game.waypoint_market_info(contract_waypoint)
    # import: ALUMINUM_ORE, IRON_ORE, COPPER_ORE

    # output = game.sell(mine_drone_id, "ICE_WATER", 2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

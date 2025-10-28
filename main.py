import requests
from decouple import config
import json
from src.ship import Ship


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

    def list_ships(self):
        url = "https://api.spacetraders.io/v2/my/ships"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def ship_info(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def ship_nav_info(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/nav"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def accept_contract(self, contract_id):
        url = f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept"
        r = requests.post(url, headers=self.headers)
        return r.json()

    def list_shipyard(self, waypoint: str):
        system = waypoint.split("-")[0] + "-" + waypoint.split("-")[1]
        url = f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/shipyard"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def buy_ship(self, waypoint, ship_type):
        url = "https://api.spacetraders.io/v2/my/ships"
        payload = {"shipType": ship_type, "waypointSymbol": waypoint}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()


def main():
    game = Game(config("API_KEY"))
    # url = ""
    # output = game.my_agent()
    # output = game.list_ships()
    main_ship_id = "MOONFLASK-1"
    main_ship = Ship(main_ship_id, config("API_KEY"))
    hq = "X1-TK43-A1"

    # output = game.list_contracts()
    # Details: COPPER_ORE - 65
    contract_waypoint = "X1-TK43-H51"
    con_id = "cmh9aulp469psuo70c1mp587i"
    # output = game.accept_contract(con_id)

    # output = game.search_waypoint(hq, "SHIPYARD")
    moon = "X1-TK43-H52"

    # output = game.waypoint_info(contract_waypoint)

    # output = game.list_shipyard(moon)

    # output = game.buy_ship(moon, "SHIP_MINING_DRONE")
    mine_drone_id = "MOONFLASK-3"
    # output = game.search_system_type(hq, "ENGINEERED_ASTEROID")
    asteroid_symbol = "X1-TK43-DX5F"

    # output = game.navigate(asteroid_symbol, main_ship_id)
    # output = game.ship_info(main_ship_id)
    # output = game.dock_ship(mine_drone_id)

    # output = game.refuel_ship(mine_drone_id)

    # output = game.orbit_ship(main_ship_id)

    # output = game.mine(mine_drone_id)

    # output = game.list_ship_cargo(mine_drone_id)

    # output = game.waypoint_market_info(contract_waypoint)
    # contract import: ALUMINUM_ORE, IRON_ORE, COPPER_ORE

    # main_ship.navigate(contract_waypoint)

    # main_ship.dock()
    # main_ship.refuel()
    # output = main_ship.list_cargo()

    # main_ship.sell_cargo("IRON_ORE", 21)
    # main_ship.sell_cargo("ALUMINUM_ORE", 11)
    # output = main_ship.contract_deliver(con_id, "COPPER_ORE", 5)

    # main_ship.orbit()
    # output = main_ship.navigate(asteroid_symbol)

    contract_waypoint_keep_list = ["ALUMINUM_ORE", "IRON_ORE", "COPPER_ORE"]
    main_ship.auto_mine(contract_waypoint_keep_list, 10)

    # print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

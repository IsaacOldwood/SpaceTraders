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

    def jettison_cargo(self, ship_id, item_id, units: int):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/jettison"
        payload = {"symbol": item_id, "units": units}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def contract_deliver(self, contract_id, ship_id, item_id, units: int):
        url = f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/deliver"
        payload = {"shipSymbol": ship_id, "tradeSymbol": item_id, "units": units}
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def list_ship_cargo(self, ship_id):
        url = f"https://api.spacetraders.io/v2/my/ships/{ship_id}/cargo"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def dock_fuel_orbit(self, ship_id):
        self.dock_ship(ship_id)
        self.refuel_ship(ship_id)
        return self.orbit_ship(ship_id)

    def auto_mine(self, ship_id, keep_list: list[str], max_mines: int = 3):
        mine_info = None

        for mine_no in range(0, max_mines + 1):
            mine_info = self.mine(ship_id)

            check_cargo = True
            mine_yield = mine_info["data"]["extraction"]["yield"]
            mine_symbol = mine_yield["symbol"]
            mine_units = mine_yield["units"]
            if mine_symbol not in keep_list:
                print(f"Mined {mine_symbol}, not in keep list, jettisoning...")
                self.jettison_cargo(ship_id, mine_symbol, mine_units)
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


def main():
    game = Game(config("API_KEY"))
    # url = ""
    # output = game.my_agent()
    # output = game.list_ships()
    main_ship_id = "MOONFLASK-1"
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

    # output = game.sell(mine_drone_id, "IRON_ORE", 2)
    # output = game.jettison_cargo(mine_drone_id, "QUARTZ_SAND", 2)
    # output = game.contract_deliver(con_id, mine_drone_id, "COPPER_ORE", 5)

    contract_waypoint_keep_list = ["ALUMINUM_ORE", "IRON_ORE", "COPPER_ORE"]
    output = game.auto_mine(main_ship_id, contract_waypoint_keep_list)

    # output = game.ship_nav_info(main_ship_id)
    # output = game.dock_fuel_orbit(main_ship_id)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

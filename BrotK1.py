import hlt
import logging
from collections import OrderedDict
game = hlt.Game("SentdeBot-V1")
logging.info("Starting SentdeBot")

while True:
    game_map = game.update_map()
    command_queue = []
    goal_planet = []
    
    for ship in game_map.get_me().all_ships():
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        team_ships = game_map.get_me().all_ships()
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]
        index = 0
        # If there are any empty planets, let's try to mine!
        if len(closest_empty_planets) > 0:
            target_planet = closest_empty_planets[index]
            if ship.can_dock(target_planet) and target_planet not in goal_planet :
                goal_planet.append((target_planet))
                index = index + 4
                ignore_ships=False
                
                command_queue.append(ship.dock(target_planet))
                
            elif ship.can_dock(target_planet) and target_planet not in goal_planet :
                command_queue.append(ship.dock(target_planet))
                goal_planet.append((target_planet))
                ignore_ships=False
                index = index + 1
                
                
                
                
            else:
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        # FIND SHIP TO ATTACK!
        elif len(closest_enemy_ships) > 0 and planet.all_docked_ships() >0 :
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                        ship.closest_point_to(target_ship),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)
        else:
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)


    game.send_command_queue(command_queue)
    # TURN END
# GAME END

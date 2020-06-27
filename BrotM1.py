import hlt
import logging
from collections import OrderedDict
game = hlt.Game("Apollyon")
logging.info("Starting Apollyon")
i = -1
while True:
    game_map = game.update_map()
    command_queue = []
    goal_planets=[]
    i = i+1
#    for planet in goal_planets:
 #       if (plane.is_owned())and(planet.all_docked_ships in team_ships):
  #          goal_planets.remove(planet)
          
    
    for ship in game_map.get_me().all_ships():
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue
        if i>80 :
            goal_planets=[]

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]
        closest_owned_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]

        team_ships = game_map.get_me().all_ships()
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

       
            
        

        # If there are any empty planets, let's try to mine!
        if (len(closest_empty_planets) > 0)and(closest_empty_planets[0] not in goal_planets):
            target_planet = closest_empty_planets[0]
            goal_planets.append(target_planet)
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
                
            else:
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif (len(closest_empty_planets) <1 ):
            for planet in closest_owned_planets:
                if (planet.all_docked_ships[0]not in team_ships )and(len(planet.all_docked_ships)< 3):
                    target_ship1 = planet.all_docked_ships[0]
                    navigate_command = ship.navigate(
                        ship.closest_point_to(target_ship1),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)
                        
            
        # FIND SHIP TO ATTACK!
        
        elif len(closest_enemy_ships) > 0:
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                        ship.closest_point_to(target_ship),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    # TURN END
# GAME END

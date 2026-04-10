# turtle_scanner

## Partie 1
Le noeud spawn_target.py permet de creer une deuxieme tortue appelee turtle_target avec le service /spawn.
Les coordonnees sont generees aleatoirement entre 1 et 10 pour x et y.
Apres le spawn, les coordonnees de la cible sont affichees dans le terminal.

### Screenshot

![Partie 1](images/partie1_spawn.png)

## Partie 2
Le noeud turtle_scanner_node.py récupère la pose de turtle1 et de turtle_target avec les topics turtle1/pose et /turtle_target/pose.
Les poses sont stockées dans self.pose_scanner et self.pose_target.

Verification :


ros2 topic echo /turtle1/pose

ros2 topic echo /turtle_target/pose

## Partie 3
Les valeurs choisies pour la commande sont Kp_ang = 4.0 et Kp_lin = 1.5.

Avec Kp_ang = 2.0, la tortue tourne plus lentement vers le waypoint.

Avec Kp_ang = 6.0, la tortue tourne plus vite et le mouvement devient plus brusque.

Avec Kp_lin = 0.8, la tortue avance plus lentement.

Avec Kp_lin = 3.0, la tortue avance plus vite et peut depasser le waypoint.

## Partie 4
Le nœud détecte la cible en calculant la distance entre turtle1 et turtle_target.

Un rayon de détection de 1.5 a été utilisé.

Quand la distance devient plus petite que ce rayon, le balayage s'arrête et la tortue ne bouge plus.

Le topic /target_detected publie False tant que la cible n'est pas détectée, puis True quand la cible est trouvée.

La détection a été vérifiée avec la commande ros2 topic echo /target_detected.


## Partie 5

Un package turtle_interfaces a été créé avec le service ResetMission.

Le service /reset_mission permet de relancer une mission sans redémarrer les nœuds.

Quand le service est appelé, l'ancienne cible est supprimée, une nouvelle cible est créée, puis le balayage recommence depuis le début.

Le service peut utiliser une position aléatoire avec random_target = true ou une position fixe avec les coordonnées target_x et target_y.

Vérification

ros2 interface show turtle_interfaces/srv/ResetMission

ros2 service call /reset_mission turtle_interfaces/srv/ResetMission "{target_x: 0.0, target_y: 0.0, random_target: true}"

ros2 service call /reset_mission turtle_interfaces/srv/ResetMission "{target_x: 3.0, target_y: 8.0, random_target: false}"

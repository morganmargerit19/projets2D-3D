# Référentiel, raccordement et hypothèses

## État cible documentaire

Les dix photographies présentent un jardin aménagé en usage : gravier gris, dallage gris, bandes de galets clairs, pots fleuris, haies, pelouse, abri bas de piscine, façades en pierre et aile enduite, ainsi que plusieurs escaliers. Du matériel d'entretien ponctuel est visible, mais ne suffit pas à établir une phase de chantier différente. Aucun plan de projet paysager final ni chronologie explicitement annotée n'a été trouvé dans les 19 fichiers de ce projet.

**Cible provisoire : l'état photographié aménagé.** Il n'est pas établi que tout ce qui est photographié relève de la conception de Jonathan. Ne pas confondre cette cible avec une nouvelle proposition paysagère. Aucune projection à maturité végétale n'a été produite.

## Repères conservés

Chaque PDF fournit un départ graphique P00, un axe X sur le premier côté, un axe Y et un zéro Z local. Leur position physique sur le site n'est pas annotée de manière univoque.

| Relevé | Translation d'exposition, m | Rotation d'exposition | Décalage Z d'exposition | Transformation physique |
|---|---|---|---|---|
| Bordure maison | (0, 0, 0) | 0° | 0 m | Inconnue |
| Terrasse de droite | (25, 0, 0) | 0° | 0 m | Inconnue |
| Terrasse de gauche | (0, 20, 0) | 0° | 0 m | Inconnue |
| Zone escalier | (25, 20, 0) | 0° | 0 m | Inconnue |

Ces translations servent uniquement à une présentation éclatée. Elles sont identiques dans les exports 2D et 3D, consignées dans `releves.json` et facilement réversibles. Le repère commun PHYSIQUE demandé contractuellement n'est pas établi. Aucun nord ni altitude géographique n'est attribué. Le fichier 2D a Z = 0 ; les niveaux réels disponibles sont transcrits comme Z locaux en annotation.

## Raccordements étudiés, non retenus

| Rapprochement | Indice | Pourquoi il ne suffit pas |
|---|---|---|
| Bordure / terrasse gauche | Un côté de 3,91 m apparaît dans les deux relevés | Pas de deux points physiques identifiés ; la longueur seule ne démontre ni l'identité, ni le sens, ni le rattachement Z |
| Terrasses / façades | Décrochements visibles dans les contours et les photos | Les photos ne portent pas les numéros des sommets ; plusieurs décrochements et revêtements peuvent correspondre |
| Zone escalier / photos 9311–9313 | Escaliers en pierre et ruptures de niveau visibles | Plusieurs escaliers distincts ; aucun lien point par point établi |
| Relevés / aérienne | Bâti en plusieurs volumes et piscine reconnaissables | Pas de points de contrôle cotés ; surimpression cadastrale non utilisable comme preuve de limite juridique |

Aucun redimensionnement destiné à faire coïncider les relevés n'a été appliqué. Aucune rotation ou translation physique inventée n'est dissimulée derrière la disposition des groupes.

## Lecture et calibration des PDF

Les quatre documents sont vectoriels et comportent chacun six pages : plan, tableau des côtés en plan, vue 3D, tableau des côtés 3D, contours altimétriques, surface interpolée. Les quatre JPG associés correspondent visuellement à la page 1 seulement. Les autres pages apportent des données absentes des JPG.

L'extraction lit les vertices du tracé vectoriel ; elle n'effectue ni OCR ni tracé à main levée. Les XY sont des **coordonnées reconstruites**, pas des données brutes de mesure. Le Z provient des valeurs textuelles de la page 2, publiées au centimètre. Les distances de la page 2 sont horizontales ; celles de la page 4 intègrent le dénivelé, ce que les différences observées permettent de contrôler.

Un premier calibrage utilise la barre graphique du PDF. Pour la terrasse droite et l'escalier, il produit un décalage systématique dépassant les seuls arrondis des cotes. Le calibrage final est l'intersection des échelles compatibles avec tous les côtés arrondis à 0,01 m, le parcours total arrondi et, lorsqu'elle est publiée, la surface projetée arrondie à 0,01 m². L'échelle de la barre est conservée si elle appartient à l'intervalle ; sinon le milieu de l'intersection est utilisé. Les angles et proportions internes du tracé restent inchangés.

Cela représente environ +0,191 % en longueur pour la terrasse droite et +0,464 % pour l'escalier par rapport à la lecture initiale de leur barre graphique. Ce n'est pas une correction arbitraire du relevé : c'est un calibrage de la représentation PDF, explicite et reproductible. Les facteurs, l'intervalle admissible et le facteur initial sont enregistrés dans le JSON.

**Les cotes et surfaces utilisées pour calibrer ne constituent pas une validation indépendante de l'exactitude du site.** L'intervalle de ±0,005 m utilisé est l'intervalle mathématique d'arrondi au centimètre, pas une tolérance de chantier ni une précision annoncée du MOASURE.

## Tableau des hypothèses et décisions

| ID | Objet | Classe | Décision réversible / limite |
|---|---|---|---|
| H01 | État cible | Déduit visuellement | État photographié aménagé ; antériorité des relevés par rapport aux travaux non établie |
| H02 | Coordonnées XY | Déduites du PDF | Tracé vectoriel calibré, paramètres conservés |
| H03 | Niveaux Z | Explicitement cotés, locaux | Z de page 2, indépendants pour chaque relevé |
| H04 | Disposition des groupes | Convention de présentation | Quatre positions d'exposition, aucun sens topographique |
| H05 | Terrain intérieur aux contours | Inconnu | Interpolation Blender masquée et nommée NON LEVÉE ; pas de terrain continu livré |
| H06 | Bâti et ouvertures | Présence observée, dimensions incomplètes | Aucun volume arbitraire produit |
| H07 | Marches | Observées, géométrie incomplète | Aucun nombre de marches, giron ou contremarche inventé dans la base |
| H08 | Matériaux | Observés en photo, limites métriques non localisées | Pas d'affectation paysagère spéculative aux polygones |
| H09 | Piscine | Existante, confirmée en photos et aérienne | Ne serait pas un ajout de conception ; géométrie exacte non disponible |
| H10 | Limites et nord | Non certifiés | Pas de limite juridique ni d'orientation nord attribuée |
| H11 | Surface de bordure | Tracé ouvert | Les 50,17 m² de p.5 résultent d'une surface interpolée du logiciel ; aucune surface de bâtiment déduite de cette valeur |
| H12 | Surfaces 3D des autres relevés | Valeurs affichées p.5–6 | Ne pas les confondre avec les surfaces projetées de p.1 ni avec des métrés de revêtements établis |

Le volume affiché par MOASURE en pages 5–6 n'est pas utilisé comme cubature de terrassement : son plan de référence et son interprétation opérationnelle ne sont pas suffisamment documentés.

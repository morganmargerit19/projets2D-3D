# Bilan des contrôles — remise partielle

## Conservation et inspection

- Branche de départ : `main`, commit `0144802a4c3423310ed457b8e053e17aa3202567` ; copie de travail initialement propre. Aucun `AGENTS.md` dans l'arborescence versionnée inspectée.
- Branche de travail : `nokod/projet-2-reconstruction`. Aucune fusion demandée ni réalisée.
- 19 sources déplacées, sans renommer leur fichier : quatre PDF, quatre JPG associés, dix HEIC, une aérienne.
- Les 19 contenus ont été comparés octet par octet aux blobs du commit de départ, et par SHA-256 avant/après déplacement. Résultats dans `verification-locale.json`, empreintes dans `05-sources-de-production/manifest-original.json`.
- Les 24 pages PDF ont été rendues et inspectées ; les textes et tableaux ont été extraits. Les quatre JPG ne montrent que les pages 1, avec des contenus visuellement concordants. Les dix photos ont été converties et inspectées avec leur orientation ; l'aérienne a été inspectée séparément.

## Dimensions principales

| Relevé | Parcours XY publié / reconstruit, m | Parcours 3D publié / reconstruit, m | Aire projetée publiée / reconstruite, m² | Z local min / max, m |
|---|---|---|---|---|
| Bordure maison | 20,78 / 20,7835 | 20,84 / 20,8384 | Non applicable : ouvert | -0,59 / 0,00 |
| Terrasse de droite | 34,49 / 34,4931 | 34,53 / 34,5308 | 37,89 / 37,8891 | -0,14 / +0,17 |
| Terrasse de gauche | 47,54 / 47,5428 | 47,64 / 47,6411 | 46,18 / 46,1755 | -0,68 / +0,04 |
| Zone escalier | 15,68 / 15,6822 | 17,14 / 17,1483 | 8,59 / 8,5880 | -0,62 / +0,92 |

Les décimales supplémentaires ne sont affichées ici que pour rendre les écarts de calcul auditables. Elles ne sont pas la précision réelle du relevé. Le plan de consultation affiche des valeurs au centimètre.

Le tableau exhaustif `controles-dimensionnels.csv` couvre les 81 côtés dans les deux modes, avec référence, reconstruction, écart et limite de la source. Les cotes XY reconstruites sont compatibles avec leur arrondi au centimètre après calibration du PDF. **Ce résultat vérifie la reproduction du document, pas l'exactitude du terrain.**

Les écarts 3D proviennent aussi des Z publiés arrondis. Le côté le plus défavorable de la terrasse droite présente un écart d'environ 5,1 mm ; le parcours total 3D de l'escalier s'écarte d'environ 8,3 mm de la valeur publiée. Ils sont consignés sans retoucher arbitrairement les niveaux. Les données brutes permettraient de distinguer l'effet des arrondis d'autres effets.

Les surfaces de 37,96, 46,45 et 10,85 m² affichées en pages 5–6 sont distinctes des surfaces projetées de la page 1. Les 50,17 m² de la bordure ouverte ne sont pas assimilés à une emprise bâtie. Les volumes affichés ne sont pas transformés en cubatures opérationnelles.

## Contrôles des fichiers produits

| Contrôle | Résultat | Portée |
|---|---|---|
| DXF 2D et 3D rouverts | Réussi, audit ezdxf sans erreur | Structure DXF, pas import SketchUp |
| Unités DXF | Mètres, INSUNITS = 6 | Exports 1:1 |
| Correspondance des sommets | Identique au JSON commun à la précision numérique de sérialisation | Chaque relevé, hors raccordement physique |
| Plan XY | Z = 0 | Niveaux locaux dans les annotations/tableaux |
| Emprises 2D / 3D | Mêmes XY et mêmes translations d'exposition | Les quatre groupes ne constituent pas un plan assemblé |
| Fichier Blender rouvert | Réussi | Quatre objets de référence et cinq caméras vérifiés |
| Sommets Blender | Écarts de sérialisation inférieurs à 0,00001 m | Simple effet float32, pas précision topographique |
| Surfaces interpolées | Masquées et normales vers +Z | Interpolation facultative non validée comme terrain |
| PDF | Quatre pages A3 paysage 420 × 297 mm | 1:75 pour les trois premiers relevés, 1:30 pour l'escalier, impression à 100 % |
| Mise en page PDF | Pages rendues et inspectées | Tracés, cotes, tableaux et avertissements lisibles |
| Vues techniques | Cinq PNG de 1600 × 1200, inspectés | Issus de la même scène ; aucun agrandissement |
| Fichiers SKP | Non produits ici | Ruby préparé mais non exécuté, ouverture native non vérifiée |
| Rendus photoréalistes | 0 sur 5 | Non produits faute de maquette du site validée |

Le PDF est dessiné directement avec la conversion mètre → millimètre papier correspondant à l'échelle annoncée ; la barre de 1 m utilise exactement la même conversion. Toute option d'impression « adapter à la page » annule cette échelle.

Les images techniques montrent volontairement les lignes de relevé au-dessus d'un fond de studio. Ce fond n'est pas le terrain ; les lignes et marqueurs ne sont pas des ouvrages flottants. Le contrôle d'intersections de volumes bâtis, des seuils, des marches et des interfaces entre terrasses reste **non réalisé**, car ces volumes n'ont pas été inventés.

## Limites de conformité restantes

Le rattachement physique des relevés, le repère unique du site, le bâti, les ouvertures, les niveaux communs, les marches détaillées, les interfaces et l'affectation précise des matériaux restent à établir. Le plan de site 2D, la maquette paysagère 3D, les deux SKP contrôlés et les cinq rendus finaux demandés ne sont donc pas livrés comme conformes.

La notice fournit une procédure de génération de **bases** SKP dans SketchUp Desktop. L'exécution de cette procédure seule ne termine pas les tâches de reconstruction encore manquantes.

## Mise à jour DAE et images

Deux COLLADA 1.4.1 exportés puis réimportés dans Blender 4.5.3. Voir `verification-collada.json` pour les coordonnées et surfaces après transfert et `controle-geometrie/COLLADA_*_reimporte.png` pour les vues inspectées. Géométrie 2D entièrement à Z=0, Z locaux conservés en 3D, trois surfaces éditables dans chaque fichier. Les surfaces interpolées ne constituent pas une restitution du terrain ou des marches. Les groupes restent séparés.

Cinq visualisations générées depuis les photos et inspectées, voir `CONTROLE_VISUALISATIONS.md`. Les mentions antérieures « aucun rendu livré » décrivent l'état avant cette mise à jour. La vérification entre images et géométrie 3D demeure impossible : les images ne sont pas issues du modèle.

# NOKOD GARDENS — Projet 2 — Remise DAE et visualisations

Mise à jour du 17 septembre 2026. Deux fichiers COLLADA réellement produits et réimportés dans Blender, et cinq visualisations photographiques produites. **La reconstruction complète du site n'est pas achevée.** Les DAE contiennent les quatre relevés indépendants, pas les bâtiments et aménagements assemblés. Les cinq images sont des interprétations des photographies, pas des rendus issus de ces DAE.

## Fichiers à utiliser

- `01-plan-2d/NOKOD_Projet_2_Plan_2D.dae` : contours et trois surfaces projetées éditables à Z = 0, groupes par relevé, cotes et annotations en géométrie vectorielle. Les cotes ne sont pas des objets de cotation SketchUp associatifs.
- `02-modele-3d/NOKOD_Projet_2_Modele_3D.dae` : contours conservant les niveaux locaux, trois surfaces triangulées éditables. Ces surfaces interpolent les points de bord : elles ne constituent ni un terrain mesuré à l'intérieur, ni les marches reconstruites.
- `01-plan-2d/NOKOD_Projet_2_Releves_2D_CONTROLE.pdf` : quatre feuilles de contrôle A3, avec cotes, niveaux locaux et surfaces. Ce PDF demeure la référence lisible pour toutes les valeurs.
- `03-rendus/01_...png` à `05_...png` : cinq visualisations photoréalistes interprétatives du site photographié, sans conception nouvelle. Leurs cadrages suivent les photos sources.

La bordure de maison est un relevé ouvert : aucune face de bâtiment n'a été inventée pour le fermer.

## Importer dans SketchUp Desktop

1. Créer un modèle vide. Choisir **Fichier > Importer**, type **COLLADA (*.dae)**, puis le fichier 2D ou 3D.
2. Dans les options, conserver **Valider le fichier COLLADA**. La fusion des faces coplanaires peut simplifier le plan ; la désactiver pour conserver toute la triangulation de travail.
3. Faire **Zoom étendu**. Le modèle contient quatre ensembles séparés volontairement : ce n'est pas l'implantation du site. Les unités du DAE sont les mètres, à l'échelle réelle 1:1, axe vertical Z.
4. En 2D, choisir **Caméra > Projection parallèle**, puis la vue standard **Dessus**. En 3D, utiliser Orbite.
5. Contrôler le premier segment de la bordure, environ **2,86 m**. Ne pas redimensionner chaque relevé pour l'aligner aux autres.
6. Enregistrer sous `NOKOD_Projet_2_Plan_2D.skp` ou `NOKOD_Projet_2_Modele_3D.skp`, puis fermer et rouvrir le fichier.

Cette procédure suit l'[aide officielle SketchUp sur COLLADA](https://help.sketchup.com/en/sketchup/importing-and-exporting-collada-files). L'importation réelle dans SketchUp reste non testée ici ; la réimportation COLLADA a été exécutée dans Blender 4.5.3. Aucun SKP natif n'est livré.

## Modifier et organiser

Les nœuds de premier niveau portent les noms des quatre zones et la mention `REPERE_LOCAL_NON_RACCORDE`. Développer leur hiérarchie dans Structure, entrer dans le groupe/composant à modifier et utiliser les outils de faces et d'arêtes habituels. Les surfaces portent `SURFACE_PROJETEE` en 2D ou `SURFACE_INTERPOLEE_NON_TERRAIN` en 3D. Les objets `CONTOUR_SOURCE` conservent les sommets de référence. En 3D, les rubans de 5 mm sont seulement des aides d'affichage, pas des bordures construites.

Après import, créer les balises Bordure, Terrasse droite, Terrasse gauche, Escalier et Annotations ; les affecter aux groupes, laisser la géométrie brute sur Untagged. Les balises et scènes SketchUp ne sont pas garanties par COLLADA. Masquer les annotations pour travailler sur les contours. Ne pas éclater tous les groupes ensemble.

Les translations de présentation sont Bordure (0,0,0), Droite (25,0,0), Gauche (0,20,0), Escalier (25,20,0), en mètres. Les quatre origines et zéros altimétriques restent locaux. Aucun nord n'est affirmé.

## Cinq images et portée réelle

| Image | Source | Résolution réelle |
|---|---|---|
| 01 Vue ensemble jardin | IMG_9308.HEIC | 1448 × 1086 |
| 02 Terrasse repas | IMG_9298.HEIC | 1086 × 1449 |
| 03 Terrasse côté véranda | IMG_9305.HEIC | 1448 × 1086 |
| 04 Escalier seuil maison | IMG_9312.HEIC | 1086 × 1449 |
| 05 Escalier véranda vers bassin | IMG_9313.HEIC | 1448 × 1086 |

Génération intégrée ImageGen guidée par les photographies de consultation, harmonisation de lumière et retrait de quelques objets provisoires (sacs, seau, tuyaux, doigt du photographe). Aucun agrandissement n'a été appliqué. Le grand côté demandé de 3840 pixels n'a pas été obtenu. Les modèles génératifs modifient des détails de texture, de joints, de feuillage et parfois de perspective : ces images ne prouvent pas une fidélité dimensionnelle. Elles ne sont pas associées à des caméras calibrées du modèle et ne satisfont donc pas l'exigence initiale de cinq rendus de la même maquette.

Les prompts exacts et les références sont dans `05-sources-de-production/prompts-visualisations.json`. Le contrôle visuel détaillé est dans `CONTROLE_VISUALISATIONS.md`.

## Contrôles et limites

Les deux DAE ont été réimportés : unités, Z, sommets et surfaces contrôlés ; rapport `verification-collada.json`. L'écart numérique maximal des sommets après transfert est inférieur à 0,01 mm ; il mesure uniquement la conversion informatique, **pas la précision du relevé réel**. Les valeurs documentaires sont arrondies au centimètre. Les surfaces projetées 2D et 3D coïncident après transfert.

L'absence de repérage commun a été confirmée par l'utilisateur. Le bâti, les seuils communs, l'assemblage des quatre zones et les marches ne sont pas reconstruits de manière validée. Les photos et la vue aérienne donnent des relations visuelles, pas les coordonnées nécessaires à leur certification. Les noms des fichiers ne signifient pas que ces limites sont résolues.

Pour reproduire les DAE : exécuter `exporter_collada.py` avec Blender 4.5.3, puis `verifier_collada.py`. Les scripts et données sont conservés dans `05-sources-de-production`. Le script Ruby antérieur reste une option pour créer des cotations natives ; son exécution dans SketchUp n'a pas été vérifiée.

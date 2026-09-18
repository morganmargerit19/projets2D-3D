# Reproduire la base de production

Les fichiers originaux restent dans `projet 2/`. Toutes les productions sont sous `livrables/`.

## Dépendances

Python 3.12 avec PyMuPDF (`fitz`), NumPy, ezdxf, ReportLab, Pillow ; `heif-convert` pour les HEIC. Blender 4.5.3 LTS pour la scène et ses vues techniques. SketchUp Desktop pour exécuter le Ruby et sauvegarder réellement des SKP.

## Commandes

Depuis ce dossier :

```bash
python consulter_sources.py
python extraire_releves.py
python produire_base.py
blender -b -t 4 --python construire_blender.py
python verifier_livraison.py
```

`consulter_sources.py` convertit les photos sans modifier les HEIC, rend les 24 pages PDF et extrait leurs textes. Les copies JPEG de consultation sont limitées à 3000 pixels sur le grand côté, qualité 88, orientation appliquée ; les originaux gardent leur résolution. Ces copies servent à l'audit, pas à texturer une maquette.

`extraire_releves.py` régénère `releves.json`, le CSV des points et les contrôles dimensionnels. **Ne pas modifier manuellement ces sorties sans reporter les changements dans la chaîne de production.** Les coordonnées en décimales détaillées facilitent la reproduction informatique, sans revendiquer cette précision sur le terrain.

`produire_base.py` crée les deux DXF et le PDF A3. Les DXF sont rouverts et audités immédiatement. Les pages PDF doivent ensuite être rendues et inspectées à nouveau si la mise en page change.

`construire_blender.py` crée une scène avec les relevés et cinq caméras techniques. La géométrie de référence est conservée dans les objets `RELEVE_EXACT_...`. Les tubes, sphères et fond de studio sont des symboles de contrôle. Les surfaces d'interpolation sont masquées et ne sont pas des levés du terrain.

Le fichier `cameras-controle.json` indique les positions, orientations, cadrages orthographiques et résolutions réellement utilisés. Aucun jeu de textures paysagères ni de matériaux finaux n'est livré, puisque la maquette de site n'est pas achevée.

Pour SketchUp, suivre `04-controles-et-notice/NOTICE_JONATHAN.md`. Le générateur Ruby n'a pas été exécuté dans un moteur SketchUp pendant la production. Sa validation sur la version de Jonathan reste nécessaire.

## DAE et visualisations — mise à jour

Exécuter `blender -b --python exporter_collada.py`, puis `blender -b --python verifier_collada.py` avec Blender 4.5.3. Les deux exports COLLADA sont exécutés, contrairement au script Ruby non exécuté dans SketchUp. Les contours et les surfaces réimportées sont contrôlés dans `verification-collada.json`.

Les cinq images sont issues de l'outil intégré ImageGen, une référence photographique par image. Les prompts exacts sont dans `prompts-visualisations.json`. La reproduction n'est pas déterministe ; aucun seed ni modèle/version interne n'est exposé. Pas de caméra 3D correspondante, pas d'agrandissement appliqué. Aucun fichier de texture supplémentaire n'est requis pour les DAE (matériaux unis de contrôle).

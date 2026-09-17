# NOKOD GARDENS · MARZET · Projet 2

**Remise partielle de production — 17 septembre 2026. Mission contractuelle non terminée.**

Cette remise contient les quatre relevés reconstruits, leur plan de contrôle et leur représentation 3D dans des repères locaux indépendants. Elle ne contient pas encore une maquette du site assemblée, deux fichiers SKP validés ou cinq images photoréalistes finales.

## Ce qui est disponible

| Fichier | Usage | Statut |
|---|---|---|
| `01-plan-2d/NOKOD_Projet_2_Releves_2D_CONTROLE.pdf` | Quatre feuilles A3, contours, cotes, niveaux locaux et surfaces projetées | Produit et inspecté |
| `01-plan-2d/Releves_2D_non_raccordes.dxf` | Géométrie 2D éditable, mètres, Z = 0, disposition éclatée | Produit, rouvert et audité avec ezdxf ; import SketchUp non testé |
| `02-modele-3d/Releves_3D_non_raccordes.dxf` | Polylignes 3D conservant les Z locaux | Produit, rouvert et audité avec ezdxf ; import SketchUp non testé |
| `02-modele-3d/NOKOD_Projet_2_Releves_NON_RACCORDES.blend` | Relevés 3D, collections séparées et cinq caméras de contrôle | Produit ; représentation technique, pas maquette paysagère achevée |
| `05-sources-de-production/generer_sketchup.rb` + `releves.json` | Génération native dans SketchUp Desktop | Script préparé, **non exécuté dans SketchUp**, non certifié compatible avec la version exacte de Jonathan |
| `04-controles-et-notice/controle-geometrie/` | Cinq vues techniques à 1600 × 1200 pixels | Contrôles géométriques, **pas les cinq rendus finaux** |
| `03-rendus/STATUT.md` | État de la livraison des images finales | Aucun rendu final livré |

## Obtenir les deux bases SKP dans SketchUp Desktop

Le script construit de vraies arêtes, des faces 2D, des groupes, des balises, des cotes et des scènes, puis appelle la sauvegarde native de SketchUp. Il ne renomme pas un format intermédiaire. Il ne résout pas le raccordement des relevés.

1. Télécharger la branche complète et décompresser le ZIP. Conserver l'organisation des dossiers : le script lit `releves.json` à côté de lui.
2. Ouvrir **un nouveau modèle vide** dans SketchUp Desktop. Supprimer le personnage du modèle de départ. Le script refuse d'intervenir si le modèle contient déjà des objets.
3. Ouvrir la **console Ruby**, puis coller :

```ruby
f = UI.openpanel('Choisir generer_sketchup.rb', '', '*.rb'); load f if f
```

4. Choisir `05-sources-de-production/generer_sketchup.rb`, puis **2D** dans la boîte de dialogue. Si la génération réussit, le fichier `01-plan-2d/NOKOD_Projet_2_Plan_2D.skp` est enregistré.
5. Ouvrir **un autre modèle vide**, relancer la même commande et choisir **3D**. Le fichier `02-modele-3d/NOKOD_Projet_2_Modele_3D.skp` est enregistré si la génération réussit.
6. Fermer et **rouvrir chacun des deux SKP**. Contrôler les unités, les quatre groupes, les scènes et les points ci-dessous. Les noms des fichiers ne signifient pas que la mission finale est terminée : les modèles restent des bases NON RACCORDÉES.

Aucun fichier existant n'est écrasé par le script. En cas d'erreur, conserver le message de la console avec la version et le système d'exploitation. Aucun succès dans SketchUp n'a été vérifié à distance dans cette remise.

Alternative : importer le DXF correspondant, avec l'unité **mètre**, si l'édition installée le permet ; contrôler les dimensions puis enregistrer sous SKP. Cette méthode peut perdre certaines annotations ou propriétés selon l'importeur et n'a pas été testée ici.

## Naviguer et modifier

- Les scènes donnent une vue de dessus en projection parallèle, une axonométrie pour la base 3D et une vue de chaque relevé.
- Dans **Structure**, choisir un groupe nommé `Bordure maison`, `Terrasse de droite`, `Terrasse de gauche` ou `Zone escalier`. Double-cliquer pour modifier sa géométrie.
- Dans **Balises**, afficher ou masquer les catégories 01 à 04, `90_Annotations` et `91_Cotes`. Les arêtes et faces brutes restent sur Untagged.
- Les contours sont disposés à distance les uns des autres pour être lisibles. **Ne pas lire les distances entre groupes comme des distances sur le terrain.**
- Les Z des points sont relatifs à P00 de leur propre relevé. Ne pas aligner les quatre zéros sans rattachement à un même point physique.
- Modifier les données de référence dans `releves.json`, puis régénérer les exports pour conserver la cohérence 2D/3D. Les valeurs XY sont déduites des PDF, pas des coordonnées brutes MOASURE.
- Le fichier Blender contient une surface triangulée facultative masquée pour les trois contours fermés. Elle est une interpolation des points de bord, **pas un terrain levé ni une restitution des marches**. Les épaisseurs des tubes et les sphères de contrôle sont des symboles de présentation.

## Contrôles à faire après génération native

1. En 2D, vérifier que les sommets de contour sont tous à Z = 0 ; en 3D, vérifier les Z locaux.
2. Vérifier, avec le mètre SketchUp, le premier segment de la bordure : environ 2,86 m ; la terrasse gauche doit présenter environ 46,18 m² projetés.
3. Vérifier les quatre groupes et l'absence de géométrie brute affectée aux balises métier.
4. Pour l'escalier, retrouver la plage locale de -0,62 à +0,92 m. Elle ne constitue pas un dénivelé connu entre les terrasses.
5. Vérifier qu'aucune fermeture n'a été inventée pour le relevé ouvert `Bordure maison`.
6. Contrôler visuellement les annotations dans SketchUp. Leur mise en page ne peut pas être certifiée par le seul examen du script.

Les segments inférieurs à 1 mm peuvent être omis comme arêtes lors de la génération native afin d'éviter les micro-arêtes ; leur présence et leurs valeurs sont conservées dans le JSON, les CSV et les attributs de groupe. Cela concerne des côtés publiés à 0,00 m, pas des détails architecturaux à supprimer arbitrairement.

## Ce qui empêche la remise finale

- Aucun repérage physique des départs de relevés et des points communs n'est disponible. L'utilisateur l'a confirmé pendant la production. Les rotations, translations et décalages Z physiques ne sont donc pas validés.
- Les longueurs similaires, notamment 3,91 m, ne prouvent pas à elles seules que deux côtés décrivent la même arête.
- Les contours n'identifient pas toutes les limites entre gravier, dallage, façade et bordure. Les affecter automatiquement à un matériau ou à un mur serait une hypothèse structurante non contrôlée.
- La vue aérienne ne constitue pas une orthophotographie métrique attestée. Les hauteurs de bâti, dimensions des ouvertures, emprises détaillées du bassin et girons/contremarches ne sont pas cotés dans les sources.
- Le relevé « Zone escalier » ne décrit pas chaque marche. Il ne faut pas transformer la surface interpolée en escalier final.
- SketchUp natif n'est pas disponible dans l'environnement de production. Les deux SKP n'y ont été ni créés ni rouverts.

Pour terminer fidèlement : repérer sur une même vue les départs et au moins deux points communs par raccordement, avec un point de niveau commun ; identifier les contours correspondant aux façades et revêtements ; compléter les détails architecturaux et marches qui restent indéterminés. Des exports MOASURE numériques peuvent améliorer les coordonnées, mais ne garantissent pas à eux seuls un repère commun.

## Références techniques du transfert

Le script emploie l'[API native des modèles SketchUp](https://ruby.sketchup.com/Sketchup/Model.html), l'[API de création des entités](https://ruby.sketchup.com/Sketchup/Entities.html) et les [caméras SketchUp](https://ruby.sketchup.com/Sketchup/Camera.html). La présence de ces appels ne remplace pas leur exécution et le contrôle des fichiers dans SketchUp.

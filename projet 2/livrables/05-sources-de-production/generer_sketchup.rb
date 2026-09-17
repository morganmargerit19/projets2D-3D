# encoding: UTF-8
# A EXECUTER DANS SKETCHUP DESKTOP. Non execute ni valide dans l'environnement de production.
# Produit une BASE PARTIELLE de releves independants, pas la maquette finale du site.
# Documentation API: https://ruby.sketchup.com/Sketchup/Model.html
require 'sketchup.rb'
require 'json'

module NokodProjet2
  extend self
  ROOT = File.expand_path('..', File.dirname(__FILE__)) unless const_defined?(:ROOT)
  def point(v)
    Geom::Point3d.new(v.map { |x| x.to_f.m })
  end

  def generate
    model = Sketchup.active_model
    unless model.entities.length == 0 && model.active_path.nil?
      UI.messagebox('Ouvrez un NOUVEAU modele vide et supprimez le personnage par defaut. Aucun objet existant ne sera efface par ce script.')
      return
    end
    answer = UI.inputbox(['Type de base a generer :'], ['2D'], ['2D|3D'], 'NOKOD - Releves NON RACCORDES')
    return unless answer
    mode = answer[0]
    path = File.join(ROOT, mode == '2D' ? '01-plan-2d' : '02-modele-3d', mode == '2D' ? 'NOKOD_Projet_2_Plan_2D.skp' : 'NOKOD_Projet_2_Modele_3D.skp')
    if File.exist?(path)
      UI.messagebox('Le fichier existe deja. Deplacez-le ou renommez-le avant de relancer. Aucun ecrasement effectue.')
      return
    end
    data = JSON.parse(File.read(File.join(File.dirname(__FILE__), 'releves.json'), encoding: 'UTF-8'))
    model.start_operation('NOKOD - base de releves', true)
    begin
      model.active_layer = model.layers[0]
      model.options['UnitsOptions']['LengthUnit'] = 4
      model.options['UnitsOptions']['LengthFormat'] = 0
      model.options['UnitsOptions']['LengthPrecision'] = 2
      model.options['UnitsOptions']['SuppressUnitsDisplay'] = false
      model.description = 'BASE PARTIELLE NON RACCORDEE. XY deduits des PDF; Z locaux cotes. Les positions des groupes sont une disposition eclatee de consultation. Ni batiment restitue ni terrain continu. Aucun rendu final.'
      model.set_attribute('NOKOD', 'statut', data['status'])
      model.set_attribute('NOKOD', 'mode', mode)
      colors = [[84,109,113],[168,120,67],[76,120,101],[139,100,116]]
      groups = []
      data['datasets'].each_with_index do |d,j|
        g = model.entities.add_group
        g.name = d['name'] + ' - NON RACCORDE'
        g.layer = model.layers.add(format('%02d_%s', j+1, d['name']))
        g.set_attribute('NOKOD','source',d['source'])
        g.set_attribute('NOKOD','repere','Origine P00 locale du PDF; position physique inconnue')
        g.set_attribute('NOKOD','translation_exposition_metres',d['offset_display'])
        g.set_attribute('NOKOD','points_source_json',JSON.generate(d['points']))
        g.set_attribute('NOKOD','surface_projetee_m2',d['area_projected']) if d['area_projected']
        material = model.materials.add('NOKOD_'+j.to_s)
        material.color = Sketchup::Color.new(*colors[j]);material.alpha = 0.4
        coords = d['points'].map { |p| [p[0],p[1],mode == '2D' ? 0.0 : p[2]] }
        pts = coords.map { |p| point(p) }
        omitted = []
        pts.each_cons(2).with_index do |pair,i|
          if pair[0].distance(pair[1]) < 0.001.m
            omitted << i+1
          else
            edge = g.entities.add_line(pair[0],pair[1])
            edge.layer = model.layers[0] if edge
          end
        end
        g.set_attribute('NOKOD','micro_segments_sans_arete',omitted.join(','))
        if mode == '2D' && d['closed']
          clean = []
          pts[0...-1].each { |p| clean << p if clean.empty? || clean[-1].distance(p) >= 0.001.m }
          face = g.entities.add_face(clean)
          if face
            face.reverse! if face.normal.z < 0
            face.material = material;face.back_material = material
            face.layer = model.layers[0]
          end
        end
        # Annotations independantes, geometrie brute sur Untagged.
        note = g.entities.add_group;note.name = 'Annotations locales'
        note.layer = model.layers.add('90_Annotations')
        title = d['name'] + "\nNON RACCORDE - Z local"
        title += format("\nAire projetee %.2f m2",d['area_projected']) if d['area_projected']
        note.entities.add_text(title,point([coords.map{|p|p[0]}.min,coords.map{|p|p[1]}.max+0.8,0]))
        pts.each_with_index do |p,i|
          next if i > 0 && p.distance(pts[i-1]) < 0.12.m
          next if d['closed'] && i == pts.length-1
          note.entities.add_text(format('P%02d / Zlocal=%+.2fm',i,d['points'][i][2]),p,Geom::Vector3d.new(0.2.m,0.2.m,0))
        end
        if mode == '2D'
          dims = g.entities.add_group;dims.name = 'Cotes calculees depuis XY';dims.layer = model.layers.add('91_Cotes')
          pts.each_cons(2).with_index do |pair,i|
            next if d['sides_plan'][i]['length'] < 1
            v = pair[1]-pair[0];n = Geom::Vector3d.new(-v.y,v.x,0);n.length = 0.35.m
            dims.entities.add_dimension_linear(pair[0],pair[1],n)
          end
        end
        g.transformation = Geom::Transformation.translation(point(d['offset_display']).to_a)
        groups << g
      end
      model.entities.add_text('BASE PARTIELLE - DISPOSITION ECLATEE, PAS UNE IMPLANTATION',point([0,35,0]))
      view = model.active_view
      view.camera = Sketchup::Camera.new(point([15,10,70]),point([15,10,0]),[0,1,0],false)
      view.zoom_extents
      model.pages.add('01 Plan - disposition eclatee')
      if mode == '3D'
        view.camera = Sketchup::Camera.new(point([42,-35,36]),point([15,10,0]),[0,0,1],false)
        view.zoom_extents;model.pages.add('02 Axonometrie des releves')
      end
      groups.each_with_index do |g,i|
        t=g.bounds.center
        eye= mode == '2D' ? t+Geom::Vector3d.new(0,0,30.m) : t+Geom::Vector3d.new(12.m,-18.m,18.m)
        up=mode == '2D' ? [0,1,0] : [0,0,1]
        view.camera=Sketchup::Camera.new(eye,t,up,false);view.zoom(g)
        model.pages.add(format('%02d %s',i+3,data['datasets'][i]['name']))
      end
      model.pages.selected_page=model.pages[0]
      model.commit_operation
      raise 'Echec de sauvegarde native SketchUp' unless model.save(path)
      UI.messagebox("Base #{mode} enregistree :\n#{path}\n\nElle reste NON RACCORDEE. Rouvrez le SKP et appliquez les controles de la notice. Pour l autre fichier, ouvrez un nouveau modele vide et relancez.")
    rescue StandardError => e
      model.abort_operation
      UI.messagebox("Erreur : #{e.message}\nAucun succes de livraison ne doit etre presume.")
      raise
    end
  end
end
NokodProjet2.generate

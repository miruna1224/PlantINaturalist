import torch
import torchvision.transforms.functional as F
import torchvision.transforms as transforms
from torch.nn.functional import softmax


ALL_CLASSES = ['Acacia_pycnantha', 'Acanthocereus_tetragonus', 'Achillea_millefolium', 'Ageratum_houstonianum', 'Ajuga_reptans', 'Alcea_rosea', 'Ambrosia_trifida', 'Amelanchier_spicata', 'Anredera_cordifolia', 'Apocynum_cannabinum', 'Aralia_californica', 'Aralia_spinosa', 'Arbutus_menziesii', 'Artemisia_tridentata', 'Aruncus_dioicus', 'Asclepias_humistrata', 'Asparagus_aethiopicus', 'Asparagus_scandens', 'Asplenium_viride', 'Astelia_hastata', 'Aster_alpinus', 'Atropa_belladonna', 'Betula_pumila', 'Bidens_pilosa', 'Bidens_tripartita', 'Bignonia_capreolata', 'Borrichia_frutescens', 'Bouteloua_hirsuta', 'Brachyglottis_repanda', 'Brickellia_eupatorioides', 'Briza_minor', 'Bromelia_pinguin', 'Bromus_tectorum', 'Cakile_maritima', 'Calendula_officinalis', 'Callirhoe_involucrata', 'Calochortus_splendens', 'Calotropis_procera', 'Calyptridium_monandrum', 'Campanula_glomerata', 'Carex_vesicaria', 'Carex_viridula', 'Carpobrotus_chilensis', 'Catharanthus_roseus', 'Caulophyllum_giganteum', 'Ceanothus_fendleri', 'Ceanothus_perplexans', 'Cephalanthera_damasonium', 'Chamaebatiaria_millefolium', 'Cirsium_arizonicum', 'Clematis_vitalba', 'Convallaria_majalis', 'Coptis_trifolia', 'Cornus_amomum', 'Cornus_drummondii', 'Corydalis_aurea', 'Crepis_tectorum', 'Cunila_origanoides', 'Cystopteris_protrusa', 'Dasylirion_wheeleri', 'Dianella_nigra', 'Dieteria_canescens', 'Draba_cuneifolia', 'Drosera_spatulata', 'Dryopteris_cristata', 'Dryopteris_marginalis', 'Ehrendorferia_chrysantha', 'Erigeron_bonariensis', 'Erigeron_philadelphicus', 'Eriodictyon_crassifolium', 'Eriogonum_latifolium', 'Erodium_moschatum', 'Erysimum_cheiri', 'Erythronium_montanum', 'Erythronium_umbilicatum', 'Euphorbia_dentata', 'Euphorbia_lathyris', 'Euphorbia_misera', 'Euphorbia_serpens', 'Fallopia_scandens', 'Fuchsia_excorticata', 'Funastrum_heterophyllum', 'Galearis_spectabilis', 'Galeopsis_bifida', 'Garrya_lindheimeri', 'Gaultheria_depressa', 'Genista_tinctoria', 'Gleditsia_triacanthos', 'Gonolobus_suberosus', 'Gymnadenia_rhellicani', 'Gymnocladus_dioicus', 'Hackelia_virginiana', 'Helichrysum_arenarium', 'Heliconia_psittacorum', 'Heliopsis_helianthoides', 'Hellenia_speciosa', 'Hieracium_albiflorum', 'Hylotelephium_telephium', 'Hypericum_androsaemum', 'Hypericum_gentianoides', 'Ilex_cassine', 'Ilex_vomitoria', 'Ipomoea_cordatotriloba', 'Ipomoea_quamoclit', 'Jacaranda_mimosifolia', 'Juncus_effusus', 'Juniperus_communis', 'Koeberlinia_spinosa', 'Lathyrus_vestitus', 'Ligustrum_quihoui', 'Lilium_humboldtii', 'Lolium_pratense', 'Lonicera_ciliosa', 'Lonicera_hispidula', 'Lonicera_xylosteum', 'Lotus_pedunculatus', 'Lupinus_arboreus', 'Lupinus_lepidus', 'Lycopodium_volubile', 'Lycoris_radiata', 'Lygodesmia_texana', 'Macroptilium_atropurpureum', 'Marchantia_polymorpha', 'Matelea_reticulata', 'Medeola_virginiana', 'Melilotus_albus', 'Mentha_arvensis', 'Metrosideros_robusta', 'Mikania_micrantha', 'Moehringia_lateriflora', 'Monardella_villosa', 'Moneses_uniflora', 'Muscari_botryoides', 'Myriophyllum_aquaticum', 'Neckera_pennata', 'Neolloydia_conoidea', 'Neotinea_tridentata', 'Nonea_pulla', 'Nuphar_lutea', 'Oenothera_cespitosa', 'Oenothera_glazioviana', 'Oenothera_triloba', 'Opuntia_robusta', 'Origanum_vulgare', 'Orontium_aquaticum', 'Oxalis_corniculata', 'Oxalis_incarnata', 'Pachysandra_terminalis', 'Paliurus_spina-christi', 'Parkinsonia_florida', 'Parsonsia_heterophylla', 'Paspalum_dilatatum', 'Pedicularis_bracteosa', 'Pellaea_mucronata', 'Peltandra_virginica', 'Peniocereus_greggii', 'Penstemon_davidsonii', 'Penstemon_heterophyllus', 'Penthorum_sedoides', 'Petasites_albus', 'Phaenocoma_prolifera', 'Phlomoides_tuberosa', 'Plagiomnium_insigne', 'Plantago_patagonica', 'Plantago_rugelii', 'Platanus_occidentalis', 'Platanus_racemosa', 'Pleurocoronis_pluriseta', 'Polypodium_glycyrrhiza', 'Populus_balsamifera', 'Porophyllum_gracile', 'Potentilla_gracilis', 'Prenanthes_purpurea', 'Prosopis_velutina', 'Protea_caffra', 'Prunus_dulcis', 'Prunus_ilicifolia', 'Pyrola_asarifolia', 'Pyrus_calleryana', 'Quercus_michauxii', 'Quercus_nigra', 'Quercus_shumardii', 'Ranunculus_sceleratus', 'Rhododendron_lapponicum', 'Ribes_nevadense', 'Ribes_nigrum', 'Rivina_humilis', 'Rosa_carolina', 'Rosa_gymnocarpa', 'Rubus_bifrons', 'Rubus_cissoides', 'Salix_caprea', 'Saltera_sarcocolla', 'Salvia_azurea', 'Salvia_texana', 'Sanguinaria_canadensis', 'Sanicula_europaea', 'Sceptridium_dissectum', 'Schinus_terebinthifolia', 'Schoenoplectus_californicus', 'Scolymus_hispanicus', 'Scutellaria_drummondii', 'Setaria_parviflora', 'Sida_ciliaris', 'Silene_coronaria', 'Silene_latifolia', 'Simmondsia_chinensis', 'Sisymbrium_officinale', 'Smilax_herbacea', 'Smyrnium_olusatrum', 'Solanum_elaeagnifolium', 'Solanum_mauritianum', 'Solanum_pseudocapsicum', 'Solidago_hispida', 'Solidago_speciosa', 'Sonchus_oleraceus', 'Sorbaria_sorbifolia', 'Sorbus_aucuparia', 'Sorghastrum_nutans', 'Sparaxis_tricolor', 'Spinifex_sericeus', 'Sporobolus_michauxianus', 'Stenocereus_thurberi', 'Sticherus_cunninghamii', 'Stratiotes_aloides', 'Symphyotrichum_lateriflorum', 'Tamarindus_indica', 'Tillandsia_usneoides', 'Triantha_glutinosa', 'Trifolium_subterraneum', 'Trillium_cernuum', 'Tripsacum_dactyloides', 'Tylecodon_paniculatus', 'Typha_orientalis', 'Uvularia_perfoliata', 'Vaccinium_ovalifolium', 'Vaccinium_ovatum', 'Vaccinium_oxycoccos', 'Vachellia_farnesiana', 'Vachellia_karroo', 'Verbesina_encelioides', 'Veronica_persica', 'Viburnum_edule', 'Vicia_americana', 'Viola_mirabilis', 'Viola_sagittata', 'Washingtonia_filifera', 'Zamia_integrifolia', 'Zinnia_peruviana', 'Zizia_aurea']


class SquarePad:
    def __call__(self, image):
        max_wh = max(image.size)
        p_left, p_top = [(max_wh - s) // 2 for s in image.size]
        p_right, p_bottom = [max_wh - (s+pad) for s, pad in zip(image.size, [p_left, p_top])]
        padding = (p_left, p_top, p_right, p_bottom)
        return F.pad(image, padding, 0, 'constant')


transform = transforms.Compose([
    SquarePad(),
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def load_model(path_to_model):
    return torch.jit.load(path_to_model)


def top_3_predictions(model, image):
    image = transform(image)
    image = image.unsqueeze(0)
    predictions = softmax(model(image), 1)
    values, indices = torch.topk(predictions, 3)
    values = [x.item() for x in values.squeeze()]
    indices = [ALL_CLASSES[int(x.item())] for x in indices.squeeze()]
    return list(zip(indices,values))



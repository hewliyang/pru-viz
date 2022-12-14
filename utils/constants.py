"""
Party to ID & Color Mappings were extracted from the SPR Dashboard JS files with some slight modifications
"""

alias_to_id_color = {'OTHER': {'id': 0, 'color': '#f2ffff'},
 'BN': {'id': 1, 'color': '#031A93'},
 'PAS': {'id': 2, 'color': '#6CB332'},
 'DAP': {'id': 3, 'color': '#E30911'},
 'BERJASA': {'id': 4, 'color': '#005121'},
 'PBB': {'id': 5, 'color': 'ADADAD'},
 'KIMMA': {'id': 6, 'color': '#DE8801'},
 'PRM': {'id': 7, 'color': 'FE8591'},
 'PBS': {'id': 8, 'color': '#763B37'},
 'UPKO': {'id': 9, 'color': '#2A0E72'},
 'PPM': {'id': 10, 'color': 'CC9900'},
 'BEBAS': {'id': 20, 'color': '#993300'},
 'GERAKAN': {'id': 12, 'color': '#FE2514'},
 'LDP': {'id': 13, 'color': '#AB3D1A'},
 'PMS': {'id': 14, 'color': '#FBFD0B'},
 'AMIPF': {'id': 15, 'color': '#E30300'},
 'MAP': {'id': 16, 'color': '#F6EB19'},
 'UMNO': {'id': 17, 'color': '#A03232'},
 'MCA': {'id': 18, 'color': '#07257F'},
 'MIC': {'id': 19, 'color': '#00A55E'},
 'SUPP': {'id': 11, 'color': '#FFFF00'},
 'PBRS': {'id': 21, 'color': '#6666FF'},
 'PDP': {'id': 22, 'color': '#0000FD'},
 'PKR': {'id': 23, 'color': '#04A0D1'},
 'PRS': {'id': 24, 'color': '#186D43'},
 'PEJUANG': {'id': 25, 'color': '#09618A'},
 'PFP': {'id': 26, 'color': '#E45035'},
 'PN': {'id': 27, 'color': '#043253'},
 'GAGASAN': {'id': 28, 'color': '#e9d720'},
 'ASPIRASI': {'id': 29, 'color': '#BD354D'},
 'PBDS': {'id': 30, 'color': '#0B46C8'},
 'PH': {'id': 31, 'color': '#D7292F'},
 'GPS': {'id': 32, 'color': '#1F2C45'},
 'USNO': {'id': 33, 'color': '#1A740A'},
 'PUTRA': {'id': 34, 'color': '#FEFE00'},
 'PSB': {'id': 35, 'color': '#A13C33'},
 'MUDA': {'id': 36, 'color': '#000000'},
 'IMAN': {'id': 37, 'color': '#EC1F26'},
 'SEDAR': {'id': 38, 'color': '#C3B62B'},
 'M.M.S.P.': {'id': 39, 'color': '#EF8812'},
 'BERSAMA': {'id': 40, 'color': '#FF66FF'},
 'PCM': {'id': 41, 'color': '#F4E50E'},
 'PBM': {'id': 42, 'color': '#323467'},
 'PSM': {'id': 43, 'color': '#C0110D'},
 'MCC': {'id': 44, 'color': '#C92725'},
 'AMANAH': {'id': 45, 'color': '#F79220'},
 'PPRS': {'id': 46, 'color': '#0000FF'},
 'ANAKNEGERI': {'id': 47, 'color': '#F6E13A'},
 'PEACE': {'id': 48, 'color': '#FEF200'},
 'TERAS': {'id': 49, 'color': '#310051'},
 'PKS': {'id': 50, 'color': '#3567B2'},
 'SAPU': {'id': 51, 'color': '#FC771F'},
 'PAP': {'id': 52, 'color': '#08334C'},
 'PCS': {'id': 53, 'color': '#DE1E14'},
 'WARISAN': {'id': 54, 'color': '#5BC5F0'},
 'BERSATU': {'id': 55, 'color': '#E30007'},
 'STARSABAH': {'id': 56, 'color': '#0095DB'},
 'HR': {'id': 57, 'color': '#6F92BF'},
 'PBK': {'id': 58, 'color': '#672D34'},
 'IKATAN': {'id': 59, 'color': '#F6E816'},
 'MU': {'id': 60, 'color': '#ED1D24'},
 'PERPADUAN': {'id': 61, 'color': '#01AC5C'},
 'SPP': {'id': 62, 'color': '#c7e011'},
 'GRS': {'id': 63, 'color': '#6285a8'},
 'KDM': {'id': 64, 'color': '#EB7389'},
 'PUR': {'id': 65, 'color': '#ff030b'},
 'PRIM': {'id': 66, 'color': '#fff'}}

id_to_alias_color = {0: {'alias': 'OTHER', 'color': '#f2ffff'},
 1: {'alias': 'BN', 'color': '#031A93'},
 2: {'alias': 'PAS', 'color': '#6CB332'},
 3: {'alias': 'DAP', 'color': '#E30911'},
 4: {'alias': 'BERJASA', 'color': '#005121'},
 5: {'alias': 'PBB', 'color': 'ADADAD'},
 6: {'alias': 'KIMMA', 'color': '#DE8801'},
 7: {'alias': 'PRM', 'color': 'FE8591'},
 8: {'alias': 'PBS', 'color': '#763B37'},
 9: {'alias': 'UPKO', 'color': '#2A0E72'},
 10: {'alias': 'PPM', 'color': 'CC9900'},
 20: {'alias': 'BEBAS', 'color': '#993300'},
 12: {'alias': 'GERAKAN', 'color': '#FE2514'},
 13: {'alias': 'LDP', 'color': '#AB3D1A'},
 14: {'alias': 'PMS', 'color': '#FBFD0B'},
 15: {'alias': 'AMIPF', 'color': '#E30300'},
 16: {'alias': 'MAP', 'color': '#F6EB19'},
 17: {'alias': 'UMNO', 'color': '#A03232'},
 18: {'alias': 'MCA', 'color': '#07257F'},
 19: {'alias': 'MIC', 'color': '#00A55E'},
 11: {'alias': 'SUPP', 'color': '#FFFF00'},
 21: {'alias': 'PBRS', 'color': '#6666FF'},
 22: {'alias': 'PDP', 'color': '#0000FD'},
 23: {'alias': 'PKR', 'color': '#04A0D1'},
 24: {'alias': 'PRS', 'color': '#186D43'},
 25: {'alias': 'PEJUANG', 'color': '#09618A'},
 26: {'alias': 'PFP', 'color': '#E45035'},
 27: {'alias': 'PN', 'color': '#043253'},
 28: {'alias': 'GAGASAN', 'color': '#e9d720'},
 29: {'alias': 'ASPIRASI', 'color': '#BD354D'},
 30: {'alias': 'PBDS', 'color': '#0B46C8'},
 31: {'alias': 'PH', 'color': '#D7292F'},
 32: {'alias': 'GPS', 'color': '#1F2C45'},
 33: {'alias': 'USNO', 'color': '#1A740A'},
 34: {'alias': 'PUTRA', 'color': '#FEFE00'},
 35: {'alias': 'PSB', 'color': '#A13C33'},
 36: {'alias': 'MUDA', 'color': '#000000'},
 37: {'alias': 'IMAN', 'color': '#EC1F26'},
 38: {'alias': 'SEDAR', 'color': '#C3B62B'},
 39: {'alias': 'M.M.S.P.', 'color': '#EF8812'},
 40: {'alias': 'BERSAMA', 'color': '#FF66FF'},
 41: {'alias': 'PCM', 'color': '#F4E50E'},
 42: {'alias': 'PBM', 'color': '#323467'},
 43: {'alias': 'PSM', 'color': '#C0110D'},
 44: {'alias': 'MCC', 'color': '#C92725'},
 45: {'alias': 'AMANAH', 'color': '#F79220'},
 46: {'alias': 'PPRS', 'color': '#0000FF'},
 47: {'alias': 'ANAKNEGERI', 'color': '#F6E13A'},
 48: {'alias': 'PEACE', 'color': '#FEF200'},
 49: {'alias': 'TERAS', 'color': '#310051'},
 50: {'alias': 'PKS', 'color': '#3567B2'},
 51: {'alias': 'SAPU', 'color': '#FC771F'},
 52: {'alias': 'PAP', 'color': '#08334C'},
 53: {'alias': 'PCS', 'color': '#DE1E14'},
 54: {'alias': 'WARISAN', 'color': '#5BC5F0'},
 55: {'alias': 'BERSATU', 'color': '#E30007'},
 56: {'alias': 'STARSABAH', 'color': '#0095DB'},
 57: {'alias': 'HR', 'color': '#6F92BF'},
 58: {'alias': 'PBK', 'color': '#672D34'},
 59: {'alias': 'IKATAN', 'color': '#F6E816'},
 60: {'alias': 'MU', 'color': '#ED1D24'},
 61: {'alias': 'PERPADUAN', 'color': '#01AC5C'},
 62: {'alias': 'SPP', 'color': '#c7e011'},
 63: {'alias': 'GRS', 'color': '#6285a8'},
 64: {'alias': 'KDM', 'color': '#EB7389'},
 65: {'alias': 'PUR', 'color': '#ff030b'},
 66: {'alias': 'PRIM', 'color': '#fff'}}

# minified js code to format the legends/tooltips

vmap_jscode = 'function test(a){return({0:{alias:"OTHER",color:"#FFFFFF"},1:{alias:"BN",color:"#031A93"},2:{alias:"PAS",color:"#6CB332"},3:{alias:"DAP",color:"#E30911"},4:{alias:"BERJASA",color:"#005121"},5:{alias:"PBB",color:"ADADAD"},6:{alias:"KIMMA",color:"#DE8801"},7:{alias:"PRM",color:"FE8591"},8:{alias:"PBS",color:"#763B37"},9:{alias:"UPKO",color:"#2A0E72"},10:{alias:"PPM",color:"CC9900"},20:{alias:"BEBAS",color:"#993300"},12:{alias:"GERAKAN",color:"#FE2514"},13:{alias:"LDP",color:"#AB3D1A"},14:{alias:"PMS",color:"#FBFD0B"},15:{alias:"AMIPF",color:"#E30300"},16:{alias:"MAP",color:"#F6EB19"},17:{alias:"UMNO",color:"#A03232"},18:{alias:"MCA",color:"#07257F"},19:{alias:"MIC",color:"#00A55E"},11:{alias:"SUPP",color:"#FFFF00"},21:{alias:"PBRS",color:"#6666FF"},22:{alias:"PDP",color:"#0000FD"},23:{alias:"PKR",color:"#04A0D1"},24:{alias:"PRS",color:"#186D43"},25:{alias:"PEJUANG",color:"#09618A"},26:{alias:"PFP",color:"#E45035"},27:{alias:"PN",color:"#043253"},28:{alias:"GAGASAN",color:"#e9d720"},29:{alias:"ASPIRASI",color:"#BD354D"},30:{alias:"PBDS",color:"#0B46C8"},31:{alias:"PH",color:"#D7292F"},32:{alias:"GPS",color:"#1F2C45"},33:{alias:"USNO",color:"#1A740A"},34:{alias:"PUTRA",color:"#FEFE00"},35:{alias:"PSB",color:"#A13C33"},36:{alias:"MUDA",color:"#000000"},37:{alias:"IMAN",color:"#EC1F26"},38:{alias:"SEDAR",color:"#C3B62B"},39:{alias:"M.M.S.P.",color:"#EF8812"},40:{alias:"BERSAMA",color:"#FF66FF"},41:{alias:"PCM",color:"#F4E50E"},42:{alias:"PBM",color:"#323467"},43:{alias:"PSM",color:"#C0110D"},44:{alias:"MCC",color:"#C92725"},45:{alias:"AMANAH",color:"#F79220"},46:{alias:"PPRS",color:"#0000FF"},47:{alias:"ANAKNEGERI",color:"#F6E13A"},48:{alias:"PEACE",color:"#FEF200"},49:{alias:"TERAS",color:"#310051"},50:{alias:"PKS",color:"#3567B2"},51:{alias:"SAPU",color:"#FC771F"},52:{alias:"PAP",color:"#08334C"},53:{alias:"PCS",color:"#DE1E14"},54:{alias:"WARISAN",color:"#5BC5F0"},55:{alias:"BERSATU",color:"#E30007"},56:{alias:"STARSABAH",color:"#0095DB"},57:{alias:"HR",color:"#6F92BF"},58:{alias:"PBK",color:"#672D34"},59:{alias:"IKATAN",color:"#F6E816"},60:{alias:"MU",color:"#ED1D24"},61:{alias:"PERPADUAN",color:"#01AC5C"},62:{alias:"SPP",color:"#c7e011"},63:{alias:"GRS",color:"#6285a8"},64:{alias:"KDM",color:"#EB7389"},65:{alias:"PUR",color:"#ff030b"},66:{alias:"PRIM",color:"#fff"}})[a].alias}' 
tooltip_cont_jscode = 'function test(e){return e.seriesName+"<br/>"+e.name+": "+e.value.toFixed(2)+"%"}'
tooltip_discrete_jscode = 'function test(e){return e.seriesName+"<br/>"+e.name+": "+e.value}'
tooltip_result_jscode = 'function test(a){return a.seriesName+"<br/>"+a.name+": "+({0:{alias:"OTHER",color:"#FFFFFF"},1:{alias:"BN",color:"#031A93"},2:{alias:"PAS",color:"#6CB332"},3:{alias:"DAP",color:"#E30911"},4:{alias:"BERJASA",color:"#005121"},5:{alias:"PBB",color:"ADADAD"},6:{alias:"KIMMA",color:"#DE8801"},7:{alias:"PRM",color:"FE8591"},8:{alias:"PBS",color:"#763B37"},9:{alias:"UPKO",color:"#2A0E72"},10:{alias:"PPM",color:"CC9900"},20:{alias:"BEBAS",color:"#993300"},12:{alias:"GERAKAN",color:"#FE2514"},13:{alias:"LDP",color:"#AB3D1A"},14:{alias:"PMS",color:"#FBFD0B"},15:{alias:"AMIPF",color:"#E30300"},16:{alias:"MAP",color:"#F6EB19"},17:{alias:"UMNO",color:"#A03232"},18:{alias:"MCA",color:"#07257F"},19:{alias:"MIC",color:"#00A55E"},11:{alias:"SUPP",color:"#FFFF00"},21:{alias:"PBRS",color:"#6666FF"},22:{alias:"PDP",color:"#0000FD"},23:{alias:"PKR",color:"#04A0D1"},24:{alias:"PRS",color:"#186D43"},25:{alias:"PEJUANG",color:"#09618A"},26:{alias:"PFP",color:"#E45035"},27:{alias:"PN",color:"#043253"},28:{alias:"GAGASAN",color:"#e9d720"},29:{alias:"ASPIRASI",color:"#BD354D"},30:{alias:"PBDS",color:"#0B46C8"},31:{alias:"PH",color:"#D7292F"},32:{alias:"GPS",color:"#1F2C45"},33:{alias:"USNO",color:"#1A740A"},34:{alias:"PUTRA",color:"#FEFE00"},35:{alias:"PSB",color:"#A13C33"},36:{alias:"MUDA",color:"#000000"},37:{alias:"IMAN",color:"#EC1F26"},38:{alias:"SEDAR",color:"#C3B62B"},39:{alias:"M.M.S.P.",color:"#EF8812"},40:{alias:"BERSAMA",color:"#FF66FF"},41:{alias:"PCM",color:"#F4E50E"},42:{alias:"PBM",color:"#323467"},43:{alias:"PSM",color:"#C0110D"},44:{alias:"MCC",color:"#C92725"},45:{alias:"AMANAH",color:"#F79220"},46:{alias:"PPRS",color:"#0000FF"},47:{alias:"ANAKNEGERI",color:"#F6E13A"},48:{alias:"PEACE",color:"#FEF200"},49:{alias:"TERAS",color:"#310051"},50:{alias:"PKS",color:"#3567B2"},51:{alias:"SAPU",color:"#FC771F"},52:{alias:"PAP",color:"#08334C"},53:{alias:"PCS",color:"#DE1E14"},54:{alias:"WARISAN",color:"#5BC5F0"},55:{alias:"BERSATU",color:"#E30007"},56:{alias:"STARSABAH",color:"#0095DB"},57:{alias:"HR",color:"#6F92BF"},58:{alias:"PBK",color:"#672D34"},59:{alias:"IKATAN",color:"#F6E816"},60:{alias:"MU",color:"#ED1D24"},61:{alias:"PERPADUAN",color:"#01AC5C"},62:{alias:"SPP",color:"#c7e011"},63:{alias:"GRS",color:"#6285a8"},64:{alias:"KDM",color:"#EB7389"},65:{alias:"PUR",color:"#ff030b"},66:{alias:"PRIM",color:"#fff"}})[parseInt(a.value)].alias}'

# selected columns names for each category

## one dimensional metrics to use:
## population, income_avg, income_median, household_size_avg, births, deaths
attr_nationality = ["nationality_citizen", "nationality_non_citizen"]
attr_sex = ["sex_male", "sex_female"]
attr_ethnicity = ["ethnicity_bumi", "ethnicity_chinese", "ethnicity_indian", "ethnicity_other"]
attr_religion = ["religion_muslim", "religion_christian", "religion_buddhist", "religion_hindu", "religion_other", "religion_atheist", "religion_unknown"]
attr_married = ["marital_never_married", "marital_married", "marital_widowed", "marital_separated", "marital_unknown"]
attr_age_group = ["age_0_14", "age_15_64", "age_65_above"]
attr_births = ["live_births_male", "live_births_female"]
attr_deaths = ["deaths_male", "deaths_female"]


attr_ethnicity_proportion = ["ethnicity_proportion_bumi", "ethnicity_proportion_chinese", "ethnicity_proportion_indian", "ethnicity_proportion_other"]
attr_age_group_proportion = ["age_proportion_0_14", "age_proportion_15_64", "age_proportion_65_above"]
attr_employment = []

attr_voter_type = ["votertype_regular", "votertype_early_army", "votertype_early_police", "votertype_postal_overseas"]

# census indicators - split by aggregation type (sum / mean)

mean = ["ethnicity_proportion_bumi", "ethnicity_proportion_chinese", "ethnicity_proportion_indian", "ethnicity_proportion_other", "age_proportion_0_14", "age_proportion_15_64", "age_proportion_65_above", "age_proportion_18_above", "household_size_avg", "labour_participation_rate", "labour_unemployment_rate", "income_avg", "income_median", "expenditure_avg", "gini", "poverty_incidence","utilities_pipedwater_home", "utilities_pipedwater_public", "utilities_pipedwater_other", "utilities_electricity_home", "utilities_electricity_none"]
sum = ["area_km2","population_total", "nationality_citizen", "nationality_non_citizen", "sex_male", "sex_female","housing_total","household_total","live_births","live_births_male","live_births_female","deaths","deaths_male","deaths_female","sme_small","sme_micro", "sme_medium", "businesses_agriculture", "businesses_crops", "businesses_livestock", "businesses_fisheries", "businesses_forestry", "businesses_mining", "businesses_manufacturing", "businesses_construction", "businesses_services"]

census_agg_map = dict({metric:"mean" for metric in mean}, **{metric:"sum" for metric in sum})
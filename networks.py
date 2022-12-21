import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv
with open("ling2221_survey_data.csv", 'r') as survey_file:
    reader = csv.reader(survey_file)

    results_table = []
    for row in reader:
        results_table.append(row)

# all accumulators
names_list = []
connections_list = []

belonging_list = []
community_list = []
identity_list = []
terms_known = []
terms_used = []
terms_written = []
programs = []
risdining_days = []
years_in_risley = []
year_of_college = []
risley_again = []

color_by_belonging = []
color_by_community = []
color_by_identity = []
color_by_use = []
color_by_familiarity = []
color_by_terms = []
color_by_programs = []
color_by_risdining_days = []
color_by_year_in_ris = []
color_by_year = []
color_by_risley_again = []
cmap1 = mpl.colormaps['coolwarm']
cmap2 = mpl.colormaps['plasma']


def int_of_year(s):
    if s == 'Freshman' or s == '0-1 years':
        return 1
    if s == 'Sophomore' or s == '1-2 years':
        return 2
    if s == 'Junior' or s == '2-3 years':
        return 3
    if s == 'Senior' or s == '3-4 years':
        return 4


for row in range(3, len(results_table)):
    name = results_table[row][46]
    names_list.append(name)
    num_known = 0
    num_used = 0
    for col in range(18, 38):
        if results_table[row][col] == "I use this term":
            num_known += 1
            num_used += 1
        elif results_table[row][col] == "I am familiar with this term, but do not use it":
            num_known += 1
    terms_known.append(num_known)
    terms_used.append(num_used)
    belonging_list.append(int(results_table[row][43]))
    community_list.append(int(results_table[row][44]))
    identity_list.append(int(results_table[row][45]))
    terms_written.append(int(results_table[row][50]))
    if results_table[row][41] == '6+':
        programs.append(6)
    else:
        programs.append(int(results_table[row][41]))
    years_in_risley.append(int_of_year(results_table[row][39]))
    year_of_college.append(int_of_year(results_table[row][38]))
    risdining_days.append(int(results_table[row][42]))
    if results_table[row][40] == 'Yes':
        risley_again.append(2)
    elif results_table[row][40] == 'Not sure' or results_table[row][40] == 'N/A (Graduating/transferring)':
        risley_again.append(1)
    else:
        risley_again.append(0)


for row in range(3, len(results_table)):
    name = results_table[row][46]
    friends = results_table[row][49].split(", ")
    for friend in friends:
        if friend in names_list:
            connections_list.append((name, friend))

# low knowledge: 0-12
# medium knowledge: 13-16
# high knowledge: 17-18
# very high knowledge: 19-20

# very low use: 1-5
# low use: 6-10
# medium use: 11-15
# high use: 16-20


def get_avg_sentiment(vocab_list, sentiment_list, low, high):
    acc = 0
    counter = 0
    for i in range(len(vocab_list)):
        if vocab_list[i] >= low and vocab_list[i] <= high and sentiment_list[i] != -1 and sentiment_list[i] != 144:
            acc += sentiment_list[i]
            counter += 1
    if counter != 0:
        return acc/counter
    else:
        return -1


x_knowledge = ['low', 'medium', 'high', 'very high']
x_use = ['very low', 'low', 'medium', 'high']
belonging_knowledge_y = [get_avg_sentiment(terms_known, belonging_list, 0, 12), get_avg_sentiment(
    terms_known, belonging_list,  13, 16), get_avg_sentiment(terms_known, belonging_list,  17, 18), get_avg_sentiment(terms_known, belonging_list,  19, 20)]
belonging_use_y = [get_avg_sentiment(terms_used, belonging_list, 0, 5), get_avg_sentiment(terms_used, belonging_list,  6, 10), get_avg_sentiment(
    terms_used, belonging_list,  11, 15), get_avg_sentiment(terms_used, belonging_list,  16, 20)]

community_knowledge_y = [get_avg_sentiment(terms_known, community_list, 0, 12), get_avg_sentiment(terms_known, community_list,  13, 16), get_avg_sentiment(
    terms_known, community_list,  17, 18), get_avg_sentiment(terms_known, community_list,  19, 20)]
community_use_y = [get_avg_sentiment(terms_used, community_list, 0, 5), get_avg_sentiment(terms_used, community_list,  6, 10), get_avg_sentiment(
    terms_used, community_list,  11, 15), get_avg_sentiment(terms_used, community_list,  16, 20)]

identity_knowledge_y = [get_avg_sentiment(terms_known, identity_list, 0, 12), get_avg_sentiment(
    terms_known, identity_list,  13, 16), get_avg_sentiment(terms_known, identity_list,  17, 18), get_avg_sentiment(terms_known, identity_list,  19, 20)]
identity_use_y = [get_avg_sentiment(terms_used, identity_list, 0, 5), get_avg_sentiment(terms_used, identity_list,  6, 10), get_avg_sentiment(
    terms_used, identity_list,  11, 15), get_avg_sentiment(terms_used, identity_list,  16, 20)]

terms_programs_y = [get_avg_sentiment(programs, terms_written, 0, 1), get_avg_sentiment(
    programs, terms_written, 2, 2), get_avg_sentiment(programs, terms_written, 3, 6)]
terms_knowledge_y = [get_avg_sentiment(programs, terms_known, 0, 1), get_avg_sentiment(
    programs, terms_known, 2, 2), get_avg_sentiment(programs, terms_known, 3, 6)]


plt.plot(['0-1', '2', '3+'], terms_programs_y)
plt.ylim(0, 15)
plt.xlabel('Risley programs attended per week')
plt.ylabel('Average number of terms given in response')
plt.title('Involvement vs. terms given')
plt.show()

plt.plot(['0-1', '2', '3+'], terms_knowledge_y)
plt.ylim(0, 20)
plt.xlabel('Risley programs attended per week')
plt.ylabel('Average number of terms known of 20')
plt.title('Involvement vs. familiarity with jargon')
plt.show()

plt.plot(x_knowledge, belonging_knowledge_y, label="Belonging")
plt.plot(x_knowledge, community_knowledge_y, label="Community")
plt.plot(x_knowledge, identity_knowledge_y, label="Identity")
plt.ylim(0, 6)
plt.xlabel('Familiarity with in-group vocabulary')
plt.ylabel('Average agreement with belonging/community/identity statements')
plt.title('Familiarity with jargon vs. belonging/community/identity')
plt.legend()
plt.show()


plt.plot(x_use, belonging_use_y, label="Belonging")
plt.plot(x_use, community_use_y, label="Community")
plt.plot(x_use, identity_use_y, label="Identity")
plt.ylim(0, 6)
plt.xlabel('Use of in-group vocabulary')
plt.ylabel('Average agreement with belonging/community/identity statements')
plt.title('Use of jargon vs. belonging/community/identity')
plt.legend()
plt.show()

# Function sourced from: https://stackoverflow.com/a/62799153


def map_to_color(value, cmap_name, vmin=0, vmax=1):
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)
    rgb = cmap(norm(abs(value)))[:3]
    color = mpl.colors.rgb2hex(rgb)
    return color


for num in terms_used:
    color_by_use.append(map_to_color(num, cmap1, 0, 20))

for num in terms_known:
    color_by_familiarity.append(map_to_color(num, cmap1, 10, 20))

for num in terms_written:
    color_by_terms.append(map_to_color(num, cmap1, 0, 20))

for num in year_of_college:
    color_by_year.append(map_to_color(num, cmap2, 1, 4))

for num in years_in_risley:
    color_by_year_in_ris.append(map_to_color(num, cmap2, 1, 4))

for num in programs:
    color_by_programs.append(map_to_color(num, cmap1, 0, 6))

for num in belonging_list:
    color_by_belonging.append(map_to_color(num, cmap1, 0, 6))

for num in community_list:
    color_by_community.append(map_to_color(num, cmap1, 0, 6))

for num in identity_list:
    color_by_identity.append(map_to_color(num, cmap1, 0, 6))

for num in risdining_days:
    color_by_risdining_days.append(map_to_color(num, cmap1, 0, 5))

for num in risley_again:
    color_by_risley_again.append(map_to_color(num, cmap1, 0, 2))

G_year = nx.MultiDiGraph()
G_year.add_nodes_from(names_list)
G_year.add_edges_from(connections_list)
G_year_anonymous = nx.convert_node_labels_to_integers(G_year)
plt.title(
    "Social network by year in university [Blue–Freshmen, Purple–Sophomore, Orange–Junior, Yellow–Senior]")
nx.draw(G_year_anonymous, pos=nx.kamada_kawai_layout(G_year_anonymous, center=[8, 20]),
        with_labels=True, node_color=color_by_year
        )
plt.show()

G_id = nx.MultiDiGraph()
G_id.add_nodes_from(names_list)
G_id.add_edges_from(connections_list)
G_id_anonymous = nx.convert_node_labels_to_integers(G_id)
plt.title(
    "Social network by Risley identity [Cool-Low, Warm-High]")
nx.draw(G_id_anonymous, pos=nx.kamada_kawai_layout(G_id_anonymous, center=[8, 20]),
        with_labels=True, node_color=color_by_identity
        )
plt.show()

G_fam = nx.MultiDiGraph()
G_fam.add_nodes_from(names_list)
G_fam.add_edges_from(connections_list)
G_fam_anonymous = nx.convert_node_labels_to_integers(G_fam)
plt.title(
    "Social network by Risley vocab familiarity [Cool-Low, Warm-High]")
nx.draw(G_fam_anonymous, pos=nx.kamada_kawai_layout(G_fam_anonymous, center=[8, 20]),
        with_labels=True, node_color=color_by_familiarity
        )
plt.show()

G_use = nx.MultiDiGraph()
G_use.add_nodes_from(names_list)
G_use.add_edges_from(connections_list)
G_use_anonymous = nx.convert_node_labels_to_integers(G_use)
plt.title(
    "Social network by Risley vocab use [Cool-Low, Warm-High]")
nx.draw(G_use_anonymous, pos=nx.kamada_kawai_layout(G_use_anonymous, center=[8, 20]),
        with_labels=True, node_color=color_by_use
        )
plt.show()

import pandas as pd
import networkx as nx

def make_edge_list(df: pd.DataFrame) -> list:
    from_len = df["prereq"].apply(lambda x: len(x))
    to_list = from_len * df["label"].apply(lambda x: [x])

    edge_list = []
    for n, row in df.iterrows():
        from_len = len(row[2])
        to_list = [row[0]] * from_len
        edges = list(zip(row[2], to_list))
        edge_list += edges
    return edge_list

def make_node_list(df: pd.DataFrame) -> (list, list):
    node_list = list(set(df["label"].to_list() + df["prereq"].sum()))
    title_list = []
    for node in node_list:
        title = df[df["label"]==node]["name"]
        title = node if title.empty else title.item()
        title_list.append(title)
    return node_list, title_list

def make_nx_graph(subjects: list):
    # read data
    df = pd.DataFrame()
    for subject in subjects:
        courses = pd.read_json(f"courses/{subject}.json")
        df = pd.concat([df, courses])

    g = nx.DiGraph() # NetworkX directed graph
    edge_list = make_edge_list(df)
    g.add_edges_from(edge_list)
    print(g)
    return g
    




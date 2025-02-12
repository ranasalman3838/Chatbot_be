from langgraph.graph import StateGraph, START, END
from app.schemas.graph_schemas import  State
from app.graph.graph_nodes import graph_obj



class GraphModel:
    def __init__(self):
        self.graph_builder = StateGraph(State)
        # Add nodes to the graph
        self.graph_builder.add_node("classification_node", graph_obj.classification_node)
        self.graph_builder.add_node("entity_extraction", graph_obj.entity_extraction_node)
        self.graph_builder.add_node("summarization", graph_obj.summarization_node)

        # Add edges to the graph
        self.graph_builder.set_entry_point("classification_node")  # Set the entry point of the graph
        self.graph_builder.add_edge("classification_node", "entity_extraction")
        self.graph_builder.add_edge("entity_extraction", "summarization")
        self.graph_builder.add_edge("summarization", END)






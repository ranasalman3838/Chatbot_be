from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.setting import settings



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=settings.OPENAI_API_KEY)

class GraphNodes:

    @staticmethod
    def classification_node(state):
        ''' Classify the text into one of the categories: News, Blog, Research, or Other '''
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Classify the following text into one of the categories: News, Blog, Research, or Other.\n\nText:{text}\n\nCategory:"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        classification = llm.invoke([message]).content.strip()
        return {"classification": classification}

    @staticmethod
    def entity_extraction_node(state):
        ''' Extract all the entities (Person, Organization, Location) from the text '''
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Extract all the entities (Person, Organization, Location) from the following text. Provide the result as a comma-separated list.\n\nText:{text}\n\nEntities:"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        entities = llm.invoke([message]).content.strip().split(", ")
        return {"entities": entities}

    @staticmethod
    def summarization_node(state):
        ''' Summarize the text in one short sentence '''
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following text in one short sentence.\n\nText:{text}\n\nSummary:"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        summary = llm.invoke([message]).content.strip()
        return {"summary": summary}


graph_obj = GraphNodes()
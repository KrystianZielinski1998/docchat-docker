
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

from utils.logging import logger


class ResearchAgent:
    def __init__(self):
        """
        Initialize the research agent with ChatOpenAI.
        """
        # Initialize the gpt-4o-mini model
        logger.info("Initializing ResearchAgent with ChatOpenAI...")
        self.llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=300, temperature=0.3)
        logger.info("ResearchAgent initialized successfully.")

    def _build_prompt(self, question: str, context: str) -> ChatPromptTemplate:
        """
        Generate a structured prompt for the LLM to generate a precise and factual answer.
        """

        return ChatPromptTemplate.from_template(
            """
            You are an AI assistant designed to provide precise and factual answers based on the given context.

            **Instructions:**
            - Answer the following question using only the provided context.
            - Be clear, concise, and factual.
            - Return as much information as you can get from the context.
            
            **Question:** {question}
            **Context:** {context}

            **Provide your answer below:**
            """
        )

    def generate(self, question: str, documents: list[Document]) -> dict:
        """
        Generate an initial answer using the provided documents.
        """
        logger.info(
            f"ResearchAgent.generate called with question='{question}' and {len(documents)} documents."
        )

        # Combine the top document contents into one string
        context = "\n\n".join([doc.page_content for doc in documents])
        logger.debug(f"Combined context length: {len(context)} characters.")

        # Get template prompt
        prompt = self._build_prompt(question, context)

        # Create a chain: format prompt → send to LLM → parse output to string
        chain = prompt | self.llm | StrOutputParser()

        # Call the LLM
        try:
            llm_response = chain.invoke({"question": question, "context": context})

        except (ValueError, KeyError, TypeError) as e:
            logger.error(f"Error during ResearchAgent inference: {e}")
            raise RuntimeError("Failed to generate answer due to a model error.") from e

        # Sanitize the response
        draft_answer = (
            llm_response.strip()
            if llm_response
            else "I cannot answer this question based on the provided documents."
        )

        return {"draft_answer": draft_answer, "context_used": context}

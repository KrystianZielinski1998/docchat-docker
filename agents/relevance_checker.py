from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from config.settings import settings
import re
from utils.logging import logger

class RelevanceChecker:
    def __init__(self):
        """
        Initialize the relevance checker agent with ChatOpenAI.
        """

        # Initialize the ChatOpenAI
        logger.info("Initializing RelevanceChecker Agent with ChatOpenAI...")
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            max_tokens=10,
            temperature=0
        )
        logger.info("RelevanceChecker Agent initialized successfully.")

    def _build_prompt(self, question: str, document_content: str) -> ChatPromptTemplate:
        """ Builds a structured prompt template for RelevanceChecker Agent. """

        return ChatPromptTemplate.from_template(
            """
            You are given a user question and some passages from uploaded documents.
            
            Classify how well these passages address the user's question. 
            Choose exactly one of the following responses (respond ONLY with that label):
            
            1) "CAN_ANSWER": The passages contain enough explicit info to fully answer the question.
            2) "PARTIAL": The passages mention or discuss the question's topic (e.g., relevant years, facility names)
            but do not provide all the data or details needed for a complete answer.
            3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.
            
            Important: If the passages mention or reference the topic or timeframe of the question in ANY way,
            even if incomplete, you should respond "PARTIAL", not "NO_MATCH".
            
            Question: {question}
            Passages: {document_content}
            
            Respond ONLY with "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
            """
        )

    def check(self, question: str, retriever, k=3) -> str:
        """
        1. Retrieve the top-k document chunks from the global retriever.
        2. Combine them into a single text string.
        3. Pass that text + question to the LLM for classification.

        Returns: "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
        """

        logger.info(f"RelevanceChecker.check called with question='{question}' and k={k}")

        # Retrieve doc chunks from the ensemble retriever
        top_docs = retriever.invoke(question)
        if not top_docs:
            logger.warning("No documents returned from retriever.invoke(). Classifying as NO_MATCH.")
            return "NO_MATCH"

        # Combine the top k chunk texts into one string
        document_content = "\n\n".join(doc.page_content for doc in top_docs[:k])

        # Get template prompt
        prompt =  self._build_prompt(question, document_content)

        # Create a chain: format prompt → send to LLM → parse output to string
        chain = prompt | self.llm | StrOutputParser()

        # Call the LLM
        try:
            llm_response = chain.invoke({
               "question": question,
               "document_content": document_content     
            })

            llm_response = llm_response.strip().upper()

        except (ValueError, KeyError, TypeError) as e:
            logger.error(f"Error during RelevanceChecker agent inference: {e}")
            return "NO_MATCH"

        # Validate the response
        valid_labels = {"CAN_ANSWER", "PARTIAL", "NO_MATCH"}
        if llm_response not in valid_labels:
            logger.debug("LLM did not respond with a valid label. Forcing 'NO_MATCH'.")
            classification = "NO_MATCH"
        else:
            logger.debug(f"Classification recognized as '{llm_response}'.")
            classification = llm_response

        return classification

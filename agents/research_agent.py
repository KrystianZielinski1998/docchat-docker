from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Dict, List
from langchain.schema import Document
import json


class ResearchAgent:
    def __init__(self):
        """
        Initialize the research agent with the IBM WatsonX ModelInference.
        """
        # Initialize the gpt-4o-mini model
        print("Initializing ResearchAgent with IBM WatsonX ModelInference...")
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", 
            max_tokens=300,            # Adjust based on desired response length
            temperature=0.3           # Controls randomness; lower values make output more deterministic
        )
        print("ResearchAgent initialized successfully.")

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

    def generate(self, question: str, documents: List[Document]) -> Dict:
        """
        Generate an initial answer using the provided documents.
        """
        print(f"ResearchAgent.generate called with question='{question}' and {len(documents)} documents.")

        # Combine the top document contents into one string
        context = "\n\n".join([doc.page_content for doc in documents])
        print(f"Combined context length: {len(context)} characters.")

        # Get template prompt
        prompt =  self._build_prompt(question, context)

        # Create a chain: format prompt → send to LLM → parse output to string
        chain = prompt | self.llm | StrOutputParser()

        # Call the LLM 
        try:
            print("Sending prompt to the model...")
            llm_response = chain.invoke({
               "question": question,
               "context": context     
            })
            
            print("LLM response received.")

        except Exception as e:
            print(f"Error during model inference: {e}")
            raise RuntimeError("Failed to generate answer due to a model error.") from e


        # Sanitize the response
        draft_answer = llm_response.strip() if llm_response else "I cannot answer this question based on the provided documents."

        print(f"Generated answer: {draft_answer}")

        return {
            "draft_answer": draft_answer,
            "context_used": context
        }

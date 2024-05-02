from typing import Optional

from bigquery_class import BigQueryClass
from gemini_class import GeminiClass
from model import Model

# This list was extracted from Google International Search Trends. We can't answer questions about specific countries that are not included here.
INTERNATIONAL_TRENDS_COUNTRY_LIST = [
    "Argentina",
    "Australia",
    "Austria",
    "Belgium",
    "Brazil",
    "Canada",
    "Chile",
    "Colombia",
    "Czech Republic",
    "Denmark",
    "Egypt",
    "Finland",
    "France",
    "Germany",
    "Hungary",
    "India",
    "Indonesia",
    "Israel",
    "Italy",
    "Japan",
    "Malaysia",
    "Mexico",
    "Netherlands",
    "New Zealand",
    "Nigeria",
    "Norway",
    "Philippines",
    "Poland",
    "Portugal",
    "Romania",
    "Saudi Arabia",
    "South Africa",
    "South Korea",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Thailand",
    "Turkey",
    "Ukraine",
    "United Kingdom",
    "Vietnam"
]

class AskGoogleTrends:
    """Handles ask Google Trends logic flow."""
    def __init__(self):
        self.load_data_sources()

    def ask(self, question: str) -> str:
        """Executes the following steps:
    
        Step 1. Based on user input, use an LLM to check for a relevant data source.
        Step 2. Query the matched data source. If relevant data source does not exist, tell the user and bail out.
        Step 3. Take the data output results and provide it for context to ask the LLM to answer the question.
        Step 4. Return the results to the user.
        """
        print(f"User question: {question}")

        # Step 1. Based on user input, use an LLM to check for a relevant data source.
        response = self.get_data_source(question).strip()
        print(f"Step 1. Data source LLM response: {response}")

        # Step 2. Query the matched data source. If relevant data source does not exist, tell the user and bail out.
        if response in INTERNATIONAL_TRENDS_COUNTRY_LIST:
            print(f"Detected country: {response}")
            data_results = self.query_datasource("International Google Trends", response)
        elif response in self.data_source_labels:
            data_results = self.query_datasource(response)
        else:
            print("Step 2. No data source found. Returning LLM response and exiting...")
            return response

        # Step 3. Take the data output results and provide it for context to ask the LLM to answer the question.
        answer = self.get_answer(question, data_results)

        # Step 4. Return the results to the user.
        return answer
    
    def get_answer(self, question: str, data_results: str) -> str:
        prompt = f"""
        Answer the following question based on the provided trending topics. When in doubt, answer with the most recent data
        
        Question:
        {question}

        Google Search trends data:
        {data_results}
        """
        return self.execute_prompt(prompt)

    def get_data_source(self, question: str) -> str:
        prompt_prefix = f"""
        Based on the following question, determine which data source or country source is best suited to provide an answer. Respond with just the data source or country name. If none of these data sources or countries are relevant, respond with a reason why you do not have an answer.
        
        Data Sources:
        {self.data_sources_labels_display}

        Country Sources:
        {"\n".join(INTERNATIONAL_TRENDS_COUNTRY_LIST)}
        """

        examples = [
            {
                "question": "What was trending in the US?",
                "answer": "US Google Trends"
            },
            {
                "question": "What has been trending outside of the US?",
                "answer": "International Google Trends"
            },
            {
                "question": "What is popular in Africa?",
                "answer": "International Google Trends"
            }
        ]

        prompt = ""
        for example in examples:
            prompt += f"""
                {prompt_prefix}

                Question: {example['question']}

                Answer: {example['answer']}   
            """

        prompt += f"""
            {prompt_prefix}

            Question: {question}

            Answer:
        """

        print(prompt)
        return self.execute_prompt(prompt)
    
    def execute_prompt(self, prompt: str) -> str:
        """Google Cloud Gemini text model generation."""

        # Configure your model settings
        model = Model(
            model_family="Gemini",
            model_version="gemini-1.5-pro-preview-0409",
            service="Google Cloud",
            max_output_tokens=2048,
            temperature=0.8,
            top_k=40,
            top_p=1)
        
        g = GeminiClass(model)
        response = g.generate(prompt)
        return response
    
    def load_data_sources(self):
        # Using the two Top Trends datasets for now. Can also add Top Rising Trends for US and International as well.
        self.data_sources = {
            "US Google Trends": "WITH abc AS (SELECT term, rank, week FROM `bigquery-public-data.google_trends.top_terms` GROUP BY term, rank, week ORDER BY week DESC, rank ASC) SELECT DISTINCT term, rank, week FROM abc ORDER BY week DESC, rank ASC LIMIT 50000",
            "International Google Trends": "WITH abc AS (SELECT term, rank, week FROM `bigquery-public-data.google_trends.international_top_terms` GROUP BY term, rank, week ORDER BY week DESC, rank ASC) SELECT DISTINCT term, rank, week FROM abc ORDER BY week DESC, rank ASC LIMIT 50000",
        }
        self.data_source_labels = list(self.data_sources.keys())

        self.data_sources_labels_display = ""
        for label in self.data_source_labels:
            self.data_sources_labels_display += f"* {label}\n"
        
    def query_datasource(self, data_source: str, country: Optional[str] = "") -> str:
        """Queries a given data source."""
        if country:
            query = self.data_sources[data_source]
            # Hacky WHERE clause insertion but it works
            query = query.replace(
                "GROUP BY",
                f"WHERE country_name = '{country}' GROUP BY"
            )
            print(f"replaced query: {query}")
        else:
            query = self.data_sources[data_source]
        
        # Execute query + truncates results
        db = BigQueryClass()
        response = db.run_query(query)
        results = "term, rank, week\n" + str(response[:500000])
        print(f"First 500 characters of query results: {results[:500]}")
        return results
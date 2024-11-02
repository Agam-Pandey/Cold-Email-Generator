import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

             ### INSTRUCTION:
                You are ABC, a PGDM - Big Data Analytics student. You are in the final year of your course completion.
                This is a part of your resume so pick out the key elements from this resume that aligns with the job description draft the email accordingly, "NASSCOM, Noida            Data Analytics & Data Management Intern                                                  May’24-Sept’24 
                Data Analysis & Management 
                • Led a data cleansing and automation project for NASSCOM’s existing client database to support the Future Works 
                event, focusing on improving client engagement and outreach by enhancing data quality, streamlining processes 
                • Automated database management using Selenium, reducing manual data entry by 70%, while identifying potential 
                clients and ensuring that the dataset remains up-to-date and accurate for targeted marketing 
                • Created a dynamic Power BI dashboard by consolidating 6 years of event data using Python, significantly enhancing 
                data accuracy by 25% through ETL processes to provide actionable insights for improved decision-making 
                • Extracted actionable insights from multi-year event data, identifying key trends in attendee growth and demographic 
                profiles, leading to a 10% increase in event attendance and better event performance forecasting 
                • Improved decision-making for NASSCOM’s Konnect team by delivering a comprehensive analysis of revenue patterns 
                and company participation, contributing to a 20% improvement in event management efficiency 
                 
 
                Academic Achievements & Certifications 
                • National winners in the "WeShleshan 2024" Business Case Study Competition, addressing a supply chain challenge among 668 top B-School teams 
                • Advanced to the penultimate round of Bitathon Hackathon 2024, a 24-hour event by Goa Institute of Management, competing against 1315 teams 
                • Progressed to the Round 3 penultimate stage of Tata Imagination Challenge 2023, amidst stiff competition from 2,63,652 registered candidates 
                • Secured 3rd rank in the Python Challenge Bootcamp conducted in GIM out of a total of more than 90 teams and 540 participants 
                • Awarded First Division with Honors in Under graduation and constantly being in the Top 5% of the batch for all 4 years 
                • Earned a certification in Prompt Engineering for generative AI by LinkedIn, 2024 
                • Certified in AI for Managers by Microsoft and LinkedIn, 2024  
                • Certified in Python by Coursera and IBM, 2023 
                Live/ Academic Projects 
                Employee Churn Rate Analysis & Prediction 
                • Performed exploratory data analysis (EDA) and visualization using Python to identify key employee churn factors, 
                leveraging clustering techniques to segment employees based on behaviour and churn risk 
                • Conducted K-means clustering to identify and categorize employee segments based on satisfaction and evaluation 
                scores, uncovering distinct churn risk profiles and informing targeted retention strategies and interventions 
                • Developed and deployed a predictive model utilizing Gradient Boosting Classifier, achieving 97% accuracy in 
                forecasting employee turnover. The model was trained on features such as number of projects, workload, and salary 
                levels, enabling precise predictions and informed decision-making to address potential employee churn 
                • Evaluated model performance using precision and recall metrics, achieving a precision score of 95% and recall of 
                92%, demonstrating the model’s ability to accurately predict employees at risk of leaving. These insights supported 
                the development of retention strategies in a simulated environment
                Core Competencies - 
                Software Packages • Microsoft Power BI, Tableau, Azure ML Studio, Apache Spark, SAS Studio, Microsoft Excel, Microsoft PowerPoint 
                Programming  • Python, SQL, R"

                Your job is to write a cold email to the client regarding the job mentioned above describing the your capability 
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase your portfolio: {link_list}
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
        
                """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
import os
import json
import asyncio
import logging
from openai import OpenAI
from dotenv import load_dotenv

from app.models import Employee, Client, ClientPayment, PredefinedQueries

# Load environment and configure logging
load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_schema_definition():
    """
    Generate a table:columns mapping from SQLAlchemy models.
    """
    def extract_model_fields(model):
        return [col.name for col in model.__table__.columns]

    schema = {
        "employees": extract_model_fields(Employee),
        "clients": extract_model_fields(Client),
        "client_payments": extract_model_fields(ClientPayment),
        "predefined_queries": extract_model_fields(PredefinedQueries)
    }
    return json.dumps(schema, indent=2)

async def text_to_query(text: str) -> str:
    """
    Use GPT-4 to convert natural language to a JSON array of SQL queries (supports CRUD).
    """
    schema = get_schema_definition()

    prompt = f"""
You are an expert SQL assistant.

Users will ask questions in casual English using various phrasings, like:
- "How many employees do we have?"
- "Can I see their names?"
- "What's the max salary?"
- "Add employee Riya, HR, 45000"
- "Update John's salary to 70000"
- "Delete client named Acme"
- "Update budget in Dezdok as 100000"
- "Insert payment received amount for Acme as 5000"
- "What is the total sale this month?"

Your job is to convert such natural language into a **JSON array of SQL queries** as strings, based on this schema:

{schema}

⚠️ Instructions:
- Return only valid SQL queries in a JSON array (no markdown, no comments).
- Do not explain anything.
- Do not wrap the response in ```json.
- For UPDATE or DELETE: always include a WHERE clause (never affect full table).
- For name-based conditions: use `LOWER(column) = 'value_in_lowercase'`.
- For INSERT into `client_payments` using a name, use subquery:  
  `(SELECT id FROM clients WHERE LOWER(name) = 'client_name')` to resolve client_id.
- If the user mentions "sale" or "sales", assume they mean the `budget` field in the `clients` table.
- If user asks for "sales this month", use the condition:  
  `DATE_TRUNC('month', project_start_date) = DATE_TRUNC('month', CURRENT_DATE)`
- Always use PostgreSQL-compatible SQL (e.g., no MONTH() or YEAR() functions).
- Only reference fields or tables defined in the schema.

User question: "{text}"
"""

    try:
        logger.debug(f"Sending prompt to GPT:\n{prompt}")
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that only returns SQL queries as a JSON array."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        sql_output = response.choices[0].message.content.strip()

        # Clean accidental markdown
        if sql_output.startswith("```json"):
            sql_output = sql_output.removeprefix("```json").strip()
        if sql_output.endswith("```"):
            sql_output = sql_output.removesuffix("```").strip()

        logger.debug(f"SQL from GPT:\n{sql_output}")
        return sql_output

    except Exception as e:
        logger.error(f"GPT failed: {str(e)}")
        return json.dumps([f"-- Error: {str(e)}"])

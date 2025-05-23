import json
import re
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import get_current_user
from app.utils.nlp_utils import text_to_query
from app.database import get_db
from app import models  # ✅ Needed for PredefinedQueries

router = APIRouter(tags=["Chatbot"])

class NLQuery(BaseModel):
    text: str

def keyword_based_fallback(user_input: str):
    user_input = user_input.lower()
    fallback_queries = []

    if "employee" in user_input and "count" in user_input:
        fallback_queries.append("SELECT COUNT(*) FROM employees;")
    if "employee" in user_input and "name" in user_input:
        fallback_queries.append("SELECT name FROM employees;")
    if "client" in user_input and "count" in user_input:
        fallback_queries.append("SELECT COUNT(*) FROM clients;")
    if "client" in user_input and "name" in user_input:
        fallback_queries.append("SELECT name FROM clients;")
    if "salary" in user_input and "max" in user_input:
        fallback_queries.append("SELECT MAX(salary) FROM employees;")

    return fallback_queries

@router.post("/convert-to-sql")
async def convert_to_sql(
    query: NLQuery,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("🚀 convert_to_sql endpoint hit")

    # 1. Check if question already exists
    cached_query = db.query(models.PredefinedQueries).filter(
        models.PredefinedQueries.question.ilike(query.text)
    ).first()

    if cached_query:
        print("📦 Using cached query from database")
        sql_list = f'["{cached_query.sql_query}"]'
    else:
        print("🤖 Generating new query using GPT")
        sql_list = await text_to_query(query.text)

    try:
        queries = json.loads(sql_list)
        if not isinstance(queries, list):
            raise ValueError("GPT response is not a list.")
    except Exception as e:
        queries = keyword_based_fallback(query.text)
        if not queries:
            raise HTTPException(
                status_code=400,
                detail=f"GPT failed and no fallback matched.\nGPT Error: {e}\nRaw: {sql_list}"
            )

    executed_sql = []
    response_lines = []

    try:
        for sql in queries:
            cleaned_sql = sql.strip().rstrip(";")

            # Subquery replacement for client ID
            if (
                "insert into client_payments" in cleaned_sql.lower()
                and "select id from clients" in cleaned_sql.lower()
            ):
                match = re.search(r"LOWER\(name\) = '(.+?)'", cleaned_sql, re.IGNORECASE)
                if match:
                    client_name = match.group(1).lower()
                    result = db.execute(
                        text("SELECT id FROM clients WHERE LOWER(name) = :name"),
                        {"name": client_name}
                    ).fetchone()
                    if result:
                        client_id = result[0]
                        cleaned_sql = re.sub(
                            r"\(SELECT id FROM clients WHERE LOWER\(name\) = '(.+?)'\)",
                            str(client_id),
                            cleaned_sql
                        )
                    else:
                        raise HTTPException(status_code=404, detail=f"Client '{client_name}' not found.")

            executed_sql.append(cleaned_sql)

            # Block unsafe queries
            if cleaned_sql.lower().startswith(("update", "delete")) and "where" not in cleaned_sql.lower():
                raise HTTPException(status_code=400, detail="Unsafe SQL: missing WHERE clause.")

            # Execute the SQL
            if cleaned_sql.lower().startswith("select"):
                result = db.execute(text(cleaned_sql)).fetchall()
                if result:
                    row_dict = dict(result[0]._mapping)
                    if len(row_dict) == 1:
                        key, value = list(row_dict.items())[0]
                        response_lines.append(f"{key}: {value}")
                    else:
                        for row in result:
                            flat = dict(row._mapping)
                            response_lines.append(", ".join(f"{k}: {v}" for k, v in flat.items()))
                else:
                    response_lines.append("No results.")
            elif cleaned_sql.lower().startswith(("insert", "update", "delete")):
                db.execute(text(cleaned_sql))
                db.commit()
                response_lines.append(f"{cleaned_sql.split()[0].upper()} executed successfully.")
            else:
                response_lines.append(f"Unsupported SQL command: {cleaned_sql}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution failed: {str(e)}")

    # Check if success occurred (insert/update/delete or select returned data)
    success = any("successfully" in line.lower() or ":" in line for line in response_lines)

    # 2. Store successful, non-cached query
    if success and not cached_query and executed_sql:
        try:
            new_predefined_query = models.PredefinedQueries(
                question=query.text,
                sql_query=executed_sql[0]
            )
            db.add(new_predefined_query)
            db.commit()
            print("💾 Stored successful query in database")
        except Exception as e:
            print(f"❌ Failed to store query in database: {str(e)}")
            db.rollback()

    return {
        "user": user,
        "question": query.text,
        "sql": executed_sql,
        "response": "\n".join(response_lines)
    }

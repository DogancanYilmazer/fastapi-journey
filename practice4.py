# ============================================================
# Practice 4 — Path & Query Parameters
# ============================================================
# In this practice you will:
#   1. Create an endpoint that accepts a PATH parameter
#   2. Create an endpoint that accepts a QUERY parameter
#   Both endpoints search the crew list and return the matching member.
#
# To run:
#   uvicorn practice4:app --port 8000 --reload
#
# Test path parameter:
#   http://127.0.0.1:8000/crew_with_path/1
#
# Test query parameter:
#   http://127.0.0.1:8000/crew_with_query/member?crew_id=1
#
# HINT: Use `crew_id: int` in your function signature so FastAPI
#       automatically converts the value to an integer.
#
# Provided helper — use this logic inside both endpoints:
#
#   for member in crew:
#       if member["id"] == crew_id:
#           return member
#   return {"message": "Crew member not found"}
# ============================================================

from fastapi import FastAPI

# Initialize a FastAPI app instance
myapp = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob",   "role": "Scientist"},
]


# TODO: Write an endpoint to get a crew member by PATH parameter
#       Endpoint path: /crew_with_path/{crew_id}
@myapp.get("/crew_with_path/{crew_id}")  # http://127.0.0.1:8000/crew_with_path/1
def get_crew_member_by_path(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member
    return {"message": "Crew member not found"}

# TODO: Write an endpoint to get a crew member by QUERY parameter
#       Endpoint path: /crew_with_query/member
@myapp.get("/crew_with_query/member")  # http://127.0.0.1:8000/crew_with_query/member?crew_id=1
def get_crew_member_by_query(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member
    return {"message": "Crew member not found"}
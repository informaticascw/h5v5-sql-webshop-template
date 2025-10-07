#
# This is a simple FastAPI application that serves a static HTML site and provides API endpoints:
#
# source for base code https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
# extended using copilot

import sqlite3
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#
# serve API endpoints like /api/products
#

# Function to convert a row into a dictionary using field names as keys
def dict_factory(cursor, row):
    result = {}
    for i in range(len(cursor.description)):
        column_name = cursor.description[i][0]
        value = row[i]
        result[column_name] = value
    return result

# API endpoint to get a list of products
@app.get("/api/products")
def get_products(
    # declare all parameters that may be added to the query
    merk: list[str] = Query(default=[]),
    kleur: list[str] = Query(default=[])
):
    # init
    brand_filter_values = merk # list of all brands in the filter
    color_filter_values = kleur # list of all colors in the filter
    print("API: Starting /api/products endpoint")
    print("API: Parameters - merk:", brand_filter_values, ", kleur:", color_filter_values)
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert each row into a dictionary

    # Build the base query
    query = """
        SELECT *
        FROM products
    """
    query_params = []

    # Execute the query
    print("API: Query submitted:", query)
    print("API: Query parameters:", query_params)
    product_rows = db_connection.execute(query, query_params).fetchall()
    print("API: Query result (first 3 rows):", product_rows[:3])

    # Return result
    db_connection.close()
    print("API: Finished /api/products endpoint") 
    return {"products": product_rows}

# API endpoint to get all properties and values for filters
@app.get("/api/filters")
def get_filters():
    # init
    print("API: Starting /api/filters endpoint")  
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert each row into a dictionary

    # Construct the response
    filters = {
    }

    # Return result
    db_connection.close()
    print("API: Finished /api/filters endpoint")  
    return {"filters": filters}

#
# Serve static files like index.html, script.js, etc.
#

# Do not cache static files, handy for development but it slows down loading the webpage
class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers.update({
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        return response

# Endpoint to serve static files
app.mount("/", NoCacheStaticFiles(directory="static", html=True), name="static")

#
# Start server
#
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
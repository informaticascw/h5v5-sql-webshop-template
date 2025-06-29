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
    soort: list[str] = Query(default=[]),
    kleur: list[str] = Query(default=[])
):
    print("API: Starting /api/products endpoint")
    print("API: Parameters - soort:", soort, ", kleur:", kleur)
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert each row into a dictionary

    # Build the base query
    query = """
        SELECT 
            prod.id, 
            prod.name, 
            prod.image_link,
            prod.price, 
            cat.name AS soort
        FROM products prod
        LEFT JOIN categories cat ON prod.category_id = cat.id
        LEFT JOIN product_colors prodcol ON prod.id = prodcol.product_id
        LEFT JOIN colors col ON prodcol.color_id = col.id
    """

    # Filter soort (category in database)
    category_params = soort
    category_filters = []
    if len(category_params) > 0:
        placeholders = "?"
        for i in range(1, len(category_params)):
            placeholders = placeholders + ", ?"
        category_filters = ["cat.name IN (" + placeholders + ")"]

    # Filter kleur (color in database)
    color_params = kleur
    color_filters = []
    if len(color_params) > 0:
        placeholders = "?"
        for i in range(1, len(color_params)):
            placeholders = placeholders + ", ?"
        color_filters = ["col.name IN (" + placeholders + ")"]

    # Add WHERE with filters to query
    params = category_params + color_params
    filters = category_filters + color_filters
    if len(filters) > 0:
        query = query + " WHERE " + filters[0]
        for i in range(1, len(filters)):
            query = query + " AND " + filters[i]

    # Add GROUP BY to ensure each product appears only once
    query = query + " GROUP BY prod.id"

    # Execute the query
    print("API: Query submitted:", query)
    print("API: Query parameters:", params)
    product_rows = db_connection.execute(query, params).fetchall()
    print("API: Query result (first 3 rows):", product_rows[:3])

    # Add values for n:m property (e.g., colors) to products
    for product in product_rows:
        # Fetch colors for the product
        color_query = """
            SELECT col.name
            FROM colors col
            JOIN product_colors prodcol ON col.id = prodcol.color_id
            WHERE prodcol.product_id = ?
        """
        param_product_id = product["id"]
        # Execute the query to fetch colors for the current product
        print("API: Query submitted:", color_query)
        color_rows = db_connection.execute(color_query, (param_product_id,)).fetchall()
        print("API: Query result (first 3 rows):", color_rows[:3])

        # Add fetched colors to product
        colors = []
        for row in color_rows:
            colors.append(row["name"])
        product["kleur"] = colors

    db_connection.close()
    print("API: Finished /api/products endpoint") 
    return {"products": product_rows}

# API endpoint to get all properties and values for filters
@app.get("/api/filters")
def get_filters():
    print("API: Starting /api/filters endpoint")  

    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert each row into a dictionary

    # Fetch all distinct categories
    categories_query = "SELECT name FROM categories"
    print("API: Query submitted:", categories_query)  
    categories_result = db_connection.execute(categories_query).fetchall()
    print("API: Query result (first 3 rows):", categories_result[:3])  
    categories = [row["name"] for row in categories_result]

    # Fetch all distinct colors
    colors_query = "SELECT name FROM colors"
    print("API: Query submitted:", colors_query)  
    colors_result = db_connection.execute(colors_query).fetchall()
    print("API: Query result (first 3 rows):", colors_result[:3])  
    colors = [row["name"] for row in colors_result]

    # Construct the response
    filters = {
        "soort": categories,
        "kleur": colors
    }

    db_connection.close()
    print("API: Finished /api/filters endpoint")  
    return {"filters": filters}

#
# Serve static files like index.html, script.js, etc.
#

# Do not cache static files, handy for development
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
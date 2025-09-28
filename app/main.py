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
    print("API: Starting /api/products endpoint")
    print("API: Parameters - merk:", merk, ", kleur:", kleur)
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert each row into a dictionary

    # Build the base query
    query = """
        SELECT 
            products.id, 
            products.name, 
            products.beschrijving, 
            products.image_link,
            products.price, 
            brands.name AS merk
        FROM products
        LEFT JOIN brands ON products.brand_id = brands.id
        LEFT JOIN product_color ON products.id = product_color.product_id
        LEFT JOIN colors ON product_color.color_id = colors.id
    """
    # startcode
    # query = """
    #     SELECT *
    #     FROM products
    # """


    # Filter merk (brand in database)
    brand_params = merk
    brand_filters = []
    if len(brand_params) > 0:
        placeholders = "?"
        for i in range(1, len(brand_params)):
            placeholders = placeholders + ", ?"
        brand_filters = ["brands.name IN (" + placeholders + ")"]

    # Filter kleur (color in database)
    color_params = kleur
    color_filters = []
    if len(color_params) > 0:
        placeholders = "?"
        for i in range(1, len(color_params)):
            placeholders = placeholders + ", ?"
        color_filters = ["colors.name IN (" + placeholders + ")"]

    # Add WHERE with filters to query
    params = brand_params + color_params
    filters = brand_filters + color_filters
    if len(filters) > 0:
        query = query + " WHERE " + filters[0]
        for i in range(1, len(filters)):
            query = query + " AND " + filters[i]

    # Add GROUP BY to ensure each product appears only once
    query = query + " GROUP BY products.id"

    # Execute the query
    print("API: Query submitted:", query)
    print("API: Query parameters:", params)
    product_rows = db_connection.execute(query, params).fetchall()
    print("API: Query result (first 3 rows):", product_rows[:3])

    # Add values for n:m property (e.g., colors) to products
    for product in product_rows:
        # Fetch colors for the product
        color_query = """
            SELECT colors.name
            FROM colors
            JOIN product_color ON colors.id = product_color.color_id
            WHERE product_color.product_id = ?
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

    # Fetch all distinct brands
    brands_query = "SELECT name FROM brands"
    print("API: Query submitted:", brands_query)  
    brands_result = db_connection.execute(brands_query).fetchall()
    print("API: Query result (first 3 rows):", brands_result[:3])  
    brands = [row["name"] for row in brands_result]

    # Fetch all distinct colors
    colors_query = "SELECT name FROM colors"
    print("API: Query submitted:", colors_query)  
    colors_result = db_connection.execute(colors_query).fetchall()
    print("API: Query result (first 3 rows):", colors_result[:3])  
    colors = [row["name"] for row in colors_result]

    # Construct the response
    filters = {
        "merk": brands,
        "kleur": colors
    }

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
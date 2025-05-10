# This is a simple FastAPI application that serves a static HTML site and provides API endpoints:

# source for base code https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
# extended using copilot

import sqlite3
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Function to convert rows into dictionaries
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# API endpoint to get a list of products
@app.get("/api/products")
def get_products(
    merk: list[str] = Query(default=[]),
    kleur: list[str] = Query(default=[])
):
    print("DEBUG: Starting /api/products endpoint")
    print("DEBUG: Parameters - merk:", merk, ", kleur:", kleur)
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert rows into dictionaries

    # Build the base query
    query = """
        SELECT 
            p.id, 
            p.name, 
            p.image_link,
            p.price, 
            b.name AS merk
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN product_colors pc ON p.id = pc.product_id
        LEFT JOIN colors c ON pc.color_id = c.id
    """
    filters = []
    params = []

    # Add filter for brands
    if merk:
        placeholders = ", ".join(["?"] * len(merk))
        filters.append("b.name IN (" + placeholders + ")")
        params.extend(merk)

    # Add filter for colors
    if kleur:
        placeholders = ", ".join(["?"] * len(kleur))
        filters.append("c.name IN (" + placeholders + ")")
        params.extend(kleur)

    # Append WHERE clause if there are filters
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Add GROUP BY to ensure each product appears only once
    query += " GROUP BY p.id"

    # Execute the query
    print("DEBUG: Query submitted:", query)
    print("DEBUG: Query parameters:", params)
    product_rows = db_connection.execute(query, params).fetchall()
    print("DEBUG: Query result (first 5 rows):", product_rows[:5])

    # Add values for n:m property (e.g., colors)
    result = []
    for product in product_rows:
        product_id = product["id"]

        # Fetch colors for the product
        color_query = """
            SELECT c.name
            FROM colors c
            JOIN product_colors pc ON c.id = pc.color_id
            WHERE pc.product_id = ?
        """
        # Execute the query to fetch colors for the current product
        print("DEBUG: Query submitted:", color_query)
        color_rows = db_connection.execute(color_query, (product_id,)).fetchall()
        print("DEBUG: Query result (first 5 rows):", color_rows[:5])

        # Add fetched colors to product
        colors = []
        for row in color_rows:
            colors.append(row["name"])
        product["kleur"] = colors
        result.append(product)

    db_connection.close()
    print("DEBUG: Finished /api/products endpoint") 
    return {"products": result}

# API endpoint to get all properties and values for filters
@app.get("/api/filters")
def get_filters():
    print("DEBUG: Starting /api/filters endpoint")  

    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Use dict_factory for query results

    # Fetch all distinct brands
    brands_query = "SELECT name FROM brands"
    print("DEBUG: Query submitted:", brands_query)  
    brands_result = db_connection.execute(brands_query).fetchall()
    print("DEBUG: Query result (first 5 rows):", brands_result[:5])  
    brands = [row["name"] for row in brands_result]

    # Fetch all distinct colors
    colors_query = "SELECT name FROM colors"
    print("DEBUG: Query submitted:", colors_query)  
    colors_result = db_connection.execute(colors_query).fetchall()
    print("DEBUG: Query result (first 5 rows):", colors_result[:5])  
    colors = [row["name"] for row in colors_result]

    # Construct the response
    filters = {
        "merk": brands,
        "kleur": colors
    }

    db_connection.close()
    print("DEBUG: Finished /api/filters endpoint")  
    return {"filters": filters}


# Serve static files like index.html, script.js, etc.

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

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
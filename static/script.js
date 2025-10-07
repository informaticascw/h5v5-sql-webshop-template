// Load filters dynamically from /api/filters
async function loadFilters() {
  try {
    const response = await fetch('/api/filters');
    const data = await response.json();
    const productFilters = document.getElementById('product-filters');

    // Generate filter HTML using innerHTML
    let filtersHTML = '';

    // Iterate over all filter properties returned by the API
    var filterKeys = Object.keys(data.filters);
    for (var i = 0; i < filterKeys.length; i++) {
      var filterKey = filterKeys[i];           // e.g. "color"
      var filterValues = data.filters[filterKey]; // e.g. ["red", "green"]

      // Create a section for each filter
      filtersHTML += `<div class="filter-container">`;
      filtersHTML += `<h3>${filterKey.charAt(0).toUpperCase() + filterKey.slice(1)}</h3>`;

      // Add checkboxes for each filter option
      for (var j = 0; j < filterValues.length; j++) {
        const filterValue = filterValues[j];
        const checkboxId = `filter-${filterKey}-${filterValue}`;
        filtersHTML += `
            <input type="checkbox" id="${checkboxId}" value="${filterValue}">
            <label for="${checkboxId}">${filterValue}</label><br>
          `;
      }
      filtersHTML += `</div>`;
    }
    // Set the generated HTML to the productFilters container
    productFilters.innerHTML = filtersHTML;

    // Hide filter section when there are no filters
    if (Object.entries(data.filters).length === 0) {
      document.getElementById('filter-section').style.display = 'none';
    }

  } catch (error) {
    console.error('Error loading filters:', error);
    const productFilters = document.getElementById('product-filters');
    productFilters.innerHTML = '<p class="error">Failed to load filters.</p>';
  }

}

// Apply filters and reload products
async function loadFilteredProducts() {
  try {
    const queryParams = new URLSearchParams();

    // Get all filter inputs
    const filterInputs = document.querySelectorAll('#product-filters input');
    for (var i = 0; i < filterInputs.length; i++) {
      var input = filterInputs[i];
      if (input.type === 'checkbox' && input.checked) {
        // Add checkbox filters (e.g., brands, colors)
        var key = input.id.replace('filter-', '').split('-')[0];
        queryParams.append(key, input.value);
      }
    }

    // Load products with applied filters
    console.log('DEBUG: Applied filters:', queryParams.toString());
    const response = await fetch(`/api/products?${queryParams.toString()}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    // Generate product grid HTML
    const grid = document.getElementById('product-grid');
    let gridHTML = '';

    // For each product, create a tile with its details
    for (var product of data.products) {
      var content = '<article class="product-tile">';

      // Display product name
      content += '<h2>' + (product.name || 'Product') + '</h2>';

      // Display product image
      var imgUrl = '/images/' + encodeURIComponent(product.image_link || 'noimage.png');
      content += '<img src="' + imgUrl + '" alt="' + (product.name || 'noname') + '">';

      // For each product property, create a label and value
      for (var key in product) {
        if (['name', 'image_link', 'id', 'price', 'dummy'].includes(key)) continue; // Skip name, image_link, id, price and dummy

        // Format the label (e.g., 'product_name' -> 'Product Name')
        var label = key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ');

        // Check if the value is an array
        if (Array.isArray(product[key])) {
          // Display label with a list of values
          content += '<p><strong>' + label + ':</strong></p><ul>';
          for (var value of product[key]) {
            content += '<li>' + value + '</li>';
          }
          content += '</ul>';
        } else {
          // Display label with a single value
          content += '<p><strong>' + label + ':</strong> ' + product[key] + '</p>';
        }
      }
      // Display product price
      if (product.price) {
        content += '<p><strong>Prijs:</strong> € ' + product.price.toFixed(2) + '</p>';
      }
      content += '</article>';
      gridHTML += content;
    }

    // Set the generated HTML to the product grid
    grid.innerHTML = gridHTML;
  } catch (error) {
    console.error('Error loading products:', error);
    const grid = document.getElementById('product-grid');
    grid.innerHTML = '<p class="error">Failed to load products.</p>';
  }
}
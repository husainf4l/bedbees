# Test URLs for Tunisia Attractions

## Visit these URLs to test the new attraction pages:

### Working Pages (should show full detail):

1. http://localhost:8000/countries/tunisia/attraction/sidi-bou-said/
2. http://localhost:8000/countries/tunisia/attraction/el-jem-amphitheater/
3. http://localhost:8000/countries/tunisia/attraction/kairouan/
4. http://localhost:8000/countries/tunisia/attraction/matmata/

### Newly Added Pages (should now work):

5. http://localhost:8000/countries/tunisia/attraction/carthage-archaeological-site/
6. http://localhost:8000/countries/tunisia/attraction/dougga-ancient-city/
7. http://localhost:8000/countries/tunisia/attraction/tunis-medina/
8. http://localhost:8000/countries/tunisia/attraction/bardo-museum/
9. http://localhost:8000/countries/tunisia/attraction/djerba-island/
10. http://localhost:8000/countries/tunisia/attraction/sahara-desert/
11. http://localhost:8000/countries/tunisia/attraction/sousse-medina/
12. http://localhost:8000/countries/tunisia/attraction/hammamet/
13. http://localhost:8000/countries/tunisia/attraction/tozeur/

## How to Test:

1. Make sure Django server is running at http://localhost:8000/
2. Click on each URL above
3. Each should show a full attraction detail page with:
   - Hero image
   - Detailed description
   - Historical significance
   - Visitor information
   - Facts and tips
   - Photo gallery
   - Practical details

## If Redirects Occur:

If any URL redirects back to the country page, the slug might not match exactly. Check that:

- The slug in the URL matches the key in demo_attractions dictionary
- The slug matches what's listed in the country's attractions array

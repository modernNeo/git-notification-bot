import json


def log_request_data(request):
    """Helper method to print incoming request details."""
    print(f"\n--- Incoming {request.method} Request ---")
    print("Path:", request.path)
    print("Query Params (GET):", dict(request.GET))
    print("Headers:", dict(request.headers))

    # Read JSON body for POST/PATCH if content-type is JSON
    if request.content_type == "application/json":
        try:
            print("Body (JSON):", json.loads(request.body))
        except json.JSONDecodeError:
            print("Body (Invalid JSON):", request.body)
    else:
        print("Form Data (POST):", dict(request.POST))

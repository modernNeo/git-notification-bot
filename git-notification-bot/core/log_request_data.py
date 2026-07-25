import json


def log_request_data(request):
    """Helper method to print incoming request details."""
    print(f"\n--- Incoming {request.method} Request ---")
    print("Path:", request.path)
    print("Query Params (GET):", dict(request.GET))
    headers = json.dumps(dict(request.headers), indent=4)
    print("Headers:", headers)

    # Read JSON body for POST/PATCH/PUT
    if request.content_type == "application/json":
        try:
            # request.body is bytes, decode it to string first, then load JSON
            body_data = json.loads(request.body.decode('utf-8'))
            print("Body (JSON):", json.dumps(body_data, indent=4))
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("Body (Invalid JSON):", request.body)

    elif request.content_type == "application/x-www-form-urlencoded":
        # request.POST is a QueryDict; convert it to a standard dict for pretty printing
        print("Body (Form URL-Encoded):", json.dumps(request.POST, indent=4))

        payload_data = json.loads(request.POST['payload'])
        print("Body Payload (Form URL-Encoded):", json.dumps(payload_data, indent=4))

    else:
        # Fallback for other data types (like multipart/form-data file uploads)
        print("Form Data (POST):", dict(request.POST))
        if request.FILES:
            print("Files:", {k: v.name for k, v in request.FILES.items()})

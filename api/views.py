import requests
from django.http import JsonResponse
from datetime import datetime, timezone

def classify_name(request):
    name = request.GET.get('name')

    # 400: missing name
    if not name:
        return JsonResponse({
            "status": "error",
            "message": "Name parameter is required"
        }, status=400)

    try:
        response = requests.get(f"https://api.genderize.io/?name={name}")

        if response.status_code != 200:
            return JsonResponse({
                "status": "error",
                "message": "Upstream API failure"
            }, status=502)

        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # ✅ FIXED CONDITION (IMPORTANT)
        if gender is None or count is None or count == 0:
            return JsonResponse({
                "status": "error",
                "message": "No prediction available for the provided name"
            }, status=422)

        probability = float(probability)

        is_confident = probability >= 0.7 and count >= 100

        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return JsonResponse({
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": count,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }, status=200)

    except Exception:
        return JsonResponse({
            "status": "error",
            "message": "Server error"
        }, status=500)
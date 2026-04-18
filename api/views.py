from datetime import datetime, timezone

def classify_name(request):
    name = request.GET.get('name')

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

        if gender is None or count == 0:
            return JsonResponse({
                "status": "error",
                "message": "No prediction available"
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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from .models import Profile


def serialize_profile(profile):
    return {
        "id": str(profile.id),
        "name": profile.name,
        "gender": profile.gender,
        "gender_probability": profile.gender_probability,
        "sample_size": profile.sample_size,
        "age": profile.age,
        "age_group": profile.age_group,
        "country_id": profile.country_id,
        "country_probability": profile.country_probability,
        "created_at": profile.created_at.isoformat().replace("+00:00", "Z")
    }


@csrf_exempt
@require_http_methods(["POST"])
def create_profile(request):
    try:
        body = json.loads(request.body)
        name = body.get("name")

        if not name:
            return JsonResponse({"status": "error", "message": "Name is required"}, status=400)

        if not isinstance(name, str):
            return JsonResponse({"status": "error", "message": "Name must be a string"}, status=422)

        name = name.lower()

        existing = Profile.objects.filter(name=name).first()
        if existing:
            return JsonResponse({
                "status": "success",
                "message": "Profile already exists",
                "data": serialize_profile(existing)
            }, status=200)

        # API calls
        g = requests.get(f"https://api.genderize.io?name={name}").json()
        a = requests.get(f"https://api.agify.io?name={name}").json()
        n = requests.get(f"https://api.nationalize.io?name={name}").json()

        if g.get("gender") is None or g.get("count") == 0:
            return JsonResponse({"status": "error", "message": "Genderize returned an invalid response"}, status=502)

        if a.get("age") is None:
            return JsonResponse({"status": "error", "message": "Agify returned an invalid response"}, status=502)

        if not n.get("country"):
            return JsonResponse({"status": "error", "message": "Nationalize returned an invalid response"}, status=502)

        age = a["age"]

        if age <= 12:
            age_group = "child"
        elif age <= 19:
            age_group = "teenager"
        elif age <= 59:
            age_group = "adult"
        else:
            age_group = "senior"

        top_country = max(n["country"], key=lambda x: x["probability"])

        profile = Profile.objects.create(
            name=name,
            gender=g["gender"],
            gender_probability=g["probability"],
            sample_size=g["count"],
            age=age,
            age_group=age_group,
            country_id=top_country["country_id"],
            country_probability=top_country["probability"]
        )

        return JsonResponse({"status": "success", "data": serialize_profile(profile)}, status=201)

    except Exception:
        return JsonResponse({"status": "error", "message": "Server error"}, status=500)


@require_http_methods(["GET"])
def get_all_profiles(request):
    try:
        profiles = Profile.objects.all()

        gender = request.GET.get("gender")
        country_id = request.GET.get("country_id")
        age_group = request.GET.get("age_group")

        if gender:
            profiles = profiles.filter(gender__iexact=gender)

        if country_id:
            profiles = profiles.filter(country_id__iexact=country_id)

        if age_group:
            profiles = profiles.filter(age_group__iexact=age_group)

        data = [
            {
                "id": str(p.id),
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "age_group": p.age_group,
                "country_id": p.country_id
            }
            for p in profiles
        ]

        return JsonResponse({
            "status": "success",
            "count": len(data),
            "data": data
        }, status=200)

    except Exception:
        return JsonResponse({"status": "error", "message": "Server error"}, status=500)


@require_http_methods(["GET"])
def get_profile(request, id):
    profile = Profile.objects.filter(id=id).first()

    if not profile:
        return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)

    return JsonResponse({"status": "success", "data": serialize_profile(profile)}, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_profile(request, id):
    profile = Profile.objects.filter(id=id).first()

    if not profile:
        return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)

    profile.delete()
    return JsonResponse({}, status=204)
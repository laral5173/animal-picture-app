"""
Service responsible for fetching random animal pictures from external APIs
and saving them to disk.
"""
import httpx
import os
import uuid

# External APIs used to fetch random animal pictures.
# Each returns an image directly (not JSON), so we just download the bytes.
ANIMAL_APIS = {
    "cat": "https://cataas.com/cat",
    "dog": "https://place.dog/{width}/{height}",
    "bear": "https://placebear.com/{width}/{height}",
}

IMAGES_DIR = "./app/images"


class UnsupportedAnimalError(Exception):
    """Raised when the requested animal type is not one we support."""
    pass


async def fetch_animal_image(animal_type: str) -> tuple[str, str]:
    """
    Fetch a single random image for the given animal type.

    Returns:
        (source_url, local_file_path)
    """
    animal_type = animal_type.lower().strip()
    if animal_type not in ANIMAL_APIS:
        raise UnsupportedAnimalError(
            f"'{animal_type}' is not supported. Choose from: {list(ANIMAL_APIS.keys())}"
        )

    # Fixed size for all images. Some APIs (place.dog, placebear) accept
    # width/height in the URL; cataas.com ignores them and returns its own.
    width, height = 300, 300
    url = ANIMAL_APIS[animal_type].format(width=width, height=height)

    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "image/jpeg")
        extension = "png" if "png" in content_type else "jpg"

        os.makedirs(IMAGES_DIR, exist_ok=True)
        filename = f"{animal_type}_{uuid.uuid4().hex[:8]}.{extension}"
        file_path = os.path.join(IMAGES_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)

    return str(response.url), file_path


async def fetch_multiple_animal_images(animal_type: str, count: int) -> list[tuple[str, str]]:
    """Fetch `count` images sequentially for the given animal type."""
    results = []
    for _ in range(count):
        result = await fetch_animal_image(animal_type)
        results.append(result)
    return results

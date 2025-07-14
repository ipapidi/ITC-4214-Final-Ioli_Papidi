from products.models import Category
from django.core.files import File
from pathlib import Path

media_root = Path("media/categories")

for category in Category.objects.all():
    filename = f"{category.name}.png"
    filepath = media_root / filename

    if filepath.exists():
        with filepath.open("rb") as f:
            # Overwrite existing file and keep clean name
            category.icon_class.delete(save=False)  # Remove old
            category.icon_class.save(filename, File(f), save=True)
            print(f"✅ Set icon for: {category.name}")
    else:
        print(f"⚠️ Not found: {filename}")
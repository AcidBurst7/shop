import time
import random
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

import requests
from fake_useragent import UserAgent

from io import BytesIO
from transliterate import translit

from shop.models import Category, Product
from orders.models import Order, OrderItem


ua = UserAgent(browsers=['Edge', 'Chrome'])

CATEGORIES = [ 
    'Наклейки', 
    'Футболки', 
    'Значки', 
    'Плакаты', 
    'Кружки', 
]

CATEGORY_PROMPTS = {
    "Наклейки": "retro sci-fi sticker pack",
    "Футболки": "black t-shirt mockup cyberpunk",
    "Значки": "enamel pin product photography",
    "Плакаты": "dark sci-fi poster art",
    "Кружки": "coffee mug product photography",
}

PRODUCTS = {
    "Наклейки": [
        "Trust No One Sticker",
        "Alien Signal Pack",
        "Retro UFO Vinyl",
        "Mystery Archive Set",
        "Glitch Signal Sticker",
    ],
    "Футболки": [
        "Area 51 T-Shirt",
        "The Truth Tee",
        "Midnight Broadcast",
        "Paranormal Dept",
        "Signal Lost Shirt",
    ],
    "Значки": [
        "UFO Enamel Pin",
        "Ghost File Badge",
        "Strange Signal Pin",
        "Neon Eye Badge",
        "Agent Unknown Pin",
    ],
    "Плакаты": [
        "Night Sky Poster",
        "Unknown Contact Print",
        "Cyber Mystery Wall Art",
        "Lost Transmission Poster",
        "Dark Forest Signal",
    ],
    "Кружки": [
        "Trust No One Mug",
        "Late Night Debug Mug",
        "Alien Coffee Cup",
        "Signal Hunter Mug",
        "Black Terminal Cup",
    ],
}

DESCRIPTIONS = [
    "Лимитированный дизайн для любителей мистики, технологий и ретро-эстетики.",
    "Авторский принт с атмосферой загадочных архивов и ночных расследований.",
    "Идеально для тех, кто любит странные сигналы, космос и техно-нуар.",
    "Минималистичный дизайн с лёгким sci-fi настроением.",
    "Стильный аксессуар для коллекции или повседневного использования.",
]

def generate_image(prompt: str) -> ContentFile:
    try:
        headers = {"User-Agent": ua.random}
        url = f"https://image.pollinations.ai/prompt/{prompt}"

        response = requests.get(
            url,
            timeout=60,
            headers=headers
        )
        response.raise_for_status()

        return ContentFile(
            response.content,
            name=f"{slugify(prompt)[:50]}.png",
        )
    finally:
        time.sleep(30)

    

class Command(BaseCommand):
    help = "Заполняет магазин тестовыми товарами"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Удаляем старые данные...'))

        Product.objects.all().delete()
        Category.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()

        self.stdout.write(self.style.WARNING('Удалены категории, продукты, заказы.'))
        self.stdout.write(self.style.WARNING('Создаем категории...'))

        for category_name in CATEGORIES:
            category_slug = translit(slugify(category_name, allow_unicode=True), reversed=True)
            category = Category.objects.create(
                name=category_name,
                slug=category_slug
            )

            for idx, product_name in enumerate(PRODUCTS[category_name], start=1):
                prompt = (
                    f"{CATEGORY_PROMPTS[category_name]}, "
                    f"{product_name}, "
                    f"mysterious alien conspiracy style, "
                    f"studio lighting, "
                    f"ultra detailed, "
                    f"product photo"
                )
                
                product = Product.objects.create(
                    category=category,
                    name=product_name,
                    slug=f"{slugify(product_name)}-{idx}",
                    description=random.choice(DESCRIPTIONS),
                    price=Decimal(random.randrange(500, 4500)),
                )

                try:
                    image = generate_image(prompt)
                    product.image.save(
                        image.name,
                        image,
                        save=True
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Изображение создано для {product.name}"
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"✗ Ошибка генерации изображения "
                            f"для {product.name}: {e}"
                        )
                    )
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))
    
        
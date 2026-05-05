TOOLS = [
    {
        "slug": "pressure_converter",
        "name": "BAR ↔ PSI",
        "title": "Конвертер давления BAR ↔ PSI",
        "url": "/pressure_converter",
        "category": "Авто и техника",
        "description": "Быстрый перевод давления для шин, компрессоров и оборудования.",
        "icon": "BAR",
        "featured": True,
        "nav": True,
        "priority": 10,
        "related": ["fuel_calculator", "converter", "calculator"],
    },
    {
        "slug": "calculator",
        "name": "Калькулятор",
        "title": "Калькулятор онлайн",
        "url": "/calculator",
        "category": "Расчеты",
        "description": "Обычные вычисления, проценты, степени и корни.",
        "icon": "123",
        "featured": True,
        "nav": True,
        "priority": 20,
        "related": ["converter", "currency", "pressure_converter"],
    },
    {
        "slug": "currency",
        "name": "Конвертер валют",
        "title": "Конвертер валют",
        "url": "/currency",
        "category": "Деньги",
        "description": "Перевод популярных валют с курсами ЦБ РФ и локальной историей.",
        "icon": "RUB",
        "featured": True,
        "nav": True,
        "priority": 30,
        "related": ["fuel_calculator", "calculator", "converter"],
    },
    {
        "slug": "fuel_calculator",
        "name": "Калькулятор бензина",
        "title": "Калькулятор бензина",
        "url": "/fuel-calculator",
        "category": "Авто и техника",
        "description": "Стоимость поездки по расстоянию, расходу, цене топлива и валюте.",
        "icon": "L",
        "featured": False,
        "nav": True,
        "priority": 40,
        "related": ["pressure_converter", "currency", "calculator"],
    },
    {
        "slug": "converter",
        "name": "Конвертер величин",
        "title": "Конвертер величин",
        "url": "/converter",
        "category": "Конвертация",
        "description": "Длина, вес, объем и скорость в одном простом конвертере.",
        "icon": "↔",
        "featured": False,
        "nav": True,
        "priority": 50,
        "related": ["pressure_converter", "currency", "calculator"],
    },
    {
        "slug": "timer",
        "name": "Таймер",
        "title": "Таймер онлайн",
        "url": "/timer",
        "category": "Время",
        "description": "Таймер и секундомер для повседневных задач.",
        "icon": "00",
        "featured": False,
        "nav": True,
        "priority": 60,
        "related": ["calculator", "qr_code", "converter"],
    },
    {
        "slug": "qr_code",
        "name": "QR-код",
        "title": "Создать QR-код онлайн",
        "url": "/qr-code",
        "category": "Текст и ссылки",
        "description": "Создание и скачивание QR-кода для текста или ссылки.",
        "icon": "QR",
        "featured": False,
        "nav": True,
        "priority": 70,
        "related": ["timer", "calculator", "currency"],
    },
    {
        "slug": "weather",
        "name": "Погода",
        "title": "Погода онлайн",
        "url": "/weather",
        "category": "Справка",
        "description": "Проверка погоды по городу, если настроен API-ключ.",
        "icon": "°C",
        "featured": False,
        "nav": True,
        "priority": 80,
        "related": ["timer", "currency", "calculator"],
    },
]


def get_tools():
    return sorted(TOOLS, key=lambda tool: tool["priority"])


def get_featured_tools():
    return [tool for tool in get_tools() if tool.get("featured")]


def get_tools_by_category():
    groups = []
    for tool in get_tools():
        category = tool["category"]
        group = next((item for item in groups if item["name"] == category), None)
        if group is None:
            group = {"name": category, "tools": []}
            groups.append(group)
        group["tools"].append(tool)
    return groups


def get_nav_tools():
    return [tool for tool in get_tools() if tool.get("nav")]


def get_tool_by_slug(slug):
    return next((tool for tool in TOOLS if tool["slug"] == slug), None)


def get_tool_by_path(path):
    return next((tool for tool in TOOLS if tool["url"] == path), None)


def get_related_tools(slug, limit=3):
    tool = get_tool_by_slug(slug)
    if not tool:
        return []

    related = []
    for related_slug in tool.get("related", []):
        related_tool = get_tool_by_slug(related_slug)
        if related_tool:
            related.append(related_tool)

    if len(related) < limit:
        for candidate in get_tools():
            if candidate["slug"] == slug or candidate in related:
                continue
            if candidate["category"] == tool["category"] or candidate.get("featured"):
                related.append(candidate)
            if len(related) >= limit:
                break

    return related[:limit]

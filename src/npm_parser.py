"""Разбор прямых зависимостей из package.json."""

DEPENDENCY_SECTIONS = (
    "dependencies",
    "devDependencies",
    "peerDependencies",
    "optionalDependencies",
)


def extract_direct_dependencies(package_json: dict) -> list[str]:
    """Возвращает отсортированный список прямых зависимостей."""
    names: set[str] = set()
    for section in DEPENDENCY_SECTIONS:
        values = package_json.get(section) or {}
        if not isinstance(values, dict):
            continue
        names.update(values.keys())
    return sorted(names)


def extract_package_name(package_json: dict) -> str:
    """Возвращает имя пакета из package.json."""
    name = package_json.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("В package.json отсутствует поле 'name'.")
    return name.strip()
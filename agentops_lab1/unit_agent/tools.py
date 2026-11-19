# tools.py -- the agent's single tool: a unit converter
from langchain_core.tools import tool

# How many metres / kilograms ONE of each unit equals
LENGTH = {
    "km": 1000.0, "m": 1.0, "cm": 0.01,
    "mile": 1609.344, "ft": 0.3048, "inch": 0.0254,
}
MASS = {"kg": 1.0, "g": 0.001, "lb": 0.45359237, "oz": 0.028349523125}

# Plural and long-form names the model might use
ALIASES = {
    "kilometer": "km", "kilometers": "km", "meter": "m", "meters": "m",
    "centimeter": "cm", "centimeters": "cm", "miles": "mile", "feet": "ft",
    "foot": "ft", "inches": "inch", "kilogram": "kg", "kilograms": "kg",
    "gram": "g", "grams": "g", "pound": "lb", "pounds": "lb", "lbs": "lb",
    "ounce": "oz", "ounces": "oz", "celsius": "c", "fahrenheit": "f",
}

def _norm(unit: str) -> str:
    unit = unit.strip().lower()
    return ALIASES.get(unit, unit)

@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a number from one unit to another.
    Supported units: km, m, cm, mile, ft, inch (length);
    kg, g, lb, oz (mass); c, f (temperature)."""
    a, b = _norm(from_unit), _norm(to_unit)
    for table in (LENGTH, MASS):
        if a in table and b in table:
            result = value * table[a] / table[b]
            return f"{value} {a} = {round(result, 4)} {b}"
    if (a, b) == ("c", "f"):
        return f"{value} c = {round(value * 9 / 5 + 32, 4)} f"
    if (a, b) == ("f", "c"):
        return f"{value} f = {round((value - 32) * 5 / 9, 4)} c"
    return (
        f"Cannot convert from '{from_unit}' to '{to_unit}'. "
        "Check the units are supported and of the same kind."
    )

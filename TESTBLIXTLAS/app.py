from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ============================================================
#  RECIPES
# ============================================================

RECIPES = [
    {
        "id": 1,
        "title": "Stekt ris med kyckling",
        "required_ingredients": [
            {"name": "ris", "amount": 200, "unit": "g"},
            {"name": "kyckling", "amount": 200, "unit": "g"},
            {"name": "ägg", "amount": 2, "unit": "st"}
        ],
        "optional_ingredients": [
            {"name": "soja", "amount": 1, "unit": "msk"},
            {"name": "morot", "amount": 1, "unit": "st"},
            {"name": "lök", "amount": 0.5, "unit": "st"}
        ],
        "instructions": [
            "Skär kycklingen i bitar och stek tills den är genomstekt.",
            "Tillsätt hackad lök och morot, fräs i några minuter.",
            "Knäck i ägg och rör om.",
            "Blanda i ris och soja, stek tills allt är varmt."
        ],
        "step_ingredients": [
            [{"name": "kyckling", "amount": 200, "unit": "g"}],
            [{"name": "lök", "amount": 0.5, "unit": "st"}, {"name": "morot", "amount": 1, "unit": "st"}],
            [{"name": "ägg", "amount": 2, "unit": "st"}],
            [{"name": "ris", "amount": 200, "unit": "g"}, {"name": "soja", "amount": 1, "unit": "msk"}]
        ]
    },
    {
        "id": 2,
        "title": "Tomat- och linsgryta",
        "required_ingredients": [
            {"name": "linser", "amount": 2, "unit": "dl"},
            {"name": "tomat", "amount": 400, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "lök", "amount": 1, "unit": "st"},
            {"name": "vitlök", "amount": 2, "unit": "klyfta"},
            {"name": "spiskummin", "amount": 1, "unit": "tsk"}
        ],
        "instructions": [
            "Fräs lök och vitlök i lite olja.",
            "Tillsätt tomat och kryddor.",
            "Häll i linser och vatten, låt koka tills linserna är mjuka."
        ],
        "step_ingredients": [
            [{"name": "lök", "amount": 1, "unit": "st"}, {"name": "vitlök", "amount": 2, "unit": "klyfta"}],
            [{"name": "tomat", "amount": 400, "unit": "g"}, {"name": "spiskummin", "amount": 1, "unit": "tsk"}],
            [{"name": "linser", "amount": 2, "unit": "dl"}]
        ]
    },
    {
        "id": 3,
        "title": "Pasta med ostsås",
        "required_ingredients": [
            {"name": "pasta", "amount": 200, "unit": "g"},
            {"name": "ost", "amount": 100, "unit": "g"},
            {"name": "mjölk", "amount": 2, "unit": "dl"}
        ],
        "optional_ingredients": [
            {"name": "smör", "amount": 10, "unit": "g"},
            {"name": "peppar", "amount": 1, "unit": "tsk"},
            {"name": "salt", "amount": 1, "unit": "tsk"}
        ],
        "instructions": [
            "Koka pastan enligt anvisningarna.",
            "Smält smör i en kastrull, tillsätt mjölk och ost.",
            "Rör tills osten har smält.",
            "Blanda med pastan och krydda."
        ],
        "step_ingredients": [
            [{"name": "pasta", "amount": 200, "unit": "g"}],
            [{"name": "smör", "amount": 10, "unit": "g"}, {"name": "mjölk", "amount": 2, "unit": "dl"}, {"name": "ost", "amount": 100, "unit": "g"}],
            [],
            []
        ]
    },
    {
        "id": 4,
        "title": "Grönsakssoppa",
        "required_ingredients": [
            {"name": "potatis", "amount": 3, "unit": "st"},
            {"name": "morot", "amount": 2, "unit": "st"},
            {"name": "vatten", "amount": 1, "unit": "l"}
        ],
        "optional_ingredients": [
            {"name": "selleri", "amount": 1, "unit": "st"},
            {"name": "buljong", "amount": 1, "unit": "tärning"},
            {"name": "persilja", "amount": 1, "unit": "msk"}
        ],
        "instructions": [
            "Skala och tärna potatis och morot.",
            "Koka i vatten med buljong.",
            "Tillsätt selleri och låt sjuda tills grönsakerna är mjuka.",
            "Servera med hackad persilja."
        ],
        "step_ingredients": [
            [{"name": "potatis", "amount": 3, "unit": "st"}, {"name": "morot", "amount": 2, "unit": "st"}],
            [{"name": "vatten", "amount": 1, "unit": "l"}, {"name": "buljong", "amount": 1, "unit": "tärning"}],
            [{"name": "selleri", "amount": 1, "unit": "st"}],
            [{"name": "persilja", "amount": 1, "unit": "msk"}]
        ]
    },
    {
        "id": 5,
        "title": "Kycklingwok",
        "required_ingredients": [
            {"name": "kyckling", "amount": 250, "unit": "g"},
            {"name": "grönsaker", "amount": 300, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "soja", "amount": 1, "unit": "msk"},
            {"name": "nudlar", "amount": 200, "unit": "g"},
            {"name": "vitlök", "amount": 1, "unit": "klyfta"}
        ],
        "instructions": [
            "Stek kycklingen tills den är gyllenbrun.",
            "Tillsätt grönsaker och vitlök, fräs snabbt.",
            "Blanda i soja och kokta nudlar.",
            "Servera genast."
        ],
        "step_ingredients": [
            [{"name": "kyckling", "amount": 250, "unit": "g"}],
            [{"name": "grönsaker", "amount": 300, "unit": "g"}, {"name": "vitlök", "amount": 1, "unit": "klyfta"}],
            [{"name": "soja", "amount": 1, "unit": "msk"}, {"name": "nudlar", "amount": 200, "unit": "g"}],
            []
        ]
    },
    {
        "id": 6,
        "title": "Omelett",
        "required_ingredients": [
            {"name": "ägg", "amount": 3, "unit": "st"}
        ],
        "optional_ingredients": [
            {"name": "ost", "amount": 30, "unit": "g"},
            {"name": "tomat", "amount": 1, "unit": "st"},
            {"name": "skinka", "amount": 50, "unit": "g"}
        ],
        "instructions": [
            "Vispa äggen och krydda.",
            "Häll i en varm panna.",
            "Tillsätt ost, tomat och skinka.",
            "Vik ihop och servera."
        ],
        "step_ingredients": [
            [{"name": "ägg", "amount": 3, "unit": "st"}],
            [],
            [{"name": "ost", "amount": 30, "unit": "g"}, {"name": "tomat", "amount": 1, "unit": "st"}, {"name": "skinka", "amount": 50, "unit": "g"}],
            []
        ]
    },
    {
        "id": 7,
        "title": "Macka med kyckling, avokado och mozzarella",
        "required_ingredients": [
            {"name": "tomat", "amount": 1, "unit": "st"},
            {"name": "avokado", "amount": 1, "unit": "st"},
            {"name": "bröd", "amount": 4, "unit": "skivor"},
            {"name": "skivad kyckling", "amount": 200, "unit": "g"},
            {"name": "mozzarella", "amount": 125, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "basilikapesto", "amount": 4, "unit": "msk"},
            {"name": "skivad inlagd jalapeño", "amount": 2, "unit": "msk"},
            {"name": "tabasco", "amount": 4, "unit": "krm"},
            {"name": "basilikablad", "amount": 15, "unit": "g"},
            {"name": "matolja", "amount": 1, "unit": "msk"}
        ],
        "instructions": [
            "Skiva tomaten.",
            "Gröp ur avokadon och skiva den.",
            "Skiva mozzarellan.",
            "Bred basilikapesto på bröden.",
            "Fördela fyllningen på bröden.",
            "Droppa tabasco och toppa med basilika.",
            "Pensla brödet med olja."
        ],
        "step_ingredients": [
            [{"name": "tomat", "amount": 1, "unit": "st"}],
            [{"name": "avokado", "amount": 1, "unit": "st"}, {"name": "mozzarella", "amount": 125, "unit": "g"}],
            [{"name": "basilikapesto", "amount": 4, "unit": "msk"}, {"name": "tabasco", "amount": 4, "unit": "krm"}],
            [{"name": "basilikablad", "amount": 15, "unit": "g"}, {"name": "matolja", "amount": 1, "unit": "msk"}],
            []
        ]
    },
    {
        "id": 8,
        "title": "Linsgryta med kokosmjölk",
        "required_ingredients": [
            {"name": "ris", "amount": 200, "unit": "g"},
            {"name": "kokosmjölk", "amount": 100, "unit": "ml"},
            {"name": "torkade linser", "amount": 1, "unit": "dl"}
        ],
        "optional_ingredients": [
            {"name": "lök", "amount": 1, "unit": "st"},
            {"name": "olja", "amount": 1, "unit": "msk"},
            {"name": "vitlök", "amount": 1, "unit": "st"},
            {"name": "curry", "amount": 1, "unit": "tsk"},
            {"name": "tomatpuré", "amount": 1, "unit": "msk"},
            {"name": "grönsaksbuljongtärning", "amount": 1, "unit": "st"},
            {"name": "sambal oelek", "amount": 1, "unit": "tsk"},
            {"name": "körsbärstomater", "amount": 65, "unit": "g"},
            {"name": "salt", "amount": 1, "unit": "krm"},
            {"name": "peppar", "amount": 1, "unit": "krm"},
            {"name": "koriander", "amount": 15, "unit": "g"},
            {"name": "matyoghurt", "amount": 1, "unit": "dl"}
        ],
        "instructions": [
            "Koka riset enligt anvisning.",
            "Fräs lök i olja.",
            "Tillsätt vitlök, curry och tomatpuré.",
            "Häll i kokosmjölk, linser och kryddor.",
            "Låt koka tills linserna är mjuka.",
            "Tillsätt tomater och krydda.",
            "Servera med ris och yoghurt."
        ],
        "step_ingredients": [
            [{"name": "ris", "amount": 200, "unit": "g"}],
            [{"name": "lök", "amount": 1, "unit": "st"}, {"name": "olja", "amount": 1, "unit": "msk"}],
            [{"name": "vitlök", "amount": 1, "unit": "st"}, {"name": "curry", "amount": 1, "unit": "tsk"}, {"name": "tomatpuré", "amount": 1, "unit": "msk"}],
            [{"name": "kokosmjölk", "amount": 100, "unit": "ml"}, {"name": "torkade linser", "amount": 1, "unit": "dl"}],
            [{"name": "körsbärstomater", "amount": 65, "unit": "g"}],
            [{"name": "salt", "amount": 1, "unit": "krm"}, {"name": "peppar", "amount": 1, "unit": "krm"}],
            [{"name": "matyoghurt", "amount": 1, "unit": "dl"}]
        ]
    },
    {
        "id": 9,
        "title": "Korvstroganoff med ris",
        "required_ingredients": [
            {"name": "ris", "amount": 200, "unit": "g"},
            {"name": "falukorv", "amount": 140, "unit": "g"},
            {"name": "tomatpuré", "amount": 0.75, "unit": "msk"},
            {"name": "grädde", "amount": 0.5, "unit": "dl"},
            {"name": "matfett", "amount": 1, "unit": "msk"}
        ],
        "optional_ingredients": [
            {"name": "gul lök", "amount": 0.25, "unit": "st"},
            {"name": "mjölk", "amount": 0.25, "unit": "dl"},
            {"name": "senap", "amount": 0.25, "unit": "tsk"}
        ],
        "instructions": [
            "Koka ris.",
            "Stek korv och lök.",
            "Tillsätt tomatpuré.",
            "Rör ner grädde, mjölk och senap.",
            "Låt sjuda."
        ],
        "step_ingredients": [
            [{"name": "ris", "amount": 200, "unit": "g"}],
            [{"name": "falukorv", "amount": 140, "unit": "g"}, {"name": "gul lök", "amount": 0.25, "unit": "st"}],
            [{"name": "tomatpuré", "amount": 0.75, "unit": "msk"}],
            [{"name": "grädde", "amount": 0.5, "unit": "dl"}, {"name": "mjölk", "amount": 0.25, "unit": "dl"}, {"name": "senap", "amount": 0.25, "unit": "tsk"}]
        ]
    },
    {
        "id": 10,
        "title": "Fläskfilégryta med champinjoner och ris",
        "required_ingredients": [
            {"name": "fläskfilé", "amount": 125, "unit": "g"},
            {"name": "ris", "amount": 200, "unit": "g"},
            {"name": "champinjoner", "amount": 75, "unit": "g"},
            {"name": "grädde", "amount": 0.75, "unit": "dl"},
            {"name": "mjölk", "amount": 0.5, "unit": "dl"},
            {"name": "matfett", "amount": 1, "unit": "msk"}
        ],
        "optional_ingredients": [
            {"name": "gul lök", "amount": 0.25, "unit": "st"},
            {"name": "tomatpuré", "amount": 0.5, "unit": "tsk"},
            {"name": "hönsbuljongtärning", "amount": 0.25, "unit": "st"},
            {"name": "japansk soja", "amount": 0.5, "unit": "msk"},
            {"name": "senap", "amount": 0.5, "unit": "tsk"}
        ],
        "instructions": [
            "Bryn köttet.",
            "Stek lök och svamp.",
            "Tillsätt tomatpuré.",
            "Häll i grädde och mjölk.",
            "Smaka av och blanda ihop."
        ],
        "step_ingredients": [
            [{"name": "fläskfilé", "amount": 125, "unit": "g"}],
            [{"name": "gul lök", "amount": 0.25, "unit": "st"}, {"name": "champinjoner", "amount": 75, "unit": "g"}],
            [{"name": "grädde", "amount": 0.75, "unit": "dl"}, {"name": "mjölk", "amount": 0.5, "unit": "dl"}]
        ]
    },
    {
        "id": 11,
        "title": "Köttfärssås med pasta",
        "required_ingredients": [
            {"name": "pasta", "amount": 200, "unit": "g"},
            {"name": "köttfärs", "amount": 250, "unit": "g"},
            {"name": "krossade tomater", "amount": 400, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "gul lök", "amount": 0.5, "unit": "st"},
            {"name": "vitlök", "amount": 1, "unit": "klyfta"},
            {"name": "oregano", "amount": 1, "unit": "tsk"},
            {"name": "salt", "amount": 1, "unit": "krm"},
            {"name": "peppar", "amount": 1, "unit": "krm"}
        ],
        "instructions": [
            "Koka pastan enligt anvisning.",
            "Stek köttfärsen tills den är genomstekt.",
            "Tillsätt lök och vitlök och fräs.",
            "Häll i tomater och kryddor.",
            "Låt sjuda i 10–15 minuter.",
            "Servera med pasta."
        ],
        "step_ingredients": [
            [{"name": "pasta", "amount": 200, "unit": "g"}],
            [{"name": "köttfärs", "amount": 250, "unit": "g"}],
            [{"name": "gul lök", "amount": 0.5, "unit": "st"}, {"name": "vitlök", "amount": 1, "unit": "klyfta"}],
            [{"name": "krossade tomater", "amount": 400, "unit": "g"}, {"name": "oregano", "amount": 1, "unit": "tsk"}],
            [{"name": "salt", "amount": 1, "unit": "krm"}, {"name": "peppar", "amount": 1, "unit": "krm"}]
        ]
    },
    {
        "id": 12,
        "title": "Pannkakor",
        "required_ingredients": [
            {"name": "mjöl", "amount": 2, "unit": "dl"},
            {"name": "mjölk", "amount": 4, "unit": "dl"},
            {"name": "ägg", "amount": 2, "unit": "st"}
        ],
        "optional_ingredients": [
            {"name": "salt", "amount": 1, "unit": "krm"},
            {"name": "smör", "amount": 1, "unit": "msk"}
        ],
        "instructions": [
            "Vispa ihop mjöl, mjölk och ägg.",
            "Tillsätt salt.",
            "Stek tunna pannkakor i smör.",
            "Servera med valfri topping."
        ],
        "step_ingredients": [
            [{"name": "mjöl", "amount": 2, "unit": "dl"}, {"name": "mjölk", "amount": 4, "unit": "dl"}, {"name": "ägg", "amount": 2, "unit": "st"}],
            [{"name": "salt", "amount": 1, "unit": "krm"}],
            [{"name": "smör", "amount": 1, "unit": "msk"}],
            []
        ]
    },
    {
        "id": 13,
        "title": "Ugnsrostad potatis med kyckling",
        "required_ingredients": [
            {"name": "potatis", "amount": 500, "unit": "g"},
            {"name": "kyckling", "amount": 300, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "olja", "amount": 1, "unit": "msk"},
            {"name": "salt", "amount": 1, "unit": "tsk"},
            {"name": "peppar", "amount": 1, "unit": "tsk"},
            {"name": "paprikapulver", "amount": 1, "unit": "tsk"}
        ],
        "instructions": [
            "Sätt ugnen på 200°C.",
            "Skär potatis och kyckling i bitar.",
            "Blanda med olja och kryddor.",
            "Rosta i ugnen i ca 30–40 minuter.",
            "Servera varmt."
        ],
        "step_ingredients": [
            [{"name": "potatis", "amount": 500, "unit": "g"}, {"name": "kyckling", "amount": 300, "unit": "g"}],
            [{"name": "olja", "amount": 1, "unit": "msk"}, {"name": "salt", "amount": 1, "unit": "tsk"}, {"name": "peppar", "amount": 1, "unit": "tsk"}, {"name": "paprikapulver", "amount": 1, "unit": "tsk"}],
            []
        ]
    },
    {
        "id": 14,
        "title": "Tacos",
        "required_ingredients": [
            {"name": "tacobröd", "amount": 4, "unit": "st"},
            {"name": "köttfärs", "amount": 300, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "tacokrydda", "amount": 1, "unit": "påse"},
            {"name": "sallad", "amount": 100, "unit": "g"},
            {"name": "tomat", "amount": 2, "unit": "st"},
            {"name": "ost", "amount": 100, "unit": "g"},
            {"name": "gräddfil", "amount": 2, "unit": "dl"}
        ],
        "instructions": [
            "Stek köttfärsen.",
            "Tillsätt tacokrydda och lite vatten.",
            "Hacka grönsaker.",
            "Fyll bröden med kött och tillbehör.",
            "Servera direkt."
        ],
        "step_ingredients": [
            [{"name": "köttfärs", "amount": 300, "unit": "g"}],
            [{"name": "tacokrydda", "amount": 1, "unit": "påse"}],
            [{"name": "sallad", "amount": 100, "unit": "g"}, {"name": "tomat", "amount": 2, "unit": "st"}],
            [{"name": "tacobröd", "amount": 4, "unit": "st"}, {"name": "ost", "amount": 100, "unit": "g"}, {"name": "gräddfil", "amount": 2, "unit": "dl"}]
        ]
    },
    {
        "id": 15,
        "title": "Fisk i ugn med potatis",
        "required_ingredients": [
            {"name": "vit fisk", "amount": 300, "unit": "g"},
            {"name": "potatis", "amount": 400, "unit": "g"}
        ],
        "optional_ingredients": [
            {"name": "citron", "amount": 0.5, "unit": "st"},
            {"name": "smör", "amount": 1, "unit": "msk"},
            {"name": "dill", "amount": 10, "unit": "g"},
            {"name": "salt", "amount": 1, "unit": "tsk"},
            {"name": "peppar", "amount": 1, "unit": "tsk"}
        ],
        "instructions": [
            "Sätt ugnen på 200°C.",
            "Skala och koka potatisen.",
            "Lägg fisken i en ugnsform.",
            "Krydda och klicka på smör.",
            "Baka i ugnen i ca 20 minuter.",
            "Servera med potatis och dill."
        ],
        "step_ingredients": [
            [{"name": "potatis", "amount": 400, "unit": "g"}],
            [{"name": "vit fisk", "amount": 300, "unit": "g"}],
            [{"name": "citron", "amount": 0.5, "unit": "st"}, {"name": "smör", "amount": 1, "unit": "msk"}],
            [{"name": "dill", "amount": 10, "unit": "g"}, {"name": "salt", "amount": 1, "unit": "tsk"}, {"name": "peppar", "amount": 1, "unit": "tsk"}]
        ]
    }
]

# ============================================================
#  HELPERS
# ============================================================
UNIT_CONVERSIONS = {
    ("kg", "g"): 1000,
    ("g", "kg"): 1 / 1000,
    ("l", "dl"): 10,
    ("dl", "l"): 1 / 10,
    ("l", "ml"): 1000,
    ("ml", "l"): 1 / 1000,
    ("dl", "ml"): 100,
    ("ml", "dl"): 1 / 100
}

def convert(amount, from_unit, to_unit):
    if from_unit == to_unit:
        return amount
    factor = UNIT_CONVERSIONS.get((from_unit, to_unit))
    if factor is None:
        return None
    return amount * factor

def scale_ingredients(ings, factor):
    return [
        {**i, "amount": round(i["amount"] * factor, 3)}
        for i in ings
    ]


def normalize_name(n):
    return n.strip().lower()

BASE_UNITS = {
    "kg": ("g", 1000),
    "g": ("g", 1),
    "l": ("ml", 1000),
    "dl": ("ml", 100),
    "ml": ("ml", 1),
    "st": ("st", 1)
}

def normalize_unit(amount, unit):
    if unit not in BASE_UNITS:
        return amount, unit
    base, factor = BASE_UNITS[unit]
    return amount * factor, base


def gather_have_quantities(pantry_list):
    have = {}

    for item in pantry_list:
        if not isinstance(item, dict):
            continue

        name = normalize_name(item.get("name", ""))

        try:
            qty = float(item.get("quantity", 0))
        except:
            qty = 0

        unit = item.get("unit", "")

        if qty <= 0 or not name:
            continue

        qty, unit = normalize_unit(qty, unit)

        have.setdefault(name, {})
        have[name][unit] = have[name].get(unit, 0) + qty

    return have


def match_recipes(pantry, leftovers, portions=1, top_n=5):
    have = gather_have_quantities(pantry + leftovers)
    results = []

    for r in RECIPES:
        score = 0
        max_score = len(r["required_ingredients"]) * 2 + len(r["optional_ingredients"])

        matched_required = []
        matched_optional = []
        missing_required = []


        # REQUIRED = heavy weight
        for ing in r["required_ingredients"]:
           name = normalize_name(ing["name"])
           req_amt = ing["amount"]
           req_unit = ing["unit"]

           available = 0

           for u, qty in have.get(name, {}).items():
                converted = convert(qty, u, req_unit)
                if converted is not None:
                  available += converted

           if available >= req_amt:
                score += 2
                matched_required.append(name)
           else:
                missing_required.append(name)


        # OPTIONAL = lätt vikt
        for ing in r["optional_ingredients"]:
            name = normalize_name(ing["name"])
            if name in have:
                score += 1
                matched_optional.append(name)

        results.append({
         "id": r["id"],
         "title": r["title"],
         "score": round(score / max_score, 3),
         "matched_required": matched_required,
         "matched_optional": matched_optional,
         "missing_required": missing_required,
         "instructions": r["instructions"],
         "required_ingredients": scale_ingredients(r["required_ingredients"], portions),
         "optional_ingredients": scale_ingredients(r["optional_ingredients"], portions),
         "step_ingredients": [
            scale_ingredients(step, portions)
            for step in r["step_ingredients"]
         ]
})



    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# ============================================================
# FRONTEND HTML (YOUR HUGE DOCUMENT)
# ============================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>Next Meal</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
body {
  font-family: Arial, sans-serif;
  margin: 20px;
  background: #faf4e0;
}
h1 { color: #394c32; }

.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.section {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
}

.ingredient-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
}

.qty-box {
  width: 50px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 0 5px;
}

button {
  cursor: pointer;
  border-radius: 6px;
}

.add-btn {
  background: #394c32;
  color: white;
  border: none;
  padding: 5px 10px;
}

.remove-btn {
  background: #394c32;
  color: white;
  border: none;
  padding: 2px 6px;
}

.action {
  background: #394c32;
  color: white;
  border: none;
  padding: 8px 16px;
  margin: 5px 0;
}

.recipe {
  background: white;
  padding: 15px;
  margin-top: 20px;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0,0,0,0.15);
}

.details {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease-out;
}

.details.open {
  max-height: 1000px;
  transition: max-height 0.6s ease-in;
}

table.shopping {
  width: 100%;
  border-collapse: collapse;
}

.shopping td {
  padding: 4px;
  border-bottom: 1px solid #eee;
}

.done {
  text-decoration: line-through;
  color: gray;
}
</style>
</head>
<body>
<h1>🍲 Next Meal</h1>

<div class="container">
  <div class="section" id="pantrySection">
    <h3>Skafferi</h3>
    <input type="text" id="pantryInput" placeholder="t.ex. ris">
    <input type="number" id="pantryQty" placeholder="mängd" class="qty-box">
    <select id="pantryUnit">
      <option value="st">st</option>
      <option value="g">g</option>
      <option value="kg">kg</option>
      <option value="ml">ml</option>
      <option value="dl">dl</option>
      <option value="l">l</option>
    </select>
    <button class="add-btn" onclick="addIngredient('pantry')">Lägg till</button>
    <ul id="pantryList"></ul>
  </div>

  <div class="section" id="fridgeSection">
    <h3>Kyl</h3>
    <input type="text" id="fridgeInput" placeholder="t.ex. mjölk">
    <input type="number" id="fridgeQty" placeholder="mängd" class="qty-box">
    <select id="fridgeUnit">
      <option value="st">st</option>
      <option value="g">g</option>
      <option value="kg">kg</option>
      <option value="ml">ml</option>
      <option value="dl">dl</option>
      <option value="l">l</option>
    </select>
    <button class="add-btn" onclick="addIngredient('fridge')">Lägg till</button>
    <ul id="fridgeList"></ul>
  </div>

  <div class="section" id="freezerSection">
    <h3>Frys</h3>
    <input type="text" id="freezerInput" placeholder="t.ex. ärtor">
    <input type="number" id="freezerQty" placeholder="mängd" class="qty-box">
    <select id="freezerUnit">
      <option value="st">st</option>
      <option value="g">g</option>
      <option value="kg">kg</option>
      <option value="ml">ml</option>
      <option value="dl">dl</option>
      <option value="l">l</option>
    </select>
    <button class="add-btn" onclick="addIngredient('freezer')">Lägg till</button>
    <ul id="freezerList"></ul>
  </div>
</div>

<label>
  Portioner:
  <input type="number" id="portionInput" value="1" min="0.5" step="0.5">
</label>

<button class="action" onclick="findRecipes()">Hitta recept</button>
<button class="action" onclick="clearAll()">Rensa allt</button>

<h2>Förslag:</h2>
<div class="section">
  <h2>🗓️ Måltidsplan</h2>
  <ul id="mealPlanList"></ul>
  <button class="action" onclick="generateMealPlanShopping()">🛒 Generera inköpslista</button>
  <h3>🧾 Samlad inköpslista</h3>
  <ul id="mealPlanShopping"></ul>
</div>
<div id="results"></div>

<script>
// ---------------------------
// Convertion Chart
// ---------------------------
const UNIT_MAP = {
  kg: { base: "g", factor: 1000 },
  g:  { base: "g", factor: 1 },

  l:  { base: "ml", factor: 1000 },
  dl: { base: "ml", factor: 100 },
  ml: { base: "ml", factor: 1 },

  st: { base: "st", factor: 1 }
};

function normalizeUnitAndQuantity(qty, unit) {
  const u = UNIT_MAP[unit];
  if (!u) return { qty, unit }; // unknown unit → leave as-is
  return {
    qty: qty * u.factor,
    unit: u.base
  };
}
function normalizeItem(item) {
  const n = normalizeUnitAndQuantity(item.quantity, item.unit);
  return {
    name: item.name,
    quantity: n.qty,
    unit: n.unit
  };
}

// ---------------------------
// GLOBALS
// ---------------------------

let storageData = {
  pantry: [],
  fridge: [],
  freezer: []
};

window.RECIPE_STEP_MAP = {};   // recept-id => step_ingredients[]

// ---------------------------
// LOAD & SAVE
// ---------------------------

function removeItem(area, name, unit) {
  storageData[area] = storageData[area].filter(
    item => !(item.name === name && item.unit === unit)
  );

  saveInputs();
  renderStorageArea(area);
}


function saveInputs() {
  localStorage.setItem("storageData", JSON.stringify(storageData));
}

function loadInputs() {
  const raw = localStorage.getItem("storageData");
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      if (typeof parsed === "object") {
        storageData = {
          pantry: (parsed.pantry || []).map(normalizeItem),
          fridge: (parsed.fridge || []).map(normalizeItem),
          freezer: (parsed.freezer || []).map(normalizeItem)
        };
      }
    } catch (e) {
      console.warn("Corrupt localStorage, resetting.");
      storageData = { pantry: [], fridge: [], freezer: [] };
    }
  }

  saveInputs(); // 🔑 re-save normalized data
  renderStorageArea("pantry");
  renderStorageArea("fridge");
  renderStorageArea("freezer");
}

// ---------------------------
// RENDER
// ---------------------------

function renderStorageArea(area) {
  const list = document.getElementById(area + "List");
  list.innerHTML = "";

  storageData[area] = storageData[area].map(normalizeItem);

  storageData[area].forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class='ingredient-item'>
        <span>${escapeHtml(item.name)}:
          <span class="qty-value">${item.quantity}</span> ${escapeHtml(item.unit)}
        </span>
        <button class="remove-btn"
          onclick="removeItem('${area}', '${item.name}', '${item.unit}')">x</button>
      </div>`;
    list.appendChild(li);
  });
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}

// ---------------------------
// ADD / REMOVE INGREDIENTS
// ---------------------------

function addIngredient(area) {
  let name = document.getElementById(area + "Input").value.trim().toLowerCase();
  let qty = parseFloat(document.getElementById(area + "Qty").value);
  let unit = document.getElementById(area + "Unit").value;

  if (!name || isNaN(qty) || qty <= 0) {
    alert("Ogiltig ingrediens eller mängd");
    return;
  }

  // 🔑 AUTO UNIT CONVERSION
  const normalized = normalizeUnitAndQuantity(qty, unit);
  qty = normalized.qty;
  unit = normalized.unit;

  // 🔑 MERGE AFTER CONVERSION
  const existing = storageData[area].find(
    i => i.name === name && i.unit === unit
  );

  if (existing) {
    existing.quantity = Math.round((existing.quantity + qty) * 1000) / 1000;
  } else {
    storageData[area].push({ name, quantity: qty, unit });
  }

  saveInputs();
  renderStorageArea(area);

  document.getElementById(area + "Input").value = "";
  document.getElementById(area + "Qty").value = "";
}

// ---------------------------
// REQUEST RECIPES
// ---------------------------

async function findRecipes() {
  saveInputs();

  const collected = [
    ...storageData.pantry.map(i=>i.name),
    ...storageData.fridge.map(i=>i.name),
    ...storageData.freezer.map(i=>i.name)
  ];

  const portions = parseFloat(document.getElementById("portionInput").value) || 1;

const res = await fetch("/match", {
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: JSON.stringify({
    pantry: [
      ...storageData.pantry,
      ...storageData.fridge,
      ...storageData.freezer
    ],
    leftovers: [],
    limit: 100,
    portions
  })
});


  const data = await res.json();
  const recipes = data.matches;

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  recipes.forEach(r => {
    window.RECIPE_STEP_MAP[r.id] = r.step_ingredients || [];

    const div = document.createElement("div");
    div.className = "recipe";
    div.dataset.recipeId = r.id;

    let instrHtml = "<ol>";
    r.instructions.forEach((step, idx) => {
      const key = `recipe-${r.id}-step-${idx}`;
      const checked = localStorage.getItem(key) === "true" ? "checked" : "";
      instrHtml += `
        <li>
          <label>
            <input type='checkbox' ${checked} onchange="handleStepCheck(${r.id}, ${idx}, this.checked, '${key}')"> ${escapeHtml(step)}
          </label>
        </li>`;
    });
    instrHtml += "</ol>";

    div.innerHTML = `
      <h3>${escapeHtml(r.title)} (score ${r.score})</h3>
      <p>Obligatoriska du har: ${r.matched_required.join(", ") || "–"}</p>
      <p>Extra du har: ${r.matched_optional.join(", ") || "–"}</p>
      <button onclick="toggleDetails(${r.id})">Visa detaljer</button>
      <button onclick="addToMealPlan(${r.id})">➕ Lägg till i plan</button>
      <div id="details-${r.id}" class="details">

        <h4>Ingredienser</h4>
        <p><b>Obligatoriska:</b></p>
        <ul>
            ${r.required_ingredients.map(i =>
                `<li>${escapeHtml(i.name)} ${i.amount} ${escapeHtml(i.unit)}</li>`
            ).join("")}
        </ul>

        <p><b>Valfria:</b></p>
        <ul>
            ${r.optional_ingredients.map(i =>
                `<li>${escapeHtml(i.name)} ${i.amount} ${escapeHtml(i.unit)}</li>`
            ).join("")}
        </ul>

        <h4>Instruktioner</h4>
        ${instrHtml}

        <h4>Inköpslista</h4>
        <table class="shopping" id="shopping-${r.id}"><tr><td>Laddar...</td></tr></table>
      </div>`;

    resultsDiv.appendChild(div);
    getShopping(r.id);
  });
}

function toggleDetails(id) {
  document.getElementById("details-" + id).classList.toggle("open");
}



// ---------------------------
// MEAL PLAN
// ---------------------------

let mealPlan = [];

function addToMealPlan(recipeId) {
  const portions = parseFloat(document.getElementById("portionInput").value) || 1;

  mealPlan.push({ recipeId, portions });
  renderMealPlan();
}

function removeFromMealPlan(index) {
  mealPlan.splice(index, 1);
  renderMealPlan();
}

function renderMealPlan() {
  const list = document.getElementById("mealPlanList");
  list.innerHTML = "";

  mealPlan.forEach((item, i) => {
    const li = document.createElement("li");

    const recipe = document.querySelector(`[data-recipe-id='${item.recipeId}'] h3`)?.innerText || "Recept";

    li.innerHTML = `
      ${recipe} (${item.portions} portioner)
      <button onclick="removeFromMealPlan(${i})">❌</button>
    `;

    list.appendChild(li);
  });
}

// ---------------------------
// COMBINED SHOPPING LIST
// ---------------------------

async function generateMealPlanShopping() {
  const allItems = [
    ...storageData.pantry,
    ...storageData.fridge,
    ...storageData.freezer
  ];

  const res = await fetch("/mealplan", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      pantry: allItems,
      meal_plan: mealPlan
    })
  });

  const data = await res.json();

  const list = document.getElementById("mealPlanShopping");
  list.innerHTML = "";

  if (!data.shopping_list.length) {
    list.innerHTML = "<li>Du har allt! 🎉</li>";
    return;
  }

  data.shopping_list.forEach((item, index) => {
  const li = document.createElement("li");

  const key = `mealplan-item-${index}`;
  const checked = localStorage.getItem(key) === "true" ? "checked" : "";

  li.innerHTML = `
    <label>
      <input type="checkbox" ${checked}
        onchange="toggleShoppingItem(this, '${key}')">
      <span class="${checked ? 'done' : ''}">${item}</span>
    </label>

    <button onclick="addShoppingTo('pantry', '${item}')">🥫</button>
    <button onclick="addShoppingTo('fridge', '${item}')">❄️</button>
    <button onclick="addShoppingTo('freezer', '${item}')">🧊</button>
  `;

  list.appendChild(li);
});
}

// ---------------------------
// SHOPPING LIST
// ---------------------------

async function getShopping(recipeId) {
  const allItems = [
    ...storageData.pantry,
    ...storageData.fridge,
    ...storageData.freezer
  ];

  const res = await fetch("/shoppinglist", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
        pantry: allItems,
        leftovers: [],
        recipe_id: recipeId,
        portions: parseFloat(document.getElementById("portionInput").value) || 1
    })

  });

  const data = await res.json();
  const table = document.getElementById("shopping-" + recipeId);
  table.innerHTML = "";

  const req = data.shopping_list.required;
  const opt = data.shopping_list.optional;

  if (req.length === 0 && opt.length === 0) {
    table.innerHTML = "<tr><td>Du har allt! ✓</td></tr>";
    return;
  }

  if (req.length) {
    table.innerHTML += `<tr><td><b>Obligatoriskt:</b></td></tr>`;
    req.forEach((item, index) => {
  const key = `recipe-${recipeId}-item-${index}`;
  const checked = localStorage.getItem(key) === "true" ? "checked" : "";

  table.innerHTML += `
    <tr>
      <td>
        <label>
          <input type="checkbox" ${checked}
            onchange="toggleShoppingItem(this, '${key}')">
          <span class="${checked ? 'done' : ''}">
            ${escapeHtml(item)}
          </span>
        </label>

        <button onclick="addShoppingTo('pantry', '${item}')">🥫</button>
        <button onclick="addShoppingTo('fridge', '${item}')">❄️</button>
        <button onclick="addShoppingTo('freezer', '${item}')">🧊</button>
      </td>
    </tr>
  `;
});
  }

  if (opt.length) {
    table.innerHTML += `<tr><td><b>Valfritt:</b></td></tr>`;
    opt.forEach(i => {
      table.innerHTML += `<tr><td>${escapeHtml(i)}</td></tr>`;
    });
  }
}

document.getElementById("portionInput").addEventListener("change", () => {
  findRecipes();
  document.querySelectorAll(".recipe").forEach(recipeEl => {
    const id = parseInt(recipeEl.dataset.recipeId);
    if (!isNaN(id)) {
      getShopping(id);
    }
  });
});



// ---------------------------
// STEP CONSUMPTION
// ---------------------------

function normalizeName(n) {
  return n.toLowerCase().trim();
}

function handleStepCheck(recipeId, stepIndex, checked, key) {
  const factor = checked ? -1 : 1;
  useIngredients(recipeId, stepIndex, factor);
  localStorage.setItem(key, checked ? "true" : "false");
}

function useIngredients(recipeId, stepIndex, factor) {
  const steps = window.RECIPE_STEP_MAP[recipeId];
  if (!steps) return;

  const ingredients = steps[stepIndex] || [];

  ingredients.forEach(ing => {
    const name = normalizeName(ing.name);
    const unit = ing.unit || "";
    const amount = parseFloat(ing.amount) * factor;

    ["pantry","fridge","freezer"].forEach(area => {
      storageData[area].forEach(item => {
        if (normalizeName(item.name) === name) {
             const converted = normalizeUnitAndQuantity(amount, unit);

             if (item.unit === converted.unit) {
                  item.quantity = Math.max(
                    0,
                    Math.round((item.quantity + converted.qty) * 1000) / 1000
                  );
             }
        }

      });
    });
  });

  saveInputs();
  renderStorageArea("pantry");
  renderStorageArea("fridge");
  renderStorageArea("freezer");
}

// ---------------------------
// SHOPPING INTERACTION
// ---------------------------

function toggleShoppingItem(checkbox, key) {
  const span = checkbox.nextElementSibling;

  if (checkbox.checked) {
    span.classList.add("done");
    localStorage.setItem(key, "true");
  } else {
    span.classList.remove("done");
    localStorage.setItem(key, "false");
  }
}

// Convert "mjölk 2 dl" → {name, qty, unit}
function parseShoppingItem(text) {
  const parts = text.split(" ");

  if (parts.length < 3) {
    return null;
  }

  const name = parts[0];
  const qty = parseFloat(parts[1]);
  const unit = parts[2];

  if (isNaN(qty)) return null;

  return { name, quantity: qty, unit };
}

function addShoppingTo(area, itemText) {
  const parsed = parseShoppingItem(itemText);

  if (!parsed) {
    alert("Kunde inte tolka varan ❗");
    return;
  }

  const normalized = normalizeUnitAndQuantity(parsed.quantity, parsed.unit);

  const existing = storageData[area].find(
    i => i.name === parsed.name && i.unit === normalized.unit
  );

  if (existing) {
    existing.quantity += normalized.qty;
  } else {
    storageData[area].push({
      name: parsed.name,
      quantity: normalized.qty,
      unit: normalized.unit
    });
  }

  saveInputs();
  renderStorageArea(area);
}





// ---------------------------
// CLEAR ALL
// ---------------------------

function clearAll() {
  if (!confirm("Vill du verkligen rensa allt?")) return;
  localStorage.clear();
  storageData = { pantry: [], fridge: [], freezer: [] };
  renderStorageArea("pantry");
  renderStorageArea("fridge");
  renderStorageArea("freezer");
}

// ---------------------------
// STARTUP
// ---------------------------

window.onload = loadInputs;

</script>
</body>
</html>
"""

# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/match", methods=["POST"])
def match_endpoint():
    data = request.json or {}

    pantry = data.get("pantry", [])
    leftovers = data.get("leftovers", [])
    limit = int(data.get("limit", len(RECIPES)))
    portions = float(data.get("portions", 1))

    matches = match_recipes(
        pantry,
        leftovers,
        portions=portions,
        top_n=limit
    )

    return jsonify({
        "matches": matches,
        "total": len(RECIPES),
        "portions": portions
    })


@app.route("/shoppinglist", methods=["POST"])
def shopping():
    data = request.json or {}
    pantry = data.get("pantry", [])
    leftovers = data.get("leftovers", [])
    recipe_id = data.get("recipe_id")

    portions = float(data.get("portions", 1))

    recipe = next((r for r in RECIPES if r["id"] == recipe_id), None)
    if recipe is None:
        return jsonify({"error": "Recipe not found"}), 404

    have = gather_have_quantities(pantry + leftovers)

    def compute_missing(ing):
        name = normalize_name(ing["name"])
        required = float(ing["amount"]) * portions
        unit = ing["unit"]

        available = 0
        for u, qty in have.get(name, {}).items():
            converted = convert(qty, u, unit)
            if converted is not None:
                available += converted

        missing = round(required - available, 3)

        if missing <= 0:
          return None

        return {
            "name": name,
            "amount": missing,
            "unit": unit
        }



    missing_required = []
    missing_optional = []

    for ing in recipe["required_ingredients"]:
        m = compute_missing(ing)
        if m: missing_required.append(m)

    for ing in recipe["optional_ingredients"]:
        m = compute_missing(ing)
        if m: missing_optional.append(m)

    return jsonify({
    "recipe": recipe["title"],
    "shopping_list": {
        "required": [
            f"{m['name']} {m['amount']} {m['unit']}" for m in missing_required
        ],
        "optional": [
            f"{m['name']} {m['amount']} {m['unit']}" for m in missing_optional
        ]
    }
})

@app.route("/mealplan", methods=["POST"])
def mealplan():
    data = request.json or {}

    pantry = data.get("pantry", [])
    meal_plan = data.get("meal_plan", [])

    have = gather_have_quantities(pantry)

    combined_needed = {}

    for entry in meal_plan:
        recipe_id = entry.get("recipeId")
        portions = float(entry.get("portions", 1))

        recipe = next((r for r in RECIPES if r["id"] == recipe_id), None)
        if not recipe:
            continue

        for ing in recipe["required_ingredients"]:
            name = normalize_name(ing["name"])
            required = ing["amount"] * portions
            unit = ing["unit"]

            # Calculate available
            available = 0
            for u, qty in have.get(name, {}).items():
                converted = convert(qty, u, unit)
                if converted:
                    available += converted

            missing = max(required - available, 0)

            if missing > 0:
                key = (name, unit)
                combined_needed[key] = combined_needed.get(key, 0) + missing

    # Format output
    shopping_list = [
        f"{name} {round(amount,2)} {unit}"
        for (name, unit), amount in combined_needed.items()
    ]

    return jsonify({
        "shopping_list": shopping_list
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

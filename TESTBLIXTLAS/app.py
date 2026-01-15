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
            {"name": "ris", "amount": 2, "unit": "dl"},
            {"name": "kyckling", "amount": 200, "unit": "g"},
            {"name": "agg", "amount": 2, "unit": "st"}
        ],
        "optional_ingredients": [
            {"name": "soja", "amount": 1, "unit": "msk"},
            {"name": "morot", "amount": 1, "unit": "st"},
            {"name": "lok", "amount": 0.5, "unit": "st"}
        ],
        "instructions": [
            "Skär kycklingen i bitar och stek tills den är genomstekt.",
            "Tillsatt hackad lök och morot, fräs i några minuter.",
            "Knack i ägg och rör om.",
            "Blanda i ris och soja, stek tills allt är varmt."
        ],
        "step_ingredients": [
            [{"name": "kyckling", "amount": 200, "unit": "g"}],
            [{"name": "lok", "amount": 0.5, "unit": "st"}, {"name": "morot", "amount": 1, "unit": "st"}],
            [{"name": "agg", "amount": 2, "unit": "st"}],
            [{"name": "ris", "amount": 2, "unit": "dl"}, {"name": "soja", "amount": 1, "unit": "msk"}]
        ]
    },
    {
        "id": 2,
        "title": "Tomat- och linsgryta",
        "required_ingredients": [
            {"name":"linser","amount":2,"unit":"dl"},
            {"name":"tomat","amount":400,"unit":"g"}
        ],
        "optional_ingredients": [
            {"name":"lok","amount":1,"unit":"st"},
            {"name":"vitlok","amount":2,"unit":"klyfta"},
            {"name":"spiskummin","amount":1,"unit":"tsk"}
        ],
        "instructions": [
            "Fräs lök och vitlök i lite olja.",
            "Tillsatt tomat och kryddor.",
            "Häll i linser och vatten, låt koka tills linserna är mjuka."
        ],
        "step_ingredients": [
            [{"name":"lok","amount":1,"unit":"st"}, {"name":"vitlok","amount":2,"unit":"klyfta"}],
            [{"name":"tomat","amount":400,"unit":"g"}, {"name":"spiskummin","amount":1,"unit":"tsk"}],
            [{"name":"linser","amount":2,"unit":"dl"}]
        ]
    },
    {
        "id": 3,
        "title": "Pasta med ostsås",
        "required_ingredients": [
            {"name":"pasta","amount":200,"unit":"g"},
            {"name":"ost","amount":100,"unit":"g"},
            {"name":"mjolk","amount":2,"unit":"dl"}
        ],
        "optional_ingredients": [
            {"name":"smor","amount":10,"unit":"g"},
            {"name":"peppar","amount":1,"unit":"tsk"},
            {"name":"salt","amount":1,"unit":"tsk"}
        ],
        "instructions": [
            "Koka pastan enligt anvisningarna.",
            "Smält smör i en kastrull, tillsätt mjölk och ost.",
            "Rör tills osten har smält.",
            "Blanda med pastan och krydda."
        ],
        "step_ingredients": [
            [ {"name":"pasta","amount":200,"unit":"g"} ],
            [ {"name":"smor","amount":10,"unit":"g"}, {"name":"mjolk","amount":2,"unit":"dl"}, {"name":"ost","amount":100,"unit":"g"} ],
            [],
            []
        ]
    },
    {
        "id": 4,
        "title": "Grönsakssoppa",
        "required_ingredients": [
            {"name":"potatis","amount":3,"unit":"st"},
            {"name":"morot","amount":2,"unit":"st"},
            {"name":"vatten","amount":1,"unit":"l"}
        ],
        "optional_ingredients": [
            {"name":"selleri","amount":1,"unit":"st"},
            {"name":"buljong","amount":1,"unit":"tärning"},
            {"name":"persilja","amount":1,"unit":"msk"}
        ],
        "instructions": [
            "Skal och tärna potatis och morot.",
            "Koka i vatten med buljong.",
            "Tillsatt selleri och låt sjuda tills grönsakerna är mjuka.",
            "Servera med hackad persilja."
        ],
        "step_ingredients": [
            [ {"name":"potatis","amount":3,"unit":"st"}, {"name":"morot","amount":2,"unit":"st"} ],
            [ {"name":"vatten","amount":1,"unit":"l"}, {"name":"buljong","amount":1,"unit":"tärning"} ],
            [ {"name":"selleri","amount":1,"unit":"st"} ],
            [ {"name":"persilja","amount":1,"unit":"msk"} ]
        ]
    },
    {
        "id": 5,
        "title": "Kycklingwok",
        "required_ingredients": [
            {"name":"kyckling","amount":250,"unit":"g"},
            {"name":"gronsaker","amount":300,"unit":"g"}
        ],
        "optional_ingredients": [
            {"name":"soja","amount":1,"unit":"msk"},
            {"name":"nudlar","amount":200,"unit":"g"},
            {"name":"vitlok","amount":1,"unit":"klyfta"}
        ],
        "instructions": [
            "Stek kycklingen tills den är gyllenbrun.",
            "Tillsatt grönsaker och vitlök, fräs snabbt.",
            "Blanda i soja och kokta nudlar.",
            "Servera genast."
        ],
        "step_ingredients": [
            [ {"name":"kyckling","amount":250,"unit":"g"} ],
            [ {"name":"gronsaker","amount":300,"unit":"g"}, {"name":"vitlok","amount":1,"unit":"klyfta"} ],
            [ {"name":"soja","amount":1,"unit":"msk"}, {"name":"nudlar","amount":200,"unit":"g"} ],
            []
        ]
    },
    {
        "id": 6,
        "title": "Omelett",
        "required_ingredients": [
            {"name":"agg","amount":3,"unit":"st"}
        ],
        "optional_ingredients": [
            {"name":"ost","amount":30,"unit":"g"},
            {"name":"tomat","amount":1,"unit":"st"},
            {"name":"skinka","amount":50,"unit":"g"}
        ],
        "instructions": [
            "Vispa äggen och krydda.",
            "Häll i en varm panna.",
            "Tillsätt ost, tomat och skinka.",
            "Vik ihop och servera."
        ],
        "step_ingredients": [
            [ {"name":"agg","amount":3,"unit":"st"} ],
            [],
            [ {"name":"ost","amount":30,"unit":"g"}, {"name":"tomat","amount":1,"unit":"st"}, {"name":"skinka","amount":50,"unit":"g"} ],
            []
        ]
    }
]

# ============================================================
#  HELPERS
# ============================================================

def normalize_name(n):
    return n.strip().lower()

def gather_have_quantities(pantry_list):
    have = {}

    for item in pantry_list:
        if not isinstance(item, dict):
            continue

        name = normalize_name(item.get("name", ""))
        try:
            qty = float(item.get("quantity", 0))
        except (TypeError, ValueError):
            qty = 0

        unit = item.get("unit", "") or ""

        if qty <= 0 or not name:
            continue

        have.setdefault(name, {})
        have[name][unit] = have[name].get(unit, 0) + qty

    return have



def match_recipes(pantry, leftovers, top_n=5):
    have_names = set()

    for i in pantry:
        have_names.add(normalize_name(i["name"]) if isinstance(i, dict) else normalize_name(i))

    for i in leftovers:
        have_names.add(normalize_name(i["name"]) if isinstance(i, dict) else normalize_name(i))

    results = []

    for r in RECIPES:
        req_names = [normalize_name(i["name"]) for i in r["required_ingredients"]]
        opt_names = [normalize_name(i["name"]) for i in r["optional_ingredients"]]

        matched_req = [n for n in req_names if n in have_names]
        matched_opt = [n for n in opt_names if n in have_names]
        missing_req = [n for n in req_names if n not in have_names]
        missing_opt = [n for n in opt_names if n not in have_names]

        score = len(matched_req + matched_opt) / max(len(req_names + opt_names), 1)

        results.append({
            "id": r["id"],
            "title": r["title"],
            "score": round(score, 3),
            "matched_required": matched_req,
            "matched_optional": matched_opt,
            "missing_required": missing_req,
            "missing_optional": missing_opt,
            "instructions": r["instructions"],
            "required_ingredients": r["required_ingredients"],
            "optional_ingredients": r["optional_ingredients"],
            "step_ingredients": r["step_ingredients"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]

# ============================================================
# FRONTEND HTML (YOUR HUGE DOCUMENT)
# ============================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>Next Meal+</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
body {
  font-family: Arial, sans-serif;
  margin: 20px;
  background: #fafafa;
}
h1 { color: #2c3e50; }
/* (… entire CSS … remain intact) */
</style>
</head>
<body>
<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>Next Meal+</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
body {
  font-family: Arial, sans-serif;
  margin: 20px;
  background: #fafafa;
}
h1 { color: #2c3e50; }

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
  background: #2ecc71;
  color: white;
  border: none;
  padding: 5px 10px;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 2px 6px;
}

.action {
  background: #3498db;
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
<h1>🍲 Next Meal+</h1>

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

<button class="action" onclick="findRecipes()">Hitta recept</button>
<button class="action" onclick="clearAll()">Rensa allt</button>

<h2>Förslag:</h2>
<div id="results"></div>

<script>

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
          pantry: Array.isArray(parsed.pantry) ? parsed.pantry : [],
          fridge: Array.isArray(parsed.fridge) ? parsed.fridge : [],
          freezer: Array.isArray(parsed.freezer) ? parsed.freezer : []
        };
      }
    } catch (e) {
      console.warn("Corrupt localStorage, resetting.");
    }
  }

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

  storageData[area].forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class='ingredient-item'>
        <span>${escapeHtml(item.name)}: <span class="qty-value">${item.quantity}</span> ${escapeHtml(item.unit)}</span>
        <button class="remove-btn" onclick="removeItem('${area}', '${item.name}')">x</button>
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
  const name = document.getElementById(area + "Input").value.trim().toLowerCase();
  const qty = parseFloat(document.getElementById(area + "Qty").value);
  const unit = document.getElementById(area + "Unit").value;

  if (!name || isNaN(qty) || qty <= 0) {
    alert("Ogiltig ingrediens eller mängd");
    return;
  }

  storageData[area].push({ name, quantity: qty, unit });
  saveInputs();
  renderStorageArea(area);

  document.getElementById(area + "Input").value = "";
  document.getElementById(area + "Qty").value = "";
}

function removeItem(area, name) {
  storageData[area] = storageData[area].filter(i => i.name !== name);
  saveInputs();
  renderStorageArea(area);
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

  const res = await fetch("/match", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ pantry: collected, leftovers: [], limit: 10 })
  });

  const data = await res.json();
  const recipes = data.matches;

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  recipes.forEach(r => {
    window.RECIPE_STEP_MAP[r.id] = r.step_ingredients || [];

    const div = document.createElement("div");
    div.className = "recipe";

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
      <div id="details-${r.id}" class="details">
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
      recipe_id: recipeId
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
    req.forEach(i => {
      table.innerHTML += `<tr><td>${escapeHtml(i)}</td></tr>`;
    });
  }

  if (opt.length) {
    table.innerHTML += `<tr><td><b>Valfritt:</b></td></tr>`;
    opt.forEach(i => {
      table.innerHTML += `<tr><td>${escapeHtml(i)}</td></tr>`;
    });
  }
}


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
        if (normalizeName(item.name) === name && item.unit === unit) {
          item.quantity = Math.max(0, item.quantity + amount);
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
    limit = int(data.get("limit", 5))

    matches = match_recipes(pantry, leftovers, top_n=limit)
    return jsonify({"matches": matches, "total": len(RECIPES)})


@app.route("/shoppinglist", methods=["POST"])
def shopping():
    data = request.json or {}
    pantry = data.get("pantry", [])
    leftovers = data.get("leftovers", [])
    recipe_id = data.get("recipe_id")

    recipe = next((r for r in RECIPES if r["id"] == recipe_id), None)
    if recipe is None:
        return jsonify({"error": "Recipe not found"}), 404

    have = gather_have_quantities(pantry + leftovers)

    def compute_missing(ing):
        name = normalize_name(ing["name"])
        required = float(ing["amount"])
        unit = ing["unit"]

        available = have.get(name, {}).get(unit, 0)
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



# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify, render_template_string
app = Flask(__name__)

RECIPES = [
    {
        "id": 1,
        "title": "Stekt ris med kyckling",
        "required_ingredients": ["ris", "kyckling", "ägg"],
        "optional_ingredients": ["soja", "morot", "lök"],
        "instructions": [
            "Skär kycklingen i bitar och stek tills den är genomstekt.",
            "Tillsatt hackad lök och morot, fräs i några minuter.",
            "Knack i ägg och rör om.",
            "Blanda i ris och soja, stek tills allt är varmt."
        ]
    },
    {
        "id": 2,
        "title": "Tomat- och linsgryta",
        "required_ingredients": ["linser", "tomat"],
        "optional_ingredients": ["lök", "vitlök", "spiskummin"],
        "instructions": [
            "Fräs lök och vitlök i lite olja.",
            "Tillsatt tomat och kryddor.",
            "Häll i linser och vatten, låt koka tills linserna är mjuka."
        ]
    },
    {
        "id": 3,
        "title": "Pasta med ostsås",
        "required_ingredients": ["pasta", "ost", "mjölk"],
        "optional_ingredients": ["smör", "peppar", "salt"],
        "instructions": [
            "Koka pastan enligt anvisningarna.",
            "Smält smör i en kastrull, tillsätt mjölk och ost.",
            "Rör tills osten har smält.",
            "Blanda med pastan och krydda."
        ]
    },
    {
        "id": 4,
        "title": "Grönsakssoppa",
        "required_ingredients": ["potatis", "morot", "vatten"],
        "optional_ingredients": ["selleri", "buljong", "persilja"],
        "instructions": [
            "Skal och tarning potatis och morot.",
            "Koka i vatten med buljong.",
            "Tillsatt selleri och lat sjuda tills gronsakerna ar mjuka.",
            "Servera med hackad persilja."
        ]
    },
    {
        "id": 5,
        "title": "Kycklingwok",
        "required_ingredients": ["kyckling", "grönsaker"],
        "optional_ingredients": ["soja", "nudlar", "vitlok"],
        "instructions": [
            "Stek kycklingen tills den är gyllenbrun.",
            "Tillsatt grönsaker och vitlok, fräs snabbt.",
            "Blanda i soja och kokta nudlar.",
            "Servera genast."
        ]
    },
    {
        "id": 6,
        "title": "Omelett",
        "required_ingredients": ["ägg"],
        "optional_ingredients": ["ost", "tomat", "skinka"],
        "instructions": [
            "Vispa äggen och krydda.",
            "Häll i en varm panna.",
            "Tillsätt ost, tomat och skinka.",
            "Vik ihop och servera."
        ]
    },
]

def match_recipes(pantry, leftovers, top_n=5):
    have = set([i.strip().lower() for i in pantry + leftovers])
    results = []

    for r in RECIPES:
        req = [i.lower() for i in r.get("required_ingredients", [])]
        opt = [i.lower() for i in r.get("optional_ingredients", [])]

        matched_req = [i for i in req if i in have]
        missing_req = [i for i in req if i not in have]
        matched_opt = [i for i in opt if i in have]
        missing_opt = [i for i in opt if i not in have]

        score = len(matched_opt+matched_req) / max(len(opt+req), 1)

        results.append({
            "id": r["id"],
            "title": r["title"],
            "score": round(score, 3),
            "matched_required": matched_req,
            "matched_optional": matched_opt,
            "missing_required": missing_req,
            "missing_optional": missing_opt,
            "instructions": r["instructions"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


# ---- HTML + JS ----
HTML_PAGE = """
<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <title>Next Meal</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; }
    h1 { color: #2c3e50; }
    input, button { padding: 6px; margin: 4px; }
    .recipe { border: 1px solid #ccc; padding: 10px; margin: 10px 0; border-radius: 8px; }
    .missing { color: #c0392b; }
    .matched { color: #27ae60; }
    .details { max-height: 0; overflow: hidden; transition: max-height 0.5s ease-out; }
    .details.open { max-height: 600px; transition: max-height 0.8s ease-in; }
    ol, ul { padding-left: 20px; }
    li { margin: 5px 0; cursor: pointer; }
    label { cursor: pointer; }
    .done { text-decoration: line-through; color: gray; }
    .list-section { margin-bottom: 20px; }
    .input-row { margin-bottom: 8px; }
    button.add-btn { background: #2ecc71; color: white; border: none; border-radius: 6px; cursor: pointer; padding: 5px 10px; }
    button.remove-btn { background: #e74c3c; color: white; border: none; border-radius: 6px; cursor: pointer; padding: 2px 8px; margin-left: 6px; }
    button.action { background: #3498db; color: white; border: none; border-radius: 8px; cursor: pointer; padding: 8px 16px; margin: 5px; }
  </style>
</head>
<body>
  <h1>🍲 Next Meal</h1>
  <p>Skriv in vad du har hemma. En ingrediens per rad:</p>

  <div class="list-section">
    <h3>Skafferi</h3>
    <div class="input-row">
      <input type="text" id="pantryInput" placeholder="t.ex. ris">
      <button class="add-btn" onclick="addItem('pantry')">Lägg till</button>
    </div>
    <ul id="pantryList"></ul>
  </div>

  <div class="list-section">
    <h3>Kyl</h3>
    <div class="input-row">
      <input type="text" id="fridgeInput" placeholder="t.ex. mjölk">
      <button class="add-btn" onclick="addItem('fridge')">Lägg till</button>
    </div>
    <ul id="fridgeList"></ul>
  </div>

  <div class="list-section">
    <h3>Frys</h3>
    <div class="input-row">
      <input type="text" id="freezerInput" placeholder="t.ex. ärtor">
      <button class="add-btn" onclick="addItem('freezer')">Lägg till</button>
    </div>
    <ul id="freezerList"></ul>
  </div>

  <div class="list-section">
    <h3>Rester</h3>
    <div class="input-row">
      <input type="text" id="leftoversInput" placeholder="t.ex. kycklinggryta">
      <button class="add-btn" onclick="addItem('leftovers')">Lägg till</button>
    </div>
    <ul id="leftoversList"></ul>
  </div>

  <button class="action" onclick="findRecipes()">Hitta recept</button>
  <button class="action" onclick="clearAll()">Rensa allt sparat</button>
  <button class="action" onclick="clearCheckboxes()">Rensa bara checkboxar</button>

  <h2>Förslag:</h2>
  <div id="results"></div>

<script>
let currentLimit = 5;
let allRecipes = [];

function addItem(type) {
  const input = document.getElementById(type + "Input");
  const value = input.value.trim().toLowerCase();
  if (!value) return;

  const list = document.getElementById(type + "List");
  if (Array.from(list.children).some(li => li.firstChild.textContent === value)) {
    alert("Den ingrediensen finns redan i " + type + "!");
    input.value = "";
    return;
  }

  const li = document.createElement("li");
  li.textContent = value;
  const btn = document.createElement("button");
  btn.textContent = "x";
  btn.className = "remove-btn";
  btn.onclick = () => { li.remove(); saveInputs(); };
  li.appendChild(btn);
  list.appendChild(li);
  input.value = "";
  saveInputs();
}

function getListValues(type) {
  return Array.from(document.querySelectorAll(`#${type}List li`)).map(li => li.firstChild.textContent);
}

function saveInputs() {
  const lists = ["pantry", "fridge", "freezer", "leftovers"];
  lists.forEach(l => localStorage.setItem(l, JSON.stringify(getListValues(l))));
}

function loadInputs() {
  const lists = ["pantry", "fridge", "freezer", "leftovers"];
  lists.forEach(l => {
    const data = JSON.parse(localStorage.getItem(l) || "[]");
    data.forEach(i => addItemFromMemory(l, i));
  });
}

function addItemFromMemory(type, value) {
  const list = document.getElementById(type + "List");
  const li = document.createElement("li");
  li.textContent = value;
  const btn = document.createElement("button");
  btn.textContent = "x";
  btn.className = "remove-btn";
  btn.onclick = () => { li.remove(); saveInputs(); };
  li.appendChild(btn);
  list.appendChild(li);
}

function clearAll() {
  if (confirm("Är du säker på att du vill rensa ALLT (skafferi, kyl, frys, rester & checkboxar)?")) {
    localStorage.clear();
    location.reload();
  }
}

function clearCheckboxes() {
  if (confirm("Rensa bara checkboxar (instruktioner & inköpslista), men behåll Skafferi, Kyl, Frys och Rester?")) {
    const saved = {};
    ["pantry","fridge","freezer","leftovers"].forEach(l => saved[l] = localStorage.getItem(l));
    localStorage.clear();
    Object.keys(saved).forEach(k => {
      if (saved[k]) localStorage.setItem(k, saved[k]);
    });
    location.reload();
  }
}

// --- Matchning ---
async function findRecipes(loadMore = false) {
  saveInputs();

  const pantry = getListValues("pantry");
  const fridge = getListValues("fridge");
  const freezer = getListValues("freezer");
  const leftovers = getListValues("leftovers");

  const allItems = pantry.concat(fridge, freezer, leftovers);

  if (!loadMore) {
    currentLimit = 5;
    allRecipes = [];
    document.getElementById("results").innerHTML = "";
  } else {
    currentLimit += 5;
  }

  const res = await fetch("/match", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pantry: allItems, leftovers: [], limit: currentLimit })
  });
  const data = await res.json();
  const recipes = data.matches;
  const total = data.total;

  const newRecipes = recipes.slice(allRecipes.length);
  allRecipes = recipes;

  const resultsDiv = document.getElementById("results");

  newRecipes.forEach(r => {
    const div = document.createElement("div");
    div.className = "recipe";

    let instrList = "<ol>";
    r.instructions.forEach((step, idx) => {
      const key = "recipe-" + r.id + "-step-" + idx;
      const checked = localStorage.getItem(key) === "true" ? "checked" : "";
      const doneClass = checked ? "done" : "";
      instrList += `
        <li class="${doneClass}">
          <label>
            <input type='checkbox' ${checked} onchange="toggleDone(this, '${key}')"> ${step}
          </label>
        </li>`;
    });
    instrList += "</ol>";

    div.innerHTML = `
      <h3>${r.title} (score ${r.score})</h3>
      <p class="matched">Obligatoriska du har: ${r.matched_required.join(", ") || "–"}</p>  
      <p class="matched">Extra du har: ${r.matched_optional.join(", ") || "–"}</p>
      <p class="missing">Obligatoriska som saknas: ${r.missing_required.join(", ") || "–"}</p>
      <p class="missing">Extra som saknas: ${r.missing_optional.join(", ") || "–"}</p>
      <button onclick="toggleDetails(${r.id})">Visa detaljer</button>
      <div id="details-${r.id}" class="details">
        <h4>Instruktioner</h4>
        ${instrList}
        <h4>Inköpslista</h4>
        <ul id="shopping-${r.id}"><li>Laddar...</li></ul>
      </div>
    `;
    resultsDiv.appendChild(div);
    getShopping(r.id);
  });

  let loadMoreBtn = document.getElementById("loadMoreBtn");
  if (!loadMoreBtn) {
    loadMoreBtn = document.createElement("button");
    loadMoreBtn.id = "loadMoreBtn";
    loadMoreBtn.innerText = "Ladda fler recept";
    loadMoreBtn.className = "action";
    loadMoreBtn.onclick = () => findRecipes(true);
    resultsDiv.appendChild(loadMoreBtn);
  }

  if (recipes.length >= total) {
    loadMoreBtn.style.display = "none";
  } else {
    loadMoreBtn.style.display = "block";
  }
}

function toggleDetails(id) {
  const div = document.getElementById("details-" + id);
  div.classList.toggle("open");
}

async function getShopping(recipeId) {
  const allItems = getListValues("pantry").concat(
    getListValues("fridge"),
    getListValues("freezer"),
    getListValues("leftovers")
  );

  const res = await fetch("/shoppinglist", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({pantry: allItems, leftovers: [], recipe_id: recipeId})
  });
  const data = await res.json();

  const ul = document.getElementById("shopping-" + recipeId);
  ul.innerHTML = "";

  const req = data.shopping_list.required;
  const opt = data.shopping_list.optional;

  if (req.length === 0 && opt.length === 0) {
    ul.innerHTML = "<li>Du har allt du behöver! ✅</li>";
    return;
  }

  if (req.length > 0) {
    const header = document.createElement("li");
    header.innerHTML = "<strong>Obligatoriskt att köpa:</strong>";
    ul.appendChild(header);
    req.forEach((item, idx) => {
      const key = `recipe-${recipeId}-req-${idx}`;
      const checked = localStorage.getItem(key) === "true" ? "checked" : "";
      const doneClass = checked ? "done" : "";
      const li = document.createElement("li");
      li.className = doneClass;
      li.innerHTML = `<label><input type='checkbox' ${checked} onchange="toggleDone(this, '${key}')"> ${item}</label>`;
      ul.appendChild(li);
    });
  }

  if (opt.length > 0) {
    const header = document.createElement("li");
    header.innerHTML = "<strong>Extra ingredienser (valfritt):</strong>";
    ul.appendChild(header);
    opt.forEach((item, idx) => {
      const key = `recipe-${recipeId}-opt-${idx}`;
      const checked = localStorage.getItem(key) === "true" ? "checked" : "";
      const doneClass = checked ? "done" : "";
      const li = document.createElement("li");
      li.className = doneClass;
      li.innerHTML = `<label><input type='checkbox' ${checked} onchange="toggleDone(this, '${key}')"> ${item}</label>`;
      ul.appendChild(li);
    });
  }
}

function toggleDone(checkbox, key) {
  const label = checkbox.parentNode;
  if (checkbox.checked) {
    label.classList.add("done");
    localStorage.setItem(key, "true");
  } else {
    label.classList.remove("done");
    localStorage.setItem(key, "false");
  }
}

window.onload = function() {
  loadInputs();
};
</script>
</body>
</html>
"""



@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/match", methods=["POST"])
def match_endpoint():
    data = request.json
    pantry = data.get("pantry", [])
    leftovers = data.get("leftovers", [])
    limit = data.get("limit", 5)
    matches = match_recipes(pantry, leftovers, top_n=limit)
    total_recipes = len(RECIPES)
    return jsonify({"matches": matches, "total": total_recipes})

@app.route("/shoppinglist", methods=["POST"])
def shoppinglist_endpoint():
    data = request.json
    pantry = data.get("pantry", [])
    leftovers = data.get("leftovers", [])
    recipe_id = data.get("recipe_id")

    recipe = next((r for r in RECIPES if r["id"] == recipe_id), None)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    have = set([i.strip().lower() for i in pantry + leftovers])
    required = [i.lower() for i in recipe.get("required_ingredients", [])]
    optional = [i.lower() for i in recipe.get("optional_ingredients", [])]
    missing_required = [i for i in required if i not in have]
    missing_optional = [i for i in optional if i not in have]

    return jsonify({
        "recipe": recipe["title"],
        "shopping_list": {
            "required": missing_required,
            "optional": missing_optional
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

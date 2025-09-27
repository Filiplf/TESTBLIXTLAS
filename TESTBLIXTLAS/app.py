
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Recept (samma som innan, ej förkortat här för tydlighet)
RECIPES = [
    {"id": 1, "title": "Stekt ris med kyckling",
     "ingredients": ["ris", "kyckling", "ägg", "soja", "morot", "lök"],
     "instructions": [
         "Skär kycklingen i bitar och stek tills den är genomstekt.",
         "Tillsätt hackad lök och morot, fräs i några minuter.",
         "Knäck i ägg och rör om.",
         "Blanda i ris och soja, stek tills allt är varmt."
     ]},
        {"id": 2, "title": "Tomat- och linsgryta",
     "ingredients": ["linser", "tomat", "lök", "vitlök", "spiskummin"],
     "instructions": [
         "Fräs lök och vitlök i lite olja.",
         "Tillsätt tomat och kryddor.",
         "Häll i linser och vatten, låt koka tills linserna är mjuka."
     ]},
    {"id": 3, "title": "Omelett med grönsaker",
     "ingredients": ["ägg", "lök", "spenat", "ost", "salt", "peppar"],
     "instructions": [
         "Vispa äggen med salt och peppar.",
         "Stek lök och spenat lätt i panna.",
         "Häll över äggsmeten och toppa med ost.",
         "Stek på låg värme tills omeletten är klar."
     ]},
    {"id": 4, "title": "Pasta carbonara",
     "ingredients": ["pasta", "ägg", "grädde", "bacon", "parmesan", "svartpeppar"],
     "instructions": [
         "Koka pastan.",
         "Stek bacon knaprigt.",
         "Vispa ihop ägg, grädde och parmesan.",
         "Blanda allt med pastan och krydda med svartpeppar."
     ]},
    {"id": 5, "title": "Köttfärssås",
     "ingredients": ["spaghetti", "köttfärs", "lök", "vitlök", "tomat", "oregano"],
     "instructions": [
         "Koka spaghetti enligt anvisning.",
         "Fräs lök och vitlök i olja.",
         "Tillsätt köttfärs och bryn.",
         "Blanda i tomat och oregano, låt puttra."
     ]},
    {"id": 6, "title": "Fiskpinnar med potatis",
     "ingredients": ["fiskpinnar", "potatis", "smör", "citron", "ärtor"],
     "instructions": [
         "Koka potatis och ärtor.",
         "Stek fiskpinnarna tills de är gyllenbruna.",
         "Servera med smör och en citronklyfta."
     ]},
    {"id": 7, "title": "Grillad ostmacka",
     "ingredients": ["bröd", "ost", "smör"],
     "instructions": [
         "Bred smör på brödet.",
         "Lägg ost mellan två skivor bröd.",
         "Grilla i panna tills brödet är gyllene och osten smält."
     ]},
    {"id": 8, "title": "Kycklingsallad",
     "ingredients": ["kyckling", "sallad", "tomat", "gurka", "olivolja"],
     "instructions": [
         "Stek eller grilla kycklingen och skär i skivor.",
         "Blanda sallad, tomat och gurka i en skål.",
         "Toppa med kyckling och ringla över olivolja."
     ]},
    {"id": 9, "title": "Ugnspannkaka",
     "ingredients": ["ägg", "mjöl", "mjölk", "salt", "bacon"],
     "instructions": [
         "Vispa ihop ägg, mjöl, mjölk och salt.",
         "Häll smeten i en smord ugnsform.",
         "Lägg på bacon och grädda i ugnen tills gyllene."
     ]},
    {"id": 10, "title": "Soppa på rotfrukter",
     "ingredients": ["morot", "palsternacka", "potatis", "lök", "buljong"],
     "instructions": [
         "Skala och tärna rotfrukterna.",
         "Fräs lök i lite olja.",
         "Tillsätt rotfrukter och buljong, koka tills mjuka.",
         "Mixa soppan slät eller servera som bitar."
     ]}
]

def match_recipes(pantry, leftovers, top_n=5):
    have = set([i.strip().lower() for i in pantry + leftovers])
    results = []
    for r in RECIPES:
        reqs = [i.strip().lower() for i in r["ingredients"]]
        matched = [i for i in reqs if i in have]
        missing = [i for i in reqs if i not in have]
        num_matched = len(matched)
        total = len(reqs)
        match_score = num_matched / total if total > 0 else 0
        penalty = len(missing) * 0.05
        final_score = match_score - penalty
        results.append({
            "id": r["id"],
            "title": r["title"],
            "score": round(final_score, 3),
            "matched": matched,
            "missing": missing,
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
  <title>Food Rescue</title>
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
    li { margin: 5px 0; }
    label { cursor: pointer; }
    .done { text-decoration: line-through; color: gray; }
  </style>
</head>
<body>
  <h1>🍲 Food Rescue</h1>
  <p>Skriv in vad du har hemma:</p>

  <label>Skafferi (komma-separerat):</label><br>
  <input type="text" id="pantry" size="60"><br>

  <label>Rester (komma-separerat):</label><br>
  <input type="text" id="leftovers" size="60"><br><br>

  <button onclick="findRecipes()">Hitta recept</button>
  <button onclick="clearAll()">Rensa allt sparat</button>
  <button onclick="clearCheckboxes()">Rensa bara checkboxar</button>

  <h2>Förslag:</h2>
  <div id="results"></div>


<script>
// === LocalStorage för Skafferi & Rester ===
function saveInputs() {
  localStorage.setItem("pantry", document.getElementById("pantry").value);
  localStorage.setItem("leftovers", document.getElementById("leftovers").value);
}
function loadInputs() {
  document.getElementById("pantry").value = localStorage.getItem("pantry") || "";
  document.getElementById("leftovers").value = localStorage.getItem("leftovers") || "";
}

// === Rensa allt sparat ===
function clearAll() {
  if (confirm("Är du säker på att du vill rensa ALLT (skafferi, rester & checkboxar)?")) {
    localStorage.clear();
    location.reload();
  }
}

// === Rensa bara checkboxar ===
function clearCheckboxes() {
  if (confirm("Rensa bara checkboxar (instruktioner & inköpslista), men behåll Skafferi och Rester?")) {
    const keysToKeep = ["pantry", "leftovers"];
    const savedPantry = localStorage.getItem("pantry");
    const savedLeftovers = localStorage.getItem("leftovers");

    localStorage.clear();

    if (savedPantry !== null) localStorage.setItem("pantry", savedPantry);
    if (savedLeftovers !== null) localStorage.setItem("leftovers", savedLeftovers);

    location.reload();
  }
}


// === Hämta recept ===
async function findRecipes() {
  saveInputs(); // spara direkt vid sökning
  const pantry = document.getElementById("pantry").value.split(",").map(x=>x.trim());
  const leftovers = document.getElementById("leftovers").value.split(",").map(x=>x.trim());

  const res = await fetch("/match", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({pantry, leftovers})
  });
  const data = await res.json();

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  data.forEach(r => {
    const div = document.createElement("div");
    div.className = "recipe";

    // Instruktionslista
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
      <p class="matched">Har redan: ${r.matched.join(", ") || "–"}</p>
      <p class="missing">Saknas: ${r.missing.join(", ") || "–"}</p>
      <button onclick="toggleDetails(${r.id})">Visa detaljer</button>
      <div id="details-${r.id}" class="details">
        <h4>Instruktioner</h4>
        ${instrList}
        <h4>Inköpslista</h4>
        <ul id="shopping-${r.id}"><li>Laddar...</li></ul>
      </div>
    `;
    resultsDiv.appendChild(div);

    // Ladda inköpslista
    getShopping(r.id);
  });
}

// === Expandera sektion ===
function toggleDetails(id) {
  const div = document.getElementById("details-" + id);
  div.classList.toggle("open");
}

// === Inköpslista ===
async function getShopping(recipeId) {
  const pantry = document.getElementById("pantry").value.split(",").map(x=>x.trim());
  const leftovers = document.getElementById("leftovers").value.split(",").map(x=>x.trim());

  const res = await fetch("/shoppinglist", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({pantry, leftovers, recipe_id: recipeId})
  });
  const data = await res.json();

  const ul = document.getElementById("shopping-" + recipeId);
  ul.innerHTML = "";
  data.shopping_list.forEach((item, idx) => {
    const key = "recipe-" + recipeId + "-shop-" + idx;
    const checked = localStorage.getItem(key) === "true" ? "checked" : "";
    const doneClass = checked ? "done" : "";
    const li = document.createElement("li");
    li.className = doneClass;
    li.innerHTML = `<label><input type='checkbox' ${checked} onchange="toggleDone(this, '${key}')"> ${item}</label>`;
    ul.appendChild(li);
  });
}

// === Överstrykning + spara ===
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

// === Init ===
window.onload = function() {
  loadInputs();
  document.getElementById("pantry").addEventListener("input", saveInputs);
  document.getElementById("leftovers").addEventListener("input", saveInputs);
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
    matches = match_recipes(pantry, leftovers)
    return jsonify(matches)

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
    missing = [i for i in recipe["ingredients"] if i.lower() not in have]
    return jsonify({"recipe": recipe["title"], "shopping_list": missing})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



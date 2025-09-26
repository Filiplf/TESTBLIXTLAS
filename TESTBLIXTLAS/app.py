from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Enkel "databas" med 10 recept
RECIPES = [
    {"id": 1, "title": "Stekt ris med kyckling",
     "ingredients": ["kokt ris", "kyckling", "ägg", "soja", "morot", "lök"]},
    {"id": 2, "title": "Tomat- och linsgryta",
     "ingredients": ["linser", "tomat", "lök", "vitlök", "spiskummin"]},
    {"id": 3, "title": "Omelett med grönsaker",
     "ingredients": ["ägg", "lök", "spenat", "ost", "salt", "peppar"]},
    {"id": 4, "title": "Pasta carbonara",
     "ingredients": ["pasta", "ägg", "grädde", "bacon", "parmesan", "svartpeppar"]},
    {"id": 5, "title": "Köttfärssås",
     "ingredients": ["spaghetti", "köttfärs", "lök", "vitlök", "tomat", "oregano"]},
    {"id": 6, "title": "Fiskpinnar med potatis",
     "ingredients": ["fiskpinnar", "potatis", "smör", "citron", "ärtor"]},
    {"id": 7, "title": "Grillad ostmacka",
     "ingredients": ["bröd", "ost", "smör"]},
    {"id": 8, "title": "Kycklingsallad",
     "ingredients": ["kyckling", "sallad", "tomat", "gurka", "olivolja"]},
    {"id": 9, "title": "Ugnspannkaka",
     "ingredients": ["ägg", "mjöl", "mjölk", "salt", "bacon"]},
    {"id": 10, "title": "Soppa på rotfrukter",
     "ingredients": ["morot", "palsternacka", "potatis", "lök", "buljong"]}
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
            "missing": missing
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]

# ---- HTML + JS direkt i koden ----
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
  </style>
</head>
<body>
  <h1>🍲 Food Rescue</h1>
  <p>Skriv in vad du har hemma:</p>

  <label>Skafferi (komma-separerat):</label><br>
  <input type="text" id="pantry" size="60" value="lök, soja"><br>

  <label>Rester (komma-separerat):</label><br>
  <input type="text" id="leftovers" size="60" value="kokt ris, kyckling"><br><br>

  <button onclick="findRecipes()">Hitta recept</button>

  <h2>Förslag:</h2>
  <div id="results"></div>

  <h2>Inköpslista:</h2>
  <ul id="shopping"></ul>

<script>
async function findRecipes() {
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
    div.innerHTML = `
      <h3>${r.title} (score ${r.score})</h3>
      <p class="matched">Har redan: ${r.matched.join(", ") || "–"}</p>
      <p class="missing">Saknas: ${r.missing.join(", ") || "–"}</p>
      <button onclick="getShopping(${r.id})">Få inköpslista</button>
    `;
    resultsDiv.appendChild(div);
  });
}

async function getShopping(recipeId) {
  const pantry = document.getElementById("pantry").value.split(",").map(x=>x.trim());
  const leftovers = document.getElementById("leftovers").value.split(",").map(x=>x.trim());

  const res = await fetch("/shoppinglist", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({pantry, leftovers, recipe_id: recipeId})
  });
  const data = await res.json();

  const ul = document.getElementById("shopping");
  ul.innerHTML = "";
  data.shopping_list.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
}
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
    app.run(host="localhost", debug=True)

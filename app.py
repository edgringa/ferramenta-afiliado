<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎛️ EuroAffiliate Ultimate</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .form-group { display: flex; gap: 15px; margin-bottom: 20px; }
        input, select, button { padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
        input { flex: 2; }
        select { flex: 1; }
        button { background-color: #3498db; color: white; border: none; cursor: pointer; font-weight: bold; transition: 0.2s; }
        button:hover { background-color: #2980b9; }
        .results-box { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .column { background: #f9f9f9; padding: 20px; border-radius: 6px; border-left: 4px solid #3498db; min-height: 100px; }
        .keyword-item { padding: 8px 0; border-bottom: 1px solid #eee; font-weight: 500; }
    </style>
</head>
<body>

<div class="container">
    <h1>🎛️ EuroAffiliate Ultimate - Extrator de Palavras-Chave de Ouro</h1>
    
    <div class="form-group">
        <input type="text" id="produto" placeholder="Digite o produto ou nicho base (Ex: Nourix, coffee machine)">
        <select id="mercado">
            <option value="en">Reino Unido / Global (EN)</option>
            <option value="fr" selected>França (FR)</option>
            <option value="es">Espanha (ES)</option>
            <option value="de">Alemanha (DE)</option>
            <option value="it">Itália (IT)</option>
        </select>
        <button onclick="buscarPalavras()">Gerar Inteligência</button>
    </div>

    <div class="results-box">
        <div>
            <h3>🎯 Termos com Intenção de Compra</h3>
            <div id="col-comercial" class="column">Digite um termo para começar...</div>
        </div>
        <div>
            <h3>❓ Dúvidas e Variações</h3>
            <div id="col-duvidas" class="column">Digite um termo para começar...</div>
        </div>
    </div>
</div>

<script>
async function consultarGoogle(termo, mercado) {
    // URL real completa da API pública do Google Autocomplete para navegadores
    const urlGoogle = `https://google.com{mercado}&q=${encodeURIComponent(termo)}`;
    
    try {
        // Usa o proxy AllOrigins para injetar e buscar os dados de forma 100% limpa no seu próprio navegador
        const resposta = await fetch(`https://allorigins.win{encodeURIComponent(urlGoogle)}`);
        if (resposta.ok) {
            const json = await resposta.json();
            const dados = JSON.parse(json.contents);
            return dados[1] || []; // Retorna o array de sugestões textuais reais
        }
    } catch (e) {
        console.error("Erro técnico na requisição:", e);
    }
    return [];
}

async function buscarPalavras() {
    const produto = document.getElementById('produto').value.trim();
    const mercado = document.getElementById('mercado').value;
    const colComercial = document.getElementById('col-comercial');
    const colDuvidas = document.getElementById('col-duvidas');

    if (!produto) {
        alert("Por favor, digite o nome de um produto!");
        return;
    }

    colComercial.innerHTML = "Minerando o mercado europeu...";
    colDuvidas.innerHTML = "Processando variações...";

    const modificadores = {
        "en": { comp: ["best", "review", "buy", "price"], duv: ["how to", "is it safe", "side effects"] },
        "fr": { comp: ["meilleur", "avis", "acheter", "prix"], duv: ["comment utiliser", "danger", "effets secondaires"] },
        "es": { comp: ["mejor", "opiniones", "comprar", "precio"], duv: ["como usar", "funciona", "contraindicaciones"] },
        "de": { comp: ["beste", "test", "kaufen", "preis"], duv: ["wie funktioniert", "erfahrungen", "nebenwirkungen"] },
        "it": { comp: ["migliore", "recensione", "comprare", "prezzo"], duv: ["come assumere", "funziona", "effetti collaterali"] }
    };

    let resultadosComerciais = new Set();
    let resultadosDuvidas = new Set();

    // 1. Busca Termo Puro
    const puras = await consultarGoogle(produto, mercado);
    puras.forEach(t => resultadosComerciais.add(t));

    // 2. Busca Termos Comerciais
    for (let mod of modificadores[mercado].comp) {
        const r1 = await consultarGoogle(`${produto} ${mod}`, mercado);
        const r2 = await consultarGoogle(`${mod} ${produto}`, mercado);
        r1.forEach(t => resultadosComerciais.add(t));
        r2.forEach(t => resultadosComerciais.add(t));
    }

    // 3. Busca Dúvidas
    for (let mod of modificadores[mercado].duv) {
        const r1 = await consultarGoogle(`${produto} ${mod}`, mercado);
        const r2 = await consultarGoogle(`${mod} ${produto}`, mercado);
        r1.forEach(t => resultadosDuvidas.add(t));
        r2.forEach(t => resultadosDuvidas.add(t));
    }

    colComercial.innerHTML = "";
    colDuvidas.innerHTML = "";

    if (resultadosComerciais.size === 0 && resultadosDuvidas.size === 0) {
        colComercial.innerHTML = "Nenhum dado retornado. Tente novamente.";
        colDuvidas.innerHTML = "Nenhum dado retornado.";
        return;
    }

    Array.from(resultadosComerciais).sort().forEach(termo => {
        colComercial.innerHTML += `<div class="keyword-item">🎯 ${termo}</div>`;
    });

    Array.from(resultadosDuvidas).sort().forEach(termo => {
        colDuvidas.innerHTML += `<div class="keyword-item">💡 ${termo}</div>`;
    });
}
</script>
</body>
</html>

# Dashboard RH — Protótipo 1

Projeto Streamlit: dashboard de Recursos Humanos (protótipo). Contém filtros interativos, KPIs, gráficos Plotly e opção de download dos dados filtrados.

## Estrutura
- `app.py` — aplicação Streamlit principal
- `.streamlit/config.toml` — tema (dark-clean)
- `BaseFuncionarios.xlsx` — base de exemplo
- `requirements.txt` — dependências

---

## Como publicar no GitHub (passo a passo)

### Opção A — usando o GitHub CLI (`gh`)
1. Instale e autentique o `gh` (docs: https://cli.github.com/).
2. No terminal, dentro da pasta do projeto:
```bash
git init
git add .
git commit -m "Initial commit - Dashboard RH Protótipo 1"
# substitua <nome-do-repo> pelo nome desejado
gh repo create <nome-do-repo> --public --source=. --remote=origin --push
```
O `gh` cria o repositório no GitHub e faz o push automaticamente.

### Opção B — via site do GitHub (manual)
1. Crie um novo repositório no GitHub (botão "New repository"). Não marque para criar README/License (para evitar conflitos).
2. No terminal, dentro da pasta do projeto:
```bash
git init
git add .
git commit -m "Initial commit - Dashboard RH Protótipo 1"
git branch -M main
# substitua <URL_DO_REPO> pela URL que o GitHub mostrar (ex: https://github.com/usuario/repo.git)
git remote add origin <URL_DO_REPO>
git push -u origin main
```

---

## Como clonar no Desktop e abrir no VS Code
No computador onde quer trabalhar (desktop ou laptop), rode:
```bash
# clonar
git clone https://github.com/<seu-usuario>/<seu-repo>.git
cd <seu-repo>

# abrir no VS Code
code .
```

> No VS Code você pode usar o terminal integrado (Ctrl+`) para rodar os próximos comandos.

---

## Como rodar localmente (Windows / macOS / Linux)

### Windows (PowerShell)
```powershell
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Se o PowerShell bloquear scripts, rode (como administrador) apenas uma vez:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Dicas e ajustes
- Se preferir tema claro, edite `.streamlit/config.toml` substituindo `base = "dark"` por `base = "light"` e ajustando as cores.  
- Recomendo criar um arquivo `.env` para variáveis sensíveis (não incluído).  
- Para deploy em serviços (Streamlit Cloud, Heroku, etc.) crie `Procfile` e configure variáveis de ambiente conforme instruções do serviço.

---

Se quiser, eu posso **criar o repositório no seu GitHub** automaticamente usando o `gh` CLI — você precisará rodar os comandos locais no seu PC ou me autorizar se quiser instruções passo a passo.


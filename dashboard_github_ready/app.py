import os
from datetime import datetime, date
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- Page config ----------------
st.set_page_config(page_title="Dashboard RH - Protótipo 1", page_icon="📊", layout="wide")

st.title("📊 Dashboard de RH — Protótipo 1")
st.markdown("Uma versão refinada do dashboard com filtros interativos, KPIs e gráficos responsivos.")

# ---------------- Paths ----------------
EXCEL = "BaseFuncionarios.xlsx"

# ---------------- Helpers ----------------
@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"Arquivo de dados não encontrado: {path}")
        return pd.DataFrame()
    df = pd.read_excel(path, engine='openpyxl', parse_dates=True)
    # normalizar nomes de colunas (remove espaços extras)
    df.columns = [c.strip() for c in df.columns]
    # garantir colunas importantes
    expected_cols = ['Nome', 'Setor', 'Cargo', 'Status', 'Salario', 'Sexo',
                     'Data de Nascimento', 'Data de Contratacao', 'Data de Demissao']
    for c in expected_cols:
        if c not in df.columns:
            df[c] = np.nan
    # calcular idade
    def calc_age(born):
        try:
            if pd.isna(born):
                return np.nan
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        except Exception:
            return np.nan
    df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'], errors='coerce')
    df['Idade'] = df['Data de Nascimento'].apply(calc_age).astype('Int64')
    # Salario como numérico
    df['Salario'] = pd.to_numeric(df['Salario'], errors='coerce').fillna(0)
    # Status sempre como string
    df['Status'] = df['Status'].fillna('').astype(str)
    return df

df = load_data(EXCEL)

# ---------------- Sidebar - filtros ----------------
st.sidebar.header("⚙️ Filtros")
if df.empty:
    st.sidebar.warning("Base de dados vazia ou não carregada. Coloque 'BaseFuncionarios.xlsx' na mesma pasta.")
else:
    setores = st.sidebar.multiselect("Setores", options=sorted(df['Setor'].dropna().unique()),
                                     default=sorted(df['Setor'].dropna().unique()))
    cargos = st.sidebar.multiselect("Cargos", options=sorted(df['Cargo'].dropna().unique()),
                                    default=sorted(df['Cargo'].dropna().unique()))
    status = st.sidebar.multiselect("Status", options=sorted(df['Status'].dropna().unique()),
                                    default=sorted(df['Status'].dropna().unique()))
    salario_min = float(df['Salario'].min())
    salario_max = float(df['Salario'].max())
    salario_range = st.sidebar.slider("Faixa salarial (R$)",
                                      min_value=0.0,
                                      max_value=salario_max if salario_max > 0 else 10000.0,
                                      value=(salario_min, salario_max if salario_max > 0 else 10000.0),
                                      step=100.0, format="%.0f")
    idade_min = int(df['Idade'].min()) if not df['Idade'].isna().all() else 18
    idade_max = int(df['Idade'].max()) if not df['Idade'].isna().all() else 65
    idade_range = st.sidebar.slider("Faixa de Idade",
                                    min_value=idade_min, max_value=idade_max,
                                    value=(idade_min, idade_max))

    # aplicar filtros
    filtered = df.copy()
    filtered = filtered[filtered['Setor'].isin(setores)]
    filtered = filtered[filtered['Cargo'].isin(cargos)]
    filtered = filtered[filtered['Status'].isin(status)]
    filtered = filtered[(filtered['Salario'] >= salario_range[0]) & (filtered['Salario'] <= salario_range[1])]
    filtered = filtered[(filtered['Idade'] >= idade_range[0]) & (filtered['Idade'] <= idade_range[1])]

    # ---------------- KPIs ----------------
    st.markdown("---")
    k1, k2, k3, k4, k5 = st.columns([1.6,1.2,1.2,1.4,1.6])
    k1.metric("👥 Total Funcionários", f"{len(filtered):,}")

    # tratar status como string minúscula
    if 'Status' in filtered:
        ativos = filtered[filtered['Status'].str.lower() == 'ativo'].shape[0]
        desligados = filtered[filtered['Status'].str.lower() == 'desligado'].shape[0]
    else:
        ativos, desligados = 0, 0

    k2.metric("✅ Ativos", f"{ativos:,}")
    k3.metric("❌ Desligados", f"{desligados:,}")
    avg_salario = filtered['Salario'].mean() if not filtered.empty else 0
    k4.metric("💰 Média Salarial", f"R$ {avg_salario:,.2f}")
    median_sal = filtered['Salario'].median() if not filtered.empty else 0
    k5.metric("📈 Mediana Salarial", f"R$ {median_sal:,.2f}")

    st.markdown("---")

    # ---------------- Layout de gráficos ----------------
    c1, c2 = st.columns((2,1))
    with c1:
        st.subheader("Salário médio por Setor")
        if filtered.empty:
            st.info("Sem dados para exibir. Ajuste os filtros.")
        else:
            grp = filtered.groupby('Setor', as_index=False)['Salario'].mean().sort_values('Salario', ascending=False)
            fig = px.bar(grp, x='Setor', y='Salario', text=grp['Salario'].round(0),
                         title="", labels={'Salario':'Salário médio (R$)'}, height=420)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Distribuição Salarial por Cargo")
        if not filtered.empty:
            fig2 = px.box(filtered, x='Cargo', y='Salario', points='outliers', title="", height=420)
            st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.subheader("Composição por Status")
        if filtered.empty:
            st.info("Sem dados para exibir.")
        else:
            pie = filtered['Status'].value_counts().rename_axis('Status').reset_index(name='count')
            fig3 = px.pie(pie, names='Status', values='count', title="", hole=0.4, height=350)
            st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Histograma de Idade")
        if not filtered.empty:
            fig4 = px.histogram(filtered, x='Idade', nbins=15, title="", height=300)
            st.plotly_chart(fig4, use_container_width=True)

    # ---------------- Dados detalhados e download ----------------
    st.markdown('---')
    with st.expander('📑 Dados filtrados (visualizar / baixar)'):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(label='⬇️ Baixar CSV dos dados filtrados',
                           data=csv,
                           file_name='dados_filtrados.csv',
                           mime='text/csv')

    st.markdown('---')
    st.caption('Protótipo 1 • Dashboard RH • Desenvolvido para você — place holder footer')

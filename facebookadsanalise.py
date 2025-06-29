"""
Análise de Performance de Campanhas do Facebook Ads
===================================================

Este script analisa dados de campanhas publicitárias do Facebook, 
calculando métricas de engajamento e criando visualizações por 
gênero e faixa etária.

Autor: Rafael
Data: Junho 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import warnings

# Configurações gerais
warnings.filterwarnings('ignore')
plt.style.use('default')

# Constantes
ARQUIVO_DADOS = "data.csv"


def carregar_dados(caminho_arquivo):
    """
    Carrega os dados do arquivo CSV contendo informações das campanhas.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV

    Returns:
        pd.DataFrame: DataFrame com os dados carregados
    """
    try:
        dados = pd.read_csv(caminho_arquivo)
        print(
            f"✅ Dados carregados com sucesso! Total de registros: {len(dados)}")
        return dados
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{caminho_arquivo}' não encontrado!")
        return None
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None


# Carregamento inicial dos dados
print("🔄 Carregando dados das campanhas do Facebook Ads...")
dados = carregar_dados(ARQUIVO_DADOS)

# Inicializar variável de métricas
metricas_demograficas = None


def tratar_dados(dados_brutos):
    """
    Realiza o tratamento e limpeza dos dados das campanhas.

    Remove colunas desnecessárias, trata valores ausentes e 
    codifica variáveis categóricas.

    Args:
        dados_brutos (pd.DataFrame): DataFrame com dados originais

    Returns:
        pd.DataFrame: DataFrame tratado e limpo
    """
    if dados_brutos is None:
        return None

    print("🧹 Iniciando tratamento dos dados...")

    # Criar uma cópia para não modificar os dados originais
    dados_tratados = dados_brutos.copy()

    # Remover colunas que não serão utilizadas na análise
    colunas_remover = ["reporting_start", "reporting_end", "fb_campaign_id"]
    dados_tratados.drop(columns=colunas_remover, inplace=True)
    print(f"   • Removidas colunas: {', '.join(colunas_remover)}")

    # Remover registros com valores ausentes
    registros_antes = len(dados_tratados)
    dados_tratados.dropna(inplace=True)
    registros_depois = len(dados_tratados)
    print(
        f"   • Removidos {registros_antes - registros_depois} registros com valores ausentes")

    # Codificar gênero para análise numérica (Feminino=0, Masculino=1)
    encoder = LabelEncoder()
    dados_tratados['gender'] = encoder.fit_transform(dados_tratados['gender'])
    print("   • Gênero codificado: Feminino=0, Masculino=1")

    print("✅ Tratamento de dados concluído!")
    return dados_tratados


# Aplicar tratamento aos dados
if dados is not None:
    dados = tratar_dados(dados)

# ====================================================================
# CÁLCULO DE MÉTRICAS DE PERFORMANCE
# ====================================================================


def calcular_metricas_demograficas(dados):
    """
    Calcula métricas de performance das campanhas agrupadas por demografia.

    Computa a taxa de engajamento (CTR - Click Through Rate) e agrupa
    os dados por gênero para análise de performance.

    Args:
        dados (pd.DataFrame): DataFrame com dados tratados das campanhas

    Returns:
        pd.DataFrame: DataFrame com métricas agrupadas por gênero
    """
    if dados is None:
        return None

    print("📊 Calculando métricas de performance...")

    # Calcular taxa de engajamento (CTR - Click Through Rate)
    # CTR = (Cliques / Impressões) × 100
    dados["Engajamento"] = (dados["clicks"] / dados["impressions"]) * 100
    print("   • Taxa de engajamento (CTR) calculada")

    # Agrupar dados por gênero e calcular métricas agregadas
    metricas_demograficas = dados.groupby(["gender"]).agg({
        "impressions": "sum",           # Total de impressões por gênero
        "clicks": "sum",               # Total de cliques por gênero
        "Engajamento": "mean",         # Taxa média de engajamento
        "total_conversion": "sum",     # Total de conversões
        "spent": "sum"                 # Total gasto em publicidade
    }).reset_index()

    # Calcular métricas adicionais
    metricas_demograficas["CPC"] = (
        metricas_demograficas["spent"] / metricas_demograficas["clicks"]
    ).round(2)  # Custo por Clique

    metricas_demograficas["CPM"] = (
        (metricas_demograficas["spent"] /
         metricas_demograficas["impressions"]) * 1000
    ).round(2)  # Custo por Mil Impressões

    print("✅ Métricas demográficas calculadas!")
    return metricas_demograficas


# Calcular métricas demográficas
if dados is not None:
    metricas_demograficas = calcular_metricas_demograficas(dados)


# ====================================================================
# VISUALIZAÇÕES E ANÁLISES
# ====================================================================

def visualizar_engajamento_por_genero(metricas_demograficas):
    """
    Cria um gráfico de barras mostrando o engajamento médio por gênero.

    Args:
        metricas_demograficas (pd.DataFrame): DataFrame com métricas por gênero
    """
    if metricas_demograficas is None:
        print("❌ Não há dados para visualizar!")
        return

    print("📈 Gerando gráfico de engajamento por gênero...")

    # Preparar dados para visualização
    generos = metricas_demograficas['gender'].astype(str).tolist()
    engajamento = metricas_demograficas['Engajamento'].tolist()

    # Definir cores atrativas para o gráfico
    # Rosa para Feminino, Verde-azulado para Masculino
    cores_barras = ['#FF6B9D', '#4ECDC4']

    # Criar figura com tamanho adequado
    plt.figure(figsize=(10, 6))
    barras = plt.bar(generos, engajamento, color=cores_barras,
                     alpha=0.8, edgecolor='black', linewidth=0.5)

    # Personalização avançada do gráfico
    plt.title('📊 Taxa de Engajamento por Gênero\n(Click Through Rate - CTR)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('👥 Gênero do Público', fontsize=12, fontweight='bold')
    plt.ylabel('📈 Taxa Média de Engajamento (%)',
               fontsize=12, fontweight='bold')

    # Personalizar rótulos do eixo X
    plt.xticks(ticks=[0, 1], labels=['👩 Feminino', '👨 Masculino'], fontsize=11)

    # Adicionar valores nas barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + 0.01,
                 f'{altura:.2f}%', ha='center', va='bottom', fontweight='bold')

    # Melhorar aparência geral
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Exibir estatísticas no console
    print("📋 Resumo das métricas por gênero:")
    for _, linha in metricas_demograficas.iterrows():
        genero_nome = "Feminino" if linha['gender'] == 0 else "Masculino"
        print(
            f"   • {genero_nome}: {linha['Engajamento']:.2f}% de engajamento")

    plt.show()


def visualizar_engajamento_por_idade(dados):
    """
    Cria um gráfico de linha mostrando o engajamento médio por faixa etária.

    Args:
        dados (pd.DataFrame): DataFrame com dados das campanhas
    """
    if dados is None:
        print("❌ Não há dados para visualizar!")
        return

    print("📈 Gerando gráfico de engajamento por faixa etária...")

    # Calcular engajamento médio por faixa etária
    engajamento_por_idade = dados.groupby(
        "age")["Engajamento"].mean().sort_index()

    # Criar gráfico de linha elegante
    plt.figure(figsize=(12, 7))
    plt.plot(engajamento_por_idade.index, engajamento_por_idade.values,
             marker="o", linestyle="-", color="#2E86AB", linewidth=3,
             markersize=8, markerfacecolor="#F24236", markeredgecolor="white",
             markeredgewidth=2)

    # Personalização avançada
    plt.title('📊 Taxa de Engajamento por Faixa Etária\n'
              'Análise de Performance Demográfica',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('👥 Faixa Etária', fontsize=12, fontweight='bold')
    plt.ylabel('📈 Taxa Média de Engajamento (%)',
               fontsize=12, fontweight='bold')

    # Melhorar aparência
    plt.grid(alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')

    # Adicionar valores nos pontos
    for idade, engaj in engajamento_por_idade.items():
        plt.annotate(f'{engaj:.2f}%',
                     (idade, engaj),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center',
                     fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

    plt.tight_layout()

    # Exibir estatísticas no console
    print("📋 Resumo do engajamento por faixa etária:")
    for idade, engajamento in engajamento_por_idade.items():
        print(f"   • {idade}: {engajamento:.2f}% de engajamento")

    plt.show()


def gerar_resumo_executivo(dados, metricas_demograficas):
    """
    Gera um resumo executivo com as principais métricas da análise.

    Args:
        dados (pd.DataFrame): DataFrame com dados das campanhas
        metricas_demograficas (pd.DataFrame): DataFrame com métricas por gênero
    """
    if dados is None or metricas_demograficas is None:
        return

    print("\n" + "="*60)
    print("📊 RESUMO EXECUTIVO - ANÁLISE DE CAMPANHAS FACEBOOK ADS")
    print("="*60)

    # Métricas gerais
    total_impressoes = dados['impressions'].sum()
    total_cliques = dados['clicks'].sum()
    total_gastos = dados['spent'].sum()
    total_conversoes = dados['total_conversion'].sum()
    ctr_geral = (total_cliques / total_impressoes) * 100

    print("\n📈 MÉTRICAS GERAIS:")
    print(f"   • Total de Impressões: {total_impressoes:,}")
    print(f"   • Total de Cliques: {total_cliques:,}")
    print(f"   • Taxa de Engajamento Geral: {ctr_geral:.2f}%")
    print(f"   • Total Investido: R$ {total_gastos:,.2f}")
    print(f"   • Total de Conversões: {total_conversoes:,}")
    print(f"   • Custo por Conversão: R$ {total_gastos/total_conversoes:.2f}")

    # Análise por gênero
    print("\n👥 ANÁLISE POR GÊNERO:")
    melhor_genero = metricas_demograficas.loc[metricas_demograficas['Engajamento'].idxmax(
    )]
    genero_nome = "Feminino" if melhor_genero['gender'] == 0 else "Masculino"

    print(f"   • Melhor Performance: {genero_nome}")
    print(f"   • Taxa de Engajamento: {melhor_genero['Engajamento']:.2f}%")
    print(f"   • Total de Cliques: {melhor_genero['clicks']:,}")
    print(f"   • CPC (Custo por Clique): R$ {melhor_genero['CPC']:.2f}")

    # Análise por faixa etária
    engajamento_por_idade = dados.groupby("age")["Engajamento"].mean()
    melhor_idade = engajamento_por_idade.idxmax()
    melhor_engajamento_idade = engajamento_por_idade.max()

    print("\n🎯 ANÁLISE POR FAIXA ETÁRIA:")
    print(f"   • Melhor Faixa Etária: {melhor_idade}")
    print(f"   • Taxa de Engajamento: {melhor_engajamento_idade:.2f}%")

    print("\n" + "="*60)


def main():
    """
    Função principal que executa toda a análise de dados.
    """
    print("🚀 INICIANDO ANÁLISE DE CAMPANHAS FACEBOOK ADS")
    print("="*60)

    # Verificar se os dados foram carregados corretamente
    if dados is None:
        print("❌ Não foi possível prosseguir devido a problemas no carregamento dos dados.")
        return

    if metricas_demograficas is None:
        print("❌ Não foi possível calcular as métricas demográficas.")
        return

    # Executar análises
    try:
        # Gerar resumo executivo
        gerar_resumo_executivo(dados, metricas_demograficas)

        # Gerar visualizações
        print("\n🎨 Gerando visualizações...")
        visualizar_engajamento_por_genero(metricas_demograficas)
        visualizar_engajamento_por_idade(dados)

        print("\n🎉 Análise concluída com sucesso!")
        print("💡 Dica: Use os insights gerados para otimizar suas próximas campanhas!")

    except Exception as e:
        print(f"❌ Erro durante a execução da análise: {e}")


# ====================================================================
# EXECUÇÃO DO PROGRAMA
# ====================================================================

if __name__ == "__main__":
    main()

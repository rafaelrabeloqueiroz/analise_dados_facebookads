# 📊 Análise de Performance - Facebook Ads

## 🎯 Sobre o Projeto

Este projeto realiza uma análise completa de campanhas publicitárias do Facebook Ads, fornecendo insights valiosos sobre performance demográfica e métricas de engajamento.

## 🚀 Funcionalidades

- **📈 Análise de Engajamento**: Calcula CTR (Click Through Rate) por gênero e faixa etária
- **👥 Segmentação Demográfica**: Análise detalhada por gênero (Masculino/Feminino)
- **🎯 Análise Etária**: Performance por diferentes faixas etárias
- **💰 Métricas Financeiras**: CPC (Custo por Clique) e CPM (Custo por Mil Impressões)
- **📊 Visualizações Interativas**: Gráficos elegantes e informativos
- **📋 Resumo Executivo**: Relatório com principais insights

## 📦 Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Como Usar

1. **Prepare seus dados**: Certifique-se de que o arquivo `data.csv` está na pasta do projeto
2. **Execute a análise:**
   ```bash
   python facebookadsanalise.py
   ```

## 📊 Estrutura dos Dados

O arquivo CSV deve conter as seguintes colunas:
- `ad_id`: ID do anúncio
- `age`: Faixa etária do público
- `gender`: Gênero (M/F)
- `impressions`: Número de impressões
- `clicks`: Número de cliques
- `spent`: Valor gasto
- `total_conversion`: Total de conversões

## 📈 Métricas Calculadas

- **CTR (Click Through Rate)**: (Cliques ÷ Impressões) × 100
- **CPC (Custo por Clique)**: Valor Gasto ÷ Cliques
- **CPM (Custo por Mil Impressões)**: (Valor Gasto ÷ Impressões) × 1000
- **Taxa de Conversão**: Conversões ÷ Cliques

## 📊 Visualizações Geradas

1. **Gráfico de Barras**: Engajamento por Gênero
2. **Gráfico de Linha**: Engajamento por Faixa Etária
3. **Resumo Executivo**: Principais métricas e insights

## 🎨 Características do Código

- ✅ **Código Limpo**: Estrutura organizada e legível
- 📝 **Documentação Completa**: Docstrings em todas as funções
- 🛡️ **Tratamento de Erros**: Validações e mensagens informativas
- 🎯 **Boas Práticas**: Seguindo padrões Python (PEP 8)
- 📊 **Visualizações Profissionais**: Gráficos com design moderno

## 🔍 Exemplo de Saída

```
📊 RESUMO EXECUTIVO - ANÁLISE DE CAMPANHAS FACEBOOK ADS
============================================================

📈 MÉTRICAS GERAIS:
   • Total de Impressões: 1,234,567
   • Total de Cliques: 12,345
   • Taxa de Engajamento Geral: 1.00%
   • Total Investido: R$ 5,678.90
   • Total de Conversões: 234

👥 ANÁLISE POR GÊNERO:
   • Melhor Performance: Feminino
   • Taxa de Engajamento: 1.25%
   • CPC (Custo por Clique): R$ 0.46

🎯 ANÁLISE POR FAIXA ETÁRIA:
   • Melhor Faixa Etária: 25-34
   • Taxa de Engajamento: 1.35%
```

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto é de uso livre para fins educacionais e comerciais.

---

**Desenvolvido com ❤️ para otimizar suas campanhas do Facebook Ads!**

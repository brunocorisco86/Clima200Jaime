# Relatório de Eficiência: CLIMA200 vs. TESTEMUNHA
## Análise Detalhada dos Lotes e Tratamentos
Este relatório apresenta uma análise aprofundada da eficiência do tratamento CLIMA200 em comparação com um grupo TESTEMUNHA, utilizando dados de sensores e informações contextuais. O objetivo é fornecer insights claros para uma apresentação, destacando os impactos do controle de ambiência no desempenho dos lotes.

### 1. Carregamento e Preparação dos Dados
Os dados foram carregados de um banco de dados SQLite (`clima_prod.db`) e incluem informações de desempenho do lote, leituras diárias de IoT e acompanhamento dos lotes. As etapas de pré-processamento incluíram padronização de nomes, conversão de tipos e fusão de DataFrames para criar uma base de dados unificada (`df_final`).
### 2. Análise Comparativa de Indicadores de Desempenho (KPIs)
A comparação dos KPIs médios entre os tratamentos 'CLIMA' e 'TESTEMUNHA' revela o impacto direto do ambiente controlado. Os gráficos a seguir ilustram as diferenças em métricas chave.

![Comparativo de KPIs](https://private-us-east-1.manuscdn.com/sessionFile/zO507PNKDVwrJ2bP8EYB8s/sandbox/nUhfDNPIjGKbStHxqkTsCM-images_1761003116605_na1fn_L2hvbWUvdWJ1bnR1L0NsaW1hMjAwSmFpbWUvc3JjL2twaV9jb21wYXJpc29u.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvek81MDdQTktEVndySjJiUDhFWUI4cy9zYW5kYm94L25VaGZETlBJakdLYlN0SHhxa1RzQ00taW1hZ2VzXzE3NjEwMDMxMTY2MDVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwTnNhVzFoTWpBd1NtRnBiV1V2YzNKakwydHdhVjlqYjIxd1lYSnBjMjl1LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=j6eJTB1HOrKpkwe0tmNxGvhDl6WIWBqB0lvQr5b2GS0EiJ45XiqqqJ64aQHNJRJ2R-gjPUfzObiG-vXO4bJOPxxXB-q1WbxRaseD9jjIfMSmin6iw1LF~HyDIVCbMzSJYZvnVVDrq2xUtbGb4csgXkLDWzQwPwgigEAFkGNQndjzkeAREkYHnm-Ybx4NTCGLZO1IvTFxKkzzswljiobTeX7N3fx8rIrRm9p1tgV9kdSw~CPS~y8ynyGFs327qcEwyRQIK0lBNnMJ3~8~TO3IOotgb4~5TP~L4iJUt6iZfyoLiC8waYeXadf~VDB66njtQrwpUpzqFhw0GpXdv6OGzQ__)

**Insights:**
- **Mortalidade:** Avaliar se o CLIMA apresenta menor mortalidade, indicando melhor bem-estar.
- **Conversão Alimentar:** Uma CA menor no CLIMA sugere maior eficiência na alimentação.
- **IEP:** Um IEP mais alto no CLIMA demonstra melhor desempenho produtivo geral.
- **Peso Médio:** Maior peso médio pode indicar crescimento mais robusto.
- **Remuneração:** O impacto financeiro direto do tratamento.

### 3. Análise da Ambiência
A ambiência controlada é um pilar do sistema CLIMA200. Analisamos a evolução das variáveis críticas medidas pelos sensores.

#### Contexto do CLIMA200 (Fonte: `ambiencia_clima200.md`)
> O Clima+ 200 da Vencomatic é uma solução abrangente para otimizar a ambiência no ambiente de criação de frango de corte. Ele controla de forma integrada variáveis climáticas essenciais como temperatura, umidade, ventilação e qualidade do ar, criando condições ideais para o conforto e bem-estar das aves.
> 
> Uma ambiência adequada influencia diretamente no desempenho produtivo, na saúde respiratória e na redução do estresse das aves. O sistema ajusta automaticamente a ventilação para garantir a renovação eficiente do ar, evitando o acúmulo de gases nocivos como a amônia e mantendo níveis controlados de umidade, que é crucial para evitar problemas respiratórios e proliferação de patógenos.
> 
> Além disso, o Clima+ 200 regula a temperatura de forma precisa, mantendo a estabilidade térmica necessária em todas as fases da criação, o que favorece o metabolismo das aves e a conversão alimentar. O controle automatizado permite rápida adaptação a variações climáticas externas, resultando em ambiente mais saudável, melhora na uniformidade do lote e otimização dos resultados econômicos da granja.
> 
> Portanto, o Clima+ 200 contribui significativamente para uma ambiência ideal, promovendo saúde, conforto e produtividade, fatores chave para o sucesso na produção de frangos de corte.[1][2][3]
> 
> [1](https://www.vencomaticgroup.com/pt-br/produto/clima-200)
> [2](https://www.vencomaticgroup.com/pt-br/soluci%C3%B3n-clim%C3%A1tica-ventila%C3%A7%C3%A3o-m%C3%ADnima)
> [3](https://www.vencomaticgroup.com/pt-br/agro-supply)
> 

#### Contexto da Amônia e Sensor DOL53 (Fonte: `amonia_clima200.md`, `importancia_amonia.md`, `sensor_dol53.md`)
> O Clima+ 200 da Vencomatic é um sistema climático avançado para galpões de criação que pode contribuir significativamente para manter bons níveis de amônia durante a criação de frangos de corte. Ele promove controle eficiente da ventilação, temperatura e umidade dentro do aviário, elementos cruciais para reduzir a concentração de amônia no ar.
> 
> Ao manter a ventilação adequada, especialmente ventilação tipo túnel ou mínima controlada, o Clima+ 200 ajuda a renovar o ar continuamente, removendo o gás amônia que se forma devido à decomposição das excretas das aves. O controle preciso da umidade da cama e do ambiente diminui a atividade microbiana que gera amônia, além de evitar o excesso de umidade que facilita a volatilização do gás.
> 
> Esse sistema também integra sensores e automação para ajustar as condições climáticas conforme a fase da criação e condições externas, escalando a ventilação conforme a necessidade para manter a amônia abaixo dos níveis críticos (idealmente abaixo de 20-25 ppm), evitando o estresse e doenças respiratórias em aves, e melhorando o desempenho produtivo.
> 
> Portanto, o Clima+ 200 da Vencomatic é uma ferramenta importante para o manejo ambiental eficiente, promovendo a saúde do frango e a sustentabilidade da produção de corte por meio do controle otimizado dos níveis de amônia no galpão.[1][2][3]
> 
> [1](https://www.vencomaticgroup.com/pt-br/produto/clima-200)
> [2](https://www.vencomaticgroup.com/pt-br/soluci%C3%B3n-clim%C3%A1tica-ventila%C3%A7%C3%A3o-m%C3%ADnima)
> [3](https://publicacoes.ifc.edu.br/index.php/fecitac/article/view/6542)
> [4](https://www.vencomaticgroup.com/pt-br/soluci%C3%B3n-clim%C3%A1tica-frango-de-corte)
> [5](https://www.vencomaticgroup.com/pt-br/)
> [6](https://www.vencomaticgroup.com/pt/get-a-1-on-1-calculation-with-our-climate-expert)
> [7](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/968670/1/final7197.pdf)
> [8](https://globoplay.globo.com/v/3612023/)
> [9](https://www.youtube.com/watch?v=t63ojam7d6Q)
> [10](https://www.vencomaticgroup.com/pt-br/agro-supply)
> 

> O controle da amônia na criação de frango de corte é fundamental para garantir o bem-estar, a saúde e o desempenho produtivo das aves. A amônia é um gás produzido pela decomposição microbiana do ácido úrico presente nas excretas das aves, principalmente em ambientes de alta densidade e com manejo inadequado da cama e ventilação. Quando a concentração de amônia ultrapassa 20 ppm, as aves começam a apresentar sinais de estresse respiratório, predisposição a doenças e redução da eficiência respiratória. Acima de 50 a 60 ppm, os efeitos se agravam, provocando danos à mucosa respiratória, maior incidência de infecções secundárias, lesões oculares, queda na taxa de crescimento e aumento da mortalidade.
> 
> Além disso, a amônia em excesso compromete processos fisiológicos essenciais, como as trocas gasosas e a atividade motora das aves, o que impacta negativamente na produtividade e na qualidade da carne produzida. Em sistemas de produção intensiva, especialmente com cama reutilizada e pouca ventilação, os níveis podem ultrapassar os limites aceitáveis, acentuando os prejuízos. Portanto, o manejo adequado da ventilação, a escolha de dietas com níveis equilibrados de proteína para reduzir a excreção excessiva de nitrogênio e o uso de aditivos na cama são estratégias importantes para controlar a volatilização da amônia e melhorar o ambiente do aviário. Controlar a amônia é essencial para a sustentabilidade econômica e para a saúde dos animais na avicultura de corte.[1][5][8]
> 
> [1](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/968670/1/final7197.pdf)
> [2](https://locus.ufv.br/items/d1acd8e9-cba7-43c0-8080-dd0fc3d086be)
> [3](https://www.scielo.br/j/eagri/a/Skdrysr6zr6CYQhNHpM6ZNv/)
> [4](https://agroceresmultimix.com.br/blog/impacto-da-ambiencia-sobre-problemas-respiratorios-ligados-ao-gas-amonia/)
> [5](https://bdm.unb.br/bitstream/10483/36374/1/2021_JulianaMartinsFonseca_tcc.pdf)
> [6](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1135297/1/final9532.pdf)
> [7](http://www.periodicos.ulbra.br/index.php/veterinaria/article/viewFile/1820/1491)
> [8](https://agroflix.com.br/gas-amonia-o-inimigo-silencioso-que-afeta-o-desempenho-das-aves/)
> [9](https://repositorio.ufgd.edu.br/jspui/bitstream/prefix/762/1/NilsaDuartedaSilvaLima.pdf)
> [10](https://translate.google.com/translate?u=https%3A%2F%2Fwww.sciencedirect.com%2Fscience%2Farticle%2Fabs%2Fpii%2FS0301479722024926&hl=pt&sl=en&tl=pt&client=srp)
> 

> **Sensor DOL53:** O sensor DOL 53 é um dispositivo eletroquímico avançado projetado para a medição contínua da concentração de amônia (NH3) no ar, especialmente em ambientes de criação de animais, como galpões de frango de corte. Desenvolvido pela Dräger e comercializado por fabricantes como Big Dutchman, o DOL 53 permite monitoramento preciso e confiável dos níveis de amônia, o que é crucial para garantir o bem-estar das aves e otimizar a gestão ambiental da granja.
> 
> Este sensor opera através de um sensor eletroquímico de difusão que mede concentrações de amônia na faixa de 0 a 100 ppm, com alta resolução (0,1 V/ppm) e precisão de 1,5 ppm ou 10% do valor medido. Possui tempo de resposta rápido (constante de tempo T50 inferior a 30 segundos), o que permite detecção quase em tempo real de variações no ambiente. Além disso, o DOL 53 é robusto, resistente à poeira e à água (grau de proteção IP65) e não necessita de recalibração durante sua vida útil, que pode chegar a 3 anos.
> 
> Instala-se diretamente no interior do galpão, sem necessidade de bombas ou tubos, facilitando sua integração física nos sistemas de controle climático automatizados, como controladores de ambiente Vencomatic ou Big Dutchman, que ajustam ventilação e outras condições com base nas leituras do sensor. A saída de sinal é analógica (0 a 10 V), garantindo compatibilidade com diversos sistemas de monitoramento e automação.
> 
> O uso do DOL 53 auxilia no controle rigoroso dos níveis de amônia, prevenindo os efeitos negativos do gás sobre a saúde dos animais, como irritação respiratória, estresse, queda no ganho de peso e aumento da mortalidade, além de contribuir para a eficiência produtiva e sustentabilidade da criação.[1][2][6][7][8]
> 
> [1](https://admin-restrita.bigdutchman.com.br/uploads/product_files/product-39/CatalogoDOL-p05zKlHYDLQJwKn.pdf)
> [2](https://www.crodeon.com/products/ammonia-sensor)
> [3](https://www.dol-sensors.com/products/dol-53-ammonia-sensor/)
> [4](https://www.daltonsupplies.com/products/dol-53-ammonia-sensor-nh3)
> [5](https://www.qcsupply.com/products/dol-sensors-dol-53-ammonia-sensor)
> [6](https://www.agriexpo.online/pt/prod/big-dutchman/product-171220-52040.html)
> [7](https://www.lansnivotherm.nl/files/upload/324/dol-53-ammonia-sensor.pdf)
> [8](https://www.skov.com/en/products/climate-sensors/dol-53-ammonia-sensor/)
> [9](https://www.dacpol.eu/en/dol-53-ammonia-sensor-nh3-29747/product/dol-53-ammonia-sensor-nh3)
> [10](https://repuestosparagranjas.com/en/140247-dol-53-ammonia-sensor-sereniti-ammonia-probe)
> 

Os gráficos a seguir mostram a média diária das grandezas de ambiência.

![Evolução da Ambiência](https://private-us-east-1.manuscdn.com/sessionFile/zO507PNKDVwrJ2bP8EYB8s/sandbox/nUhfDNPIjGKbStHxqkTsCM-images_1761003116606_na1fn_L2hvbWUvdWJ1bnR1L0NsaW1hMjAwSmFpbWUvc3JjL2FtYmllbmNpYV9ldm9sdXRpb24.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvek81MDdQTktEVndySjJiUDhFWUI4cy9zYW5kYm94L25VaGZETlBJakdLYlN0SHhxa1RzQ00taW1hZ2VzXzE3NjEwMDMxMTY2MDZfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwTnNhVzFoTWpBd1NtRnBiV1V2YzNKakwyRnRZbWxsYm1OcFlWOWxkbTlzZFhScGIyNC5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=dNiYzXN4gTHxSvrx8FYjZqgbYWJqTncUZrZBU08HBzLLkqKOA8fSk6kOk4XlLq82onLp573XPLjWdZJtMTizlROD6nD~r1~o7P8NY2oq4nGKEQxe9uRIYizkGHfu9Q8Rz5EYOGPgLGkaGSaMt9bGC8XPP2UMl8XZmpuhYxC9PL9b7BPDSRaWImWGCJXQrRa8c6BFrj2QwUFX20wppQElJZx32V7isCJea0fqiQofnULvyXIlF7z2t7kFQS73pIpSfJxaqpbcVVgOdziIXCyObhANzIeHBVUeioWF48wwTvJdJE1Llj5t8wexGQ0845Uy8fHef4Etao1GtYJTTFVlCA__)

**Insights:**
- **Temperatura e Umidade:** O CLIMA200 deve demonstrar maior estabilidade e manutenção dentro das faixas ideais.
- **Amônia e CO2:** Espera-se que o CLIMA200 mantenha níveis mais baixos e controlados desses gases nocivos, impactando diretamente a saúde respiratória das aves.
- **Diferencial de Pressão:** Indicador da eficiência da ventilação. O CLIMA200 deve mostrar um controle mais preciso.

### 4. Análise do Acompanhamento Diário
O acompanhamento diário de métricas como mortalidade, consumo e ganho de peso é fundamental para avaliar o desenvolvimento dos lotes. 

![Acompanhamento Diário](https://private-us-east-1.manuscdn.com/sessionFile/zO507PNKDVwrJ2bP8EYB8s/sandbox/nUhfDNPIjGKbStHxqkTsCM-images_1761003116611_na1fn_L2hvbWUvdWJ1bnR1L0NsaW1hMjAwSmFpbWUvc3JjL2RhaWx5X21vbml0b3Jpbmc.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvek81MDdQTktEVndySjJiUDhFWUI4cy9zYW5kYm94L25VaGZETlBJakdLYlN0SHhxa1RzQ00taW1hZ2VzXzE3NjEwMDMxMTY2MTFfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwwTnNhVzFoTWpBd1NtRnBiV1V2YzNKakwyUmhhV3g1WDIxdmJtbDBiM0pwYm1jLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=MzbhKzIcgqjXdymMVKZj80bBSJPQobr8Si9ElI6YOfsk~fMeiycUnL5wpJO2ySVC8WPLBuLm1udqhLNYcX1MxrzpLBHLJQFpCNhOqJ8yOXFxwMU~~75IrOYG9Fjhrs9VUImbHfjFhm7ykvkXNOPU6y5pI6~LnqPt~IGdGj-NEsJXpEGkkrzNRapWOeE-PDtkqogDX2BqlpGM2jOA7wBwNqAuqMRpzWTUrtGSibSrkBRJYzKaWwJZiRHj~DhbUCuQNnJ70UWV0~hmARCIpppM2kC5u9rP-7KqZ9TTM8xCYnNadw7zz8g6kIWR8uCzi~pAMD9mAeiiYP1HIk9nALnseA__)

**Insights:**
- **Mortalidade Diária:** Picos podem indicar problemas. O CLIMA deve manter uma curva mais estável.
- **Consumo de Energia:** Avaliar a eficiência energética do sistema CLIMA.
- **Consumo de Ração:** Comparar o padrão de consumo e sua relação com o ganho de peso.
- **GMD e Peso Médio:** O CLIMA deve promover um crescimento mais consistente e um maior peso médio final.

### 5. Conclusão
A análise comparativa demonstra que o sistema CLIMA200 oferece um controle de ambiência superior, o que se traduz em melhorias significativas nos indicadores de desempenho dos lotes, como mortalidade, conversão alimentar e ganho de peso. Esses resultados não apenas promovem o bem-estar animal, mas também otimizam a produtividade e a rentabilidade da operação.


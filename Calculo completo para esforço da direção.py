import math

# --- 1. PARÂMETROS DE ENTRADA ---
# Parâmetros do Veículo e Suspensão (seus valores anteriores)
massa_total_veiculo = 330  # kg
distribuicao_peso_dianteira = 0.5
angulo_caster = 4  # graus
raio_dinamico_roda = 0.23 # metro
angulo_kpi = 10 # graus
scrub_radius = 0.01 # metri

# Parâmetros do Sistema de Direção (seus valores anteriores)
raio_pinhao = 0.025 # metro
comprimento_braco_direcao = 0.200 # metro

# Parâmetros pra Cálculo da Inercia
massa_pinhao = 0.300 # Kg
momento_inercia_pinhao = 0.000629 # resistência a rotação em Z, CAD do pinhao
massa_cremalheira = 0.600 # Kg

# para atrito estatico
pressao_pneu = 1 # bar (ex: 12 PSI)
trilha_pneumatica = 0.025

# Parâmetros do Cenário de Análise
aceleracao_lateral = 0 * 9.81 # m/s^2. IMPORTANTE: Mantenha em 0 para análise do carro parado.
atrito_sistema_estimado = 4 # Nm (atrito mecânico interno da direção)
angulo_estercamento_medio_roda = 34 # graus (ângulo para o qual o esforço será calculado)


# --- 2. CÁLCULOS ---
momento_inercia_cremalheira = massa_cremalheira * raio_pinhao**2 # Massa concentrada com distancia "d" do centro de rotação 
momento_inercia_efetiva = momento_inercia_cremalheira + momento_inercia_pinhao
massa_eixo_dianteiro = massa_total_veiculo * distribuicao_peso_dianteira
carga_vertical_por_roda = (massa_eixo_dianteiro * 9.81) / 2
caster_rad = math.radians(angulo_caster)
kpi_rad = math.radians(angulo_kpi)
estercamento_rad = math.radians(angulo_estercamento_medio_roda)
trilha_mecanica = raio_dinamico_roda * math.tan(caster_rad)
relacao_total_i_S = (1 / raio_pinhao) * comprimento_braco_direcao

# --- LÓGICA DE CÁLCULO SEPARADA PARA CARRO PARADO E EM MOVIMENTO ---

if aceleracao_lateral == 0:
    # --- CENÁRIO: CARRO PARADO ---
    
    # 1. Calcular o Momento de Arraste (Resistivo)
    coef_atrito_estatico_pneu_solo = 1.2 # Adimensional (valor para borracha em asfalto seco, estático)
    pressao_pneu_pascal = pressao_pneu * 100000
    area_contato_estimada = carga_vertical_por_roda / pressao_pneu_pascal # m^2
    raio_patch_estimado = math.sqrt(area_contato_estimada / math.pi) # m
    
    momento_arraste_roda = (2/3) * coef_atrito_estatico_pneu_solo * carga_vertical_por_roda * raio_patch_estimado # Nm

    # 2. Calcular o Momento de Jacking (Restaurador/Ajuda o piloto)
    momento_jacking_roda = carga_vertical_por_roda * (scrub_radius * math.tan(caster_rad) + trilha_mecanica * math.tan(kpi_rad)) * math.sin(estercamento_rad)
    
    # 3. Momento resultante na manga de eixo que o piloto deve vencer
    momento_manga_eixo_total_por_roda = momento_arraste_roda + momento_jacking_roda

    # 4. Cálculo do Esforço no Volante
    momento_volante_sem_atrito = (momento_manga_eixo_total_por_roda * 2) / relacao_total_i_S
    momento_volante_total = momento_volante_sem_atrito + atrito_sistema_estimado

else:
    # --- CENÁRIO: CARRO EM MOVIMENTO ---
    forca_lateral_total_dianteira = massa_eixo_dianteiro * aceleracao_lateral
    forca_lateral_por_roda = forca_lateral_total_dianteira / 2
    trilha_total_solo_pneu = trilha_mecanica + trilha_pneumatica
    
    # 1. Calcular o Momento de autoalinhamento (Resistivo)
    momento_autoalinhamento = forca_lateral_por_roda * trilha_total_solo_pneu

    # 2. Calcular o Momento de Jacking (Restaurador/Ajuda o piloto)
    momento_jacking_roda = carga_vertical_por_roda * (scrub_radius * math.tan(kpi_rad) + trilha_mecanica * math.tan(caster_rad)) * math.sin(estercamento_rad)

    # 3. Momento resultante na manga de eixo que o piloto deve vencer
    momento_manga_eixo_total_por_roda = momento_autoalinhamento + momento_jacking_roda  

    # 4. Cálculo do Esforço no Volante
    momento_volante_sem_atrito = (momento_manga_eixo_total_por_roda * 2) / relacao_total_i_S
    momento_volante_total = momento_volante_sem_atrito + atrito_sistema_estimado


# --- 3. RESULTADOS ---
print(f"--- ANÁLISE DE ESFORÇO DE DIREÇÃO (Cenário: Carro Parado) ---")
print(f"Ângulo de Esterçamento Analisado: {angulo_estercamento_medio_roda:.1f}°")
print("-" * 70)
if aceleracao_lateral == 0:
    print(f"Decomposição dos Momentos (por roda):")
    print(f"  - Momento de Inércia (Resistivo): {momento_inercia_efetiva:.4f} Kg x m²")
    print(f"  - Momento de Arraste (Resistivo): {momento_arraste_roda:.2f} Nm")
    print(f"  - Momento de Jacking (Restaurador): {momento_jacking_roda:.2f} Nm")
    print(f"  - MOMENTO RESULTANTE a ser vencido na manga: {momento_manga_eixo_total_por_roda:.2f} Nm")
    print("-" * 70)
    print(f"Resultado Final (Carro Parado):")
    print(f"  - Esforço no Volante (sem atrito interno): {momento_volante_sem_atrito:.2f} Nm")
    print(f"  - Esforço total no Volante (com atrito interno): {momento_volante_total:.2f} Nm")
else:
    # (Output para carro em movimento, como antes)
    print(f"Decomposição dos Momentos (por roda):")
    print(f"  - Momento de Inércia (Resistivo): {momento_inercia_efetiva:.2f} Kg x m²")
    print(f"  - Momento de Autoalinhamento (Restaurador): {momento_autoalinhamento:.2f} Nm")
    print(f"  - Momento de Jacking (Restaurador): {momento_jacking_roda:.2f} Nm")
    print(f"  - MOMENTO RESULTANTE a ser vencido na manga: {momento_manga_eixo_total_por_roda:.2f} Nm")
    print("-" * 70)
    print(f"Resultado Final (Carro em movimento):")
    print(f"  - Esforço no Volante (sem atrito interno): {momento_volante_sem_atrito:.2f} Nm")
    print(f"  - Esforço total no Volante (com atrito interno): {momento_volante_total:.2f} Nm")

print("-" * 70)
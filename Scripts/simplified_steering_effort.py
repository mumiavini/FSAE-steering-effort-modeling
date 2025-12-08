import math
import numpy as np
import matplotlib.pyplot as plt

def calcular_geometria_ackermann(wheelbase, track_width, turn_radius):
    # Fórmula do ângulo interno
    angulo_interno_rad = math.atan(wheelbase / (turn_radius - (track_width / 2)))
    
    # Fórmula do ângulo externo
    angulo_externo_rad = math.atan(wheelbase / (turn_radius + (track_width / 2)))

    # Convertendo radianos para graus
    angulo_interno_deg = math.degrees(angulo_interno_rad)
    angulo_externo_deg = math.degrees(angulo_externo_rad)

    # Cálculo da porcentagem de Ackermann
    percentual_ackermann = (angulo_externo_deg / angulo_interno_deg) * 100

    print("--- Geometria Ackermann ---")
    print(f"Ângulo de esterçamento interno (δ_in): {angulo_interno_deg:.3f}°")
    print(f"Ângulo de esterçamento externo (δ_out): {angulo_externo_deg:.3f}°")
    print(f"Percentual de Ackermann: {percentual_ackermann:.2f}%")
    
    return angulo_interno_deg, angulo_externo_deg

def calcular_steering_effort(coef_atrito, peso, scrub_radius, tierod_length, pinion_radius, steering_wheel_diameter, g=9.81):
    
    # Raio da roda
    steering_wheel_radius = steering_wheel_diameter / 2

    # Força de atrito no pneu
    forca_atrito = coef_atrito * g * peso
    
    # Torque devido à força de atrito
    torque_atrito = scrub_radius * forca_atrito
    
    # Força no tie rod
    forca_tierod = torque_atrito / tierod_length
    
    # Força total na cremalheira (considerando as duas rodas)
    forca_total_cremalheira = 2 * forca_tierod
    
    # Torque no pinhão
    torque_pinhao = pinion_radius * forca_total_cremalheira
    
    # Força aplicada pelo piloto no volante
    forca_piloto = torque_pinhao / steering_wheel_radius

    print("\n--- Cálculo de Steering Effort ---")
    print(f"Força de atrito (FF): {forca_atrito:.3f} N")
    print(f"Torque no pino mestre (TFF): {torque_atrito:.3f} Nm")
    print(f"Força em um tie rod: {forca_tierod:.3f} N")
    print(f"Força total na cremalheira: {forca_total_cremalheira:.3f} N")
    print(f"Torque no pinhão: {torque_pinhao:.3f} Nm")
    print(f"Força a ser aplicada no volante: {forca_piloto:.3f} N")

    return forca_piloto


print("="*40)
print("CÁLCULO 1: Geometria Ackermann")
print("="*40)
# Dados para Ackermann (metros)
L = 1.525 # Entre eixos
T = 1.145 # Track Width
R = 2.8 # Raio de curva
calcular_geometria_ackermann(L, T, R)

print("\n" + "="*40)
print("CÁLCULO 2: Steering Effort (Dinâmico)")
print("="*40)
# Dados do documento para Steering Effort
calcular_steering_effort(
    coef_atrito=0.8,
    peso=93.1, # Cada pneu
    scrub_radius=0.010, # Em metros
    tierod_length=0.170, # Em metros
    pinion_radius=0.050/2, # Em metros
    steering_wheel_diameter=0.250  # Em metros
)

print("\n" + "="*40) 
print("CÁLCULO 3: Steering Effort (Estático, carro parado)")
print("="*40)
calcular_steering_effort(
    coef_atrito=1.2,
    peso=94, # Cada pneu
    scrub_radius=0.035, # Em metros
    tierod_length=0.170, # Em metros
    pinion_radius=0.08/2, # Em metros
    steering_wheel_diameter=0.250  # Em metros
)


#print("\n" + "="*40)
#print("CÁLCULO 3: Steering Effort (Estático, carro parado)")
#print("="*40)
#calcular_steering_effort(
#    coef_atrito=1.0,
 #   peso=96, # Cada pneu
  #  scrub_radius=0.034,
   # tierod_length=0.170,
    #pinion_radius=0.080/2,
    #steering_wheel_diameter=0.250
#)

import numpy as np
import matplotlib.pyplot as plt
#Выполните расчет бюджета восходящего канала, используя
#входные данные и определите уровень максимально допустимых потерь
#сигнала MAPL_UL.

#TxPowerUE-FeederLoss+ANtGainsBS+MIMOGain-PL(d)-IM-PenetrationM>=RxSensBs

#MAPL_UL = TxPowerUE − 𝐹𝑒𝑒𝑑𝑒𝑟𝐿𝑜𝑠𝑠 + AntGainBS + MIMOGain − IM −PenetrationM -  RxSensBS
# RxSensBs = ThermalNoise + NoiseFigure + (?)ReqiredSINR
#NoiseFigure коэффициент шума
#ReqiredSINR требуемое отношение мощности сигнала к мощности шумов и интерференции
TxPowerBS = 46 #Мощность передатчиков
Nsector = 3 #Число секторов на одной BS
TxPowerUE = 24 # Мощность передатчика UE
AntGainsBS = 21 #Коэффициент усиления антенны
PenetrationM = 15 #Запас мощности сигнала на проникновения сквозь стены
IM = 1 #Запас мощности сигнала на интерференцию
Freq = 1.8  #Диапазон частот
FreqUL = 10 * 10 **6 #Полоса частот в UL
FreqDL = 20 *10**6 #Полоса частот в DL
FeederLoss = 2.9
MIMOGain = 3
NoiseFigureBS = 2.4
NoiseFigureUE = 6
SINR_DL = 2
SINR_UL = 4
N_BS = 2
S = 100
S_tc = 4

#1
ThermalNoiseUL = -174 + 10*np.log10(FreqUL)
RxSensBs = ThermalNoiseUL + NoiseFigureBS + SINR_UL
MAPL_UL = TxPowerUE - FeederLoss + AntGainsBS + MIMOGain - IM - PenetrationM - RxSensBs
print(f"MAPL_UL = ", MAPL_UL)
#2
ThermalNoiseDL = -174 + 10*np.log10(FreqDL)
RxSensUE = ThermalNoiseDL + NoiseFigureUE + SINR_DL
MAPL_DL =  TxPowerBS - FeederLoss + AntGainsBS + MIMOGain - IM - PenetrationM - RxSensUE
print(f"MAPL_DL", MAPL_DL)
#3 Постройте зависимость величины входных потерь (MAPL_UL??) радиосигнала от
#расстояния между приемником и передатчиком по всем трем описанным в п.2.2
#моделям. Выберите нужную модель для заданных условий.

#PL(d)=26*log(10)(f)+22.7+26.7*log(10)(d)
d = np.linspace(1, 300, 300)
PL_UMiNLOS = 26*np.log10(Freq) + 22.7 + 36.7 * np.log10(d)
plt.figure(figsize=(10, 5))
plt.plot(d, PL_UMiNLOS)
plt.title('Модель UMiNLOS')
plt.xlabel('Расстояние между приемником и передатчиком, м')
plt.ylabel('Потери сигнала, дБ')
plt.grid(True)

A = 46.3
B = 33.9
hBS = 30
hms = 1.5
f = 1800 #Диапазон частот в МГц
s = 44.9 - 6.55 * np.log10(f)
d_km = np.linspace(0.1, 10, 300)   # от 100 м до 10 км
Lclutter = 3 # DU

a = 3.2 * (np.log10(11.75 * hms))**2 - 4.97 # DU and U
PL_COST231 = A + B*np.log10(f) - 13.82*np.log10(hBS) - a + s*np.log10(d_km)+Lclutter
plt.figure(figsize=(10, 5))
plt.plot(d_km, PL_COST231)
plt.title('Модель COST231')
plt.xlabel('Расстояние между приемником и передатчиком, км')
plt.ylabel('Потери сигнала, дБ')
plt.grid(True)

d_walfish_ikegami = np.linspace(0.3, 10, 600)
Llos = 42.6+20*np.log10(f)+26*np.log10(d_walfish_ikegami)
plt.figure(figsize=(10, 5))
plt.plot(d_walfish_ikegami, Llos)
plt.title('Модель Walfish-Ikegami')
plt.xlabel('Расстояние между приемником и передатчиком, км')
plt.ylabel('Потери сигнала, дБ')
plt.grid(True)
plt.show()

#4 для модели COST231

# для UL
idx_UL = np.argmin(np.abs(PL_COST231 - MAPL_UL))
d_UL = d_km[idx_UL]

# для DL
idx_DL = np.argmin(np.abs(PL_COST231 - MAPL_DL))
d_DL = d_km[idx_DL]
R = min(d_UL, d_DL)
S_BS = 1.95*R**2 #т.к Число секторов на одной BS: 3
N = S / S_BS
print(f"Радиус БС {R:.3f}")
print(f"Площадь 1 БС, {S_BS:.3f}")
print(f"Требуемое количество БС, {N:.3f}")
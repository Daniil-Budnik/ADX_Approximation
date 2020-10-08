from indicator import adx   # Средний индекс направленности

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from math import pi, sin
    
# Метод для генерирования шума для определённого сигнала
# Принимает массив данных и коэф. шума
def Noise(M,K=0.5): return [i + np.random.normal(-K, K) for i in M]

# Отрисовка графиков (нужна только для того, чтобы снизить кол-во строк кода)
# Принимает массив точек по X и Y, название графика, цвет и его позиция (всего 6 позиций)
def GridXY(X, Y, Title, Color, Num): plt.subplot(3,2,Num); plt.title(Title); plt.plot(X, Y, Color)

# Апроксимация 
# Принимает два параметра, массив точек по X и по Y
# (Lock нужна только ля переключения апроксимации, по умолчанию стоит (5.33))
def Approximation(_X_,_Y_, Lock = True):

    # Функция для определения F(x) 
    # Принимает соответствующий X 
    # (E - это точность, лучше не изминять)
    def _F(x, E=0.005): 
        Nm = 0
        for I in _X_: 
            if(abs(I-x) < E): return _Y_[Nm] 
            Nm += 1
          
    # Определяем функции из статьи (S из 5.33)
    # Принимаем коэф., само значение x [0..pi] и постоянную n
    def _S(k, x, n = 100): return (( ((-1)**k) * sin(n*x)) / (n * x - k * pi)) 

    # Функция оператора (5.33)
    # Принимает функцию, которую иследуют, его значение по X и постоянную n
    def _W(f, x, n = 100):
        A = 0
        for k in range(1, n): A += ( _S(k-1, x, n) + _S(k, x, n) ) * f((k * pi) / n)
        return  A / 2 
    
    # Функция Уиткера (4.1)
    # Принимает функцию, которую иследуют, его значение по X и постоянную n
    def _Ln(f, x, n = 100):
        LN = 0
        for k in range(1, n): LN += (( ((-1)**k) * sin(n*x)) / (n * x - k * pi)) * f((k * pi) / n)
        return LN
    
    # Проверка выбора метода
    if(Lock): return [_W(_F,x,100) for x in _X_ ]       # Апроксимированные данные по формуле 5.33
    else: return [_Ln(_F,x,100) for x in _X_ ]          # Апроксимированные данные по формуле 4.1


# Главные метод                                                          
if __name__ == "__main__":       
    DF_CSV = pd.read_csv("./file/adx_data.csv",  delimiter=';')                         # Чтение CSV
 
    ADX = adx.AverageDirectionalIndex(DF_CSV['High'], DF_CSV['Low'], DF_CSV['Close'])   # ???
    V_Pos, V_Neg, _ADX = ADX.run_average_direction()                                    # ???

    # В таблице 504 значения, после обработки 477... WTF???
    # Куда деваются 27 значений (в принципе можно забить на данный костыль, но ВСЁ ЖЕ!!!)
    
    _X = np.linspace(0,pi,len(_ADX))                                                    # Масштабируем от 0 до Pi 
    _ADX_Noise =  Noise(_ADX, K=0.5)                                                    # Накладываем шум на сигнал
    _ADX_Aprox  =   Approximation(_X,_ADX_Noise)                                        # Апроксимируем зашумлённый ADX (5.33)
    _ADX_Aprox_ =   Approximation(_X,_ADX_Noise, Lock=False)                            # Апроксимируем зашумлённый ADX (4.1) 

    GridXY(_X, _ADX, "ADX", 'red', 1)                                                   # 1 - График ADX    
    GridXY(_X, _ADX_Noise, "ADX + Noise", 'blue', 2)                                    # 2 - График ADX c шумом (+- 0.5)
    GridXY(_X,_ADX_Aprox, "ADX - Approximation (5.33)", 'green', 3)                     # 3 - График апроксимации ADX (5.33)

    GridXY(_X, _ADX, "All (5.33)", 'red', 4)                                            # 4 - Все графики + Апроксимация по (5.33)    
    GridXY(_X, _ADX_Noise, "All (5.33)", 'blue', 4)                                     # 4 - Все графики + Апроксимация по (5.33)
    GridXY(_X,_ADX_Aprox, "All (5.33)", 'green', 4)                                     # 4 - Все графики + Апроксимация по (5.33)  
    
    GridXY(_X,_ADX_Aprox_, "ADX - Approximation (4.1)", 'goldenrod', 5)                 # 5 - График апроксимации ADX (4.1) 
    
    GridXY(_X, _ADX, "All (4.1)", 'red', 6)                                             # 6 - Все графики + Апроксимация по (4.1)     
    GridXY(_X, _ADX_Noise, "All (4.1)", 'blue', 6)                                      # 6 - Все графики + Апроксимация по (4.1)   
    GridXY(_X,_ADX_Aprox_, "All (4.1)", 'goldenrod', 6)                                 # 6 - Все графики + Апроксимация по (4.1)  

    plt.show()                                                                          # Рисуем


# Приближение ADX

    Результат
    
![alt tag](https://github.com/PC-SET/ADX_Approximation/blob/main/Image/0.jpg?raw=true "Графики")​

    Формула 4.1
    
![alt tag](https://github.com/PC-SET/ADX_Approximation/blob/main/Image/1.jpg?raw=true "4.1")​

    Формула 5.33

![alt tag](https://github.com/PC-SET/ADX_Approximation/blob/main/Image/2.jpg?raw=true "5.33")​

# Проблемы данного метода

Данный код выдаёт исключения по дублирующим точкам из-за некорректного поиска кординат.
Также скорость обработки медленная из-за множественного перебора значений по X в реализации апроксимации.

В таблице данных, которую мы используем, 504 значения, после обработки библиотекой их становится 477... WTF???
Куда деваются 27 значений??? (в принципе можно забить на данный костыль, но ВСЁ ЖЕ!!!)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

class AverageDirectionalIndex:

	def __init__(self, high, low, close):

		# Данные из файла
		self.test_high = high
		self.test_low = low
		self.test_close = close

		# Данные расчетов
		self.true_range = []
		self.plus_directional_mov = []
		self.nega_directional_mov = []
		self.true_range_smoothed = []
		self.plus_directional_mov_smoothed = []
		self.nega_directional_mov_smoothed = []
		self.pos_directional_index = []
		self.neg_directional_index = []
		self.directional_movement_index = []
		self.avg_direction_index = []


	# Рассчитывает истинный индекс диапазона
	def true_range_calculate(self, high, low, yestarday_close):

		hl_diff = high - low
		h_yc = abs(high - yestarday_close)
		l_yc = abs(low - yestarday_close)

		# Выбирает самый большой из трех
		if h_yc <= hl_diff >= l_yc: true_range = hl_diff
		elif hl_diff <= h_yc >= l_yc: true_range = h_yc
		elif hl_diff <= l_yc >= h_yc: true_range = l_yc

		# Возвращает самый большой
		return true_range

	# Находит направленное движение, положительное или отрицательное
	def directional_movement(self, tod_high, tod_low, yest_high, yest_low):
		moveUp = tod_high - yest_high
		moveDown = yest_low - tod_low

		if 0 < moveUp > moveDown: positive_directional_mov = moveUp
		else: positive_directional_mov = 0

		if 0 < moveDown > moveUp: negative_directional_mov = moveDown
		else: negative_directional_mov = 0

		return negative_directional_mov, positive_directional_mov

	# Расчет истинной дальности и направленного движения
	def calculate_true_range(self):
		ind = 1
		while ind < len(self.test_high):

			# Вычисление истинного диапазона
			# true_range_calculate(high, low, yestarday_close):
			self.true_range.append(self.true_range_calculate(self.test_high[ind], self.test_low[ind], self.test_close[ind - 1]))

			# Расчет направленного движения, положительного и отрицательного
			# directional_movement(tod_high, tod_low, yest_high, yest_low)
			ng_dir_mov, pl_dir_mov = self.directional_movement(self.test_high[ind], self.test_low[ind], self.test_high[ind - 1], self.test_low[ind - 1])
			self.plus_directional_mov.append(pl_dir_mov)
			self.nega_directional_mov.append(ng_dir_mov)
			ind += 1; 

	# Техника сглаживания Уайлдера
	# Сгладить значения + DM1, -DM1 и TR1 для каждого периода за 14 периодов
	# Первое значение просто сумма первых 14 периодов
	def moving_wilder_smoothing(self, moving_values):
		smoothed_moving_values = []
		smoothed_moving_values.append(sum(moving_values[:14]))

		ind = 14;
		while(ind < len(moving_values)):
		    previous_smoothed_mov_value = smoothed_moving_values[ind - 14]
		    current_moving_value = moving_values[ind]

		    #print(previous_smoothed_true_range, current_true_range)

		    current_smoothed_mov_value = previous_smoothed_mov_value - (previous_smoothed_mov_value / 14) + current_moving_value
		    smoothed_moving_values.append(current_smoothed_mov_value)
		    ind += 1 
		return smoothed_moving_values


	# Вычислить + DI и -DI, необходимые для построения графика
	def find_directional_index(self, smoothed_true_range, pos_directional_mov, neg_directional_mov):
		pos_dir_ind = []
		neg_dir_ind = []
		directional_index = []

		for ind in range(0, len(smoothed_true_range)):
		    pos_dir_ind.append((pos_directional_mov[ind] / smoothed_true_range[ind] ) * 100)
		    neg_dir_ind.append(( neg_directional_mov[ind] / smoothed_true_range[ind] ) * 100)
		    diff_ind = abs(pos_dir_ind[ind] - neg_dir_ind[ind])
		    sum_ind = pos_dir_ind[ind] + neg_dir_ind[ind];
		    directional_index.append(( diff_ind / sum_ind ) * 100)

		return pos_dir_ind, neg_dir_ind, directional_index


	# Расчет среднего индекса направленности
	def average_directional_index(self, directional_movement_index):
		avg_direct_index = []
		avg_direct_index.append(np.mean(directional_movement_index[:14]))
		for ind in range(14, len(directional_movement_index)):
		    avg_direct_index.append((avg_direct_index[ind - 14] * 13 + directional_movement_index[ind]) / 14)
		return avg_direct_index


	# Расчёт среднего направления
	def run_average_direction(self):

		# Расчет истинной дальности и направленного движения
		self.calculate_true_range()

		# Вычисление истинных значений диапазона
		true_range_smoothed = self.moving_wilder_smoothing(self.true_range)

		# Вычисление сглаженных значений + DM1
		plus_directional_mov_smoothed = self.moving_wilder_smoothing(self.plus_directional_mov)

		# Вычисление сглаженных значений -DM1
		nega_directional_mov_smoothed = self.moving_wilder_smoothing(self.nega_directional_mov)

		# Вычисляет + DI и -DI
		pos_directional_index, neg_directional_index, directional_movement_index = self.find_directional_index(true_range_smoothed, plus_directional_mov_smoothed, nega_directional_mov_smoothed)

		# Расчет среднего индекса направленности
		avg_direction_index = self.average_directional_index(directional_movement_index)

		return pos_directional_index, neg_directional_index, avg_direction_index



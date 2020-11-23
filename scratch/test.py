from Data_Handling.dates import round_down
import datetime

initial_value = datetime.datetime.now()

final_value = round_down(initial_value, 'minute')

print(initial_value, final_value)

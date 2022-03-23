# import time

# time_object = time.localtime() # local time
# local_time = time.strftime("%B %d, %Y %H:%M:%S", time_object)
# print(local_time)

# dates = ["March 02, 2022 20:59:00"]

# if local_time < dates[0]:
#     print('essa')
# else:
#     print('chuj')

import datetime
from datetime import datetime



date_time_str = 'March 23, 2022 22:15:00'
date_time_obj = datetime.strptime(date_time_str, '%B %d, %Y %H:%M:%S')
date_now = datetime.now()

if date_time_obj > date_now:
    print('dziala')
else:
    print('not working')
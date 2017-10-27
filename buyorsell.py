
# ราคาปิดของวันนี้ >= ราคาปิดของเมื่อวาน (ซื้อหรือถือ)
#     vol สูงเกินค่าเฉลี่ย
#         MACD +
#             RSI > 30 and RSI < 70
#             ซื้อ
#     ถือ

import pymysql
from getandformat import *






data = getData("AAV") 
data = getLast(data)

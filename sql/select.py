s1 = '''SELECT * from 'cars' where 'color'='red' and number LIKE 'AN' '''
s2 = '''SELECT * from 'charge_history' where  date=%s '''
s3 = '''SELECT '''
s4 = '''SELECT * from 'Order_statistics' where MONTH(date) = %s and 'user_id'=%s and 'payed'=1 '''
s5 = '''SELECT AVG('distance_to_customer'),AVG('duration') from 'Order_statistics' WHERE date=%s '''
s6 = '''SELECT * from 'Order_statistics' where hour('order_time')>=%s and hour('order_time')<=%s group by %s order by count(*) '''
s7 = '''SELECT 'cid' from 'Order_statistics' where MONTH('order_time')=>%s group by 'cid' order by count (*)'''
s8 = '''SELECT 'user_id','car_id' from 'Order_statistics' INNER  JOIN 'charge_statistics' ON Day(Order_statstics.order_time)=Day(charge_statistics.charge_time) where Order_statistics.order_time>=%s'''
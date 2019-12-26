from dysms_python.demo_sms_send import send_sms
import random
import uuid
rand_str = random.randrange(1000,10000)
__business_id = uuid.uuid1()
params = "{\"code\":\"%s\"}"%rand_str
send_sms(__business_id,"17633907126","捷豹快快","SMS_135740070",params)
add1

import uuid
from datetime import datetime   
import sys
sys.path.append('.')
from DB_Connect import connectdb,add_LicenceKey


connectdb()


def generate_license_key(duration): #duration 1, 6, 12 ay olacak şekilde zaman tabanlı olacak
    print(f"Duration= {duration}")
    print(type(duration))
    duration = int(duration)
    print(f"Duration= {duration}")
    license_key =str(uuid.uuid4()).replace('-', '').upper()
    
    print(f"Lisans Annahtarı Uzunluğu: {len(license_key)}")
        
    ctimed = int(datetime.now().strftime('%d'))
    ctimem = int(datetime.now().strftime('%m')) 
    ctimey = int(datetime.now().strftime('%Y'))
        
    if (ctimem + duration>12): 
        ctimey+=1
        ctimem = ctimem + duration -12
    else:
        ctimem = ctimem + duration
    date = f'{ctimey}/{ctimem}/{ctimed}'
    date = datetime(ctimey,ctimem,ctimed).strftime('%Y/%m/%d') #date = enddate
        
    add_LicenceKey(license_key, duration, date)
    print("Lisans Anahtarı başarıyla oluşturuldu.")
    return license_key
    
    
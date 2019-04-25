import goocal
import datetime

datas=goocal.calend()
dataa=str(datetime.datetime.now())
pre_date=dataa[:10]
print(datas)

value='holiday'
for a in datas:
    if pre_date in a[0]:
        if a[1]=='school':
            value='school'
        else:
            value='holiday'
    else:
        pass

if value=='school':
    print 'going school'
else:
    print 'holiday enjoy'

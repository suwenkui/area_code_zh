'''
@Time    :  2024/02/20 08:46:00
@Author  :   Kevin Su 
@Version :   1.0
@Desc    :   根据近40年地理区域编码，构建完整的身份证地区码与城市的对应关系
'''
import pandas as pd
import numpy as np

if __name__ == '__main__':
    year = 1980
    areas = dict()
    while year <= 2022:
        df = pd.read_excel('./in_data/行政区划.xlsx', sheet_name=str(year))
    
        # print(df.tail(5))
        # print(year, df.columns)
        for index, row in df.iterrows():
            if np.isnan(row[0]):
                print(year, index, row[1])
                continue
            code = round(row[0])
            name = row[1].strip()
            if code in areas:
                names = areas[code]
                names.add(name)
            else:
                names = set()
                names.add(name)
                areas[code] = names

        year += 1
    
    with open('./out_data/areas.csv', 'w+') as fp:
        fp.write('%s,%s,%s,%s\n' % ('行政编码', '区县', '市', '省'))
        for k in sorted(areas):
            #print(k, areas[k])
            # print(str(k)[:-2], str(k))
            if str(k)[-2:] == '00' and (str(k)[2:4] != '00' or str(k)[0:2] in ('11', '12', '31', '50', '71', '81', '82')):
                # print(k, areas[k])
                area_city = ''
            if str(k)[0:2] in ('11', '12', '31', '50', '71', '81', '82'):
                area_city_code = int(str(k)[0:2] + str('0000'))
                area_city = '|'.join(areas[area_city_code])
            elif str(k)[2:4] == '00' and str(k)[-2:] == '00':
                area_city = ''
            elif str(k)[2:4] != '00' and str(k)[-2:] == '00':
                area_city = '|'.join(areas[k])
            elif str(k)[2:4] != '00' and str(k)[-2:] != '00':
                area_city_code = int(str(k)[0:4] + '00')
                try:
                    area_city = '|'.join(areas[area_city_code])
                except:
                    print(area_city_code)
                    area_city = ''
            else:
                area_city = ''
            
            area_province_code = int(str(k)[0:2] + '0000')
            area_province = '|'.join(areas[area_province_code])

            fp.write('%d,%s,%s,%s\n' % (k, '|'.join(areas[k]), area_city, area_province))
    
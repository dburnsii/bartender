import json
import re

def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


drinks_json = open("drinks.json", "r").read()
drinks = json.loads(drinks_json)

for i in range(len(drinks)):
    for j in range(1,16):
        n_str = 'strIngredient' + str(j)
        m_str = 'strMeasure' + str(j)
        if drinks[i][m_str]:
            # shot(s)
            match = re.match(r'([\d/ ]+) shot', drinks[i][m_str])
            if match:
                # 1 shot = 44 ml
                vol = round(convert_to_float(match.group(1)) * 44)
                #print("Shot: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # ounces
            match = re.match(r'([\d/ \.]+) oz', drinks[i][m_str])
            if match:
                # 1 oz = 29.6 ml
                vol = round(convert_to_float(match.group(1)) * 29.6)
                #print("oz: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # milliliter
            match = re.match(r'([\d/ \.]+) ml', drinks[i][m_str])
            if match:
                # 1 ml = 1 ml
                vol = round(convert_to_float(match.group(1)))
                #print("ml: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # centiliter
            match = re.match(r'([\d/ \.]+) cl', drinks[i][m_str])
            if match:
                # 1 cl = 10 ml
                vol = round(convert_to_float(match.group(1)) * 10)
                #print("cl: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # Cups
            match = re.match(r'([\d/ \.]+) cup', drinks[i][m_str])
            if match:
                # 1 cup = 236.5 ml
                vol = round(convert_to_float(match.group(1)) * 236.5)
                #print("cups: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # tsp
            match = re.match(r'([\d/ \.]+) tsp', drinks[i][m_str])
            if match:
                # 1 tsp = 5 ml
                vol = round(convert_to_float(match.group(1)) * 5)
                #print("tsp: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # tbsp
            match = re.match(r'([\d/ \.]+) tb[l]?sp', drinks[i][m_str])
            if match:
                # 1 tbsp = 15 ml
                vol = round(convert_to_float(match.group(1)) * 15)
                #print("tbsp: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            # dash
            match = re.match(r'([\d/ \.]+) dash', drinks[i][m_str])
            if match:
                # 1 dash = 1 ml
                vol = round(convert_to_float(match.group(1)) * 15)
                #print("dash: " + str(vol) + " -> " + drinks[i][n_str])
                drinks[i][m_str] = vol
                continue
            else:
                print("No match: " + drinks[i][m_str] + " -> " + drinks[i][n_str])

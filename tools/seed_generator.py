import csv, random, datetime as dt

def rand_ts(day, hour):
    base = dt.datetime.strptime(day, "%Y-%m-%d")
    return (base + dt.timedelta(hours=hour, minutes=random.randint(-5, 15))).isoformat()+"Z"

def gen_delivery_facts(path):
    rows = []
    for d in ["2025-06-01","2025-06-02","2025-06-03"]:
        for cfc, spoke, carrier in [("CFC_2","Spoke_17","FastShip"),("CFC_2","Spoke_17","QuickMove"),("CFC_3","Spoke_21","FastShip")]:
            promised = rand_ts(d, 10)
            actual = rand_ts(d, 10)
            rows.append([actual, promised, "South", cfc, spoke, carrier])
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["delivery_ts","promised_ts","region","cfc","spoke","carrier"])
        w.writerows(rows)

def gen_finance_facts(path):
    rows = [
        ["2025-05-01","South","Online","Electronics",120000,90000],
        ["2025-05-01","South","Online","Home",80000,52000],
        ["2025-05-01","North","Retail","Electronics",60000,48000]
    ]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date","region","channel","product_category","revenue","cogs"])
        w.writerows(rows)

def gen_marketing_facts(path):
    rows = [
        ["2025-06-01","UK","Paid Social","Summer_24_core",5000,120],
        ["2025-06-01","UK","Search","Brand_Exact",3000,220],
        ["2025-06-08","UK","Paid Social","Summer_24_core",5200,95]
    ]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date","region","channel","campaign","acq_spend","new_customers"])
        w.writerows(rows)

if __name__ == "__main__":
    gen_delivery_facts("seeds/supply_chain/delivery_facts.sample.csv")
    gen_finance_facts("seeds/finance/finance_facts.sample.csv")
    gen_marketing_facts("seeds/marketing/marketing_facts.sample.csv")


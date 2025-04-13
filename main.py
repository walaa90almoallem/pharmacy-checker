
from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# قراءة البيانات من ملف CSV
data = pd.read_csv("sample_data.csv")

@app.get("/")
def read_root():
    return {"message": "البوت شغال! استخدم /check للتحقق من الطلب"}

@app.get("/check")
def check_order(
    pharmacy: str = Query(..., description="اسم أو كود الصيدلية"),
    product: str = Query(..., description="اسم أو رمز المستحضر"),
    quantity: int = Query(..., description="الكمية المطلوبة")
):
    match = data[
        ((data["اسم الصيدلية"] == pharmacy) | (data["CODE الصيدلية"] == pharmacy)) &
        ((data["اسم المستحضر"] == product) | (data["رمز المستحضر"] == product))
    ]
    if match.empty:
        return {"result": "❌ لم يتم العثور على تطابق في البيانات"}
    
    row = match.iloc[0]
    min_qty = row["الحد الادنى"]
    max_qty = row["الحد الاعلى"]

    if quantity < min_qty:
        return {"result": "❌ الطلب أقل من الحد الأدنى", "الحد الأدنى": int(min_qty)}
    elif quantity > max_qty:
        return {"result": "❌ الطلب أكبر من الحد الأعلى", "الحد الأعلى": int(max_qty)}
    else:
        return {"result": "✔️ الطلب مقبول ✅", "بين": f"{int(min_qty)} - {int(max_qty)}"}

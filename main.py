import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1467795764511113216/NfP4WUwvzgErpz82-VOuHh2PoHj2TkDa53874umM36-v38DNaAJTMh7N_1ENDow66TCE"
CHECK_INTERVAL = 60

ITEMS = [
    {"id": "110938549915721", "name": "Black Iron King of the Night", "url": "https://www.roblox.com/it/catalog/110938549915721/Black-Iron-King-of-the-Night"},
    {"id": "133965942144109", "name": "Purple Sparkle Time Fedora", "url": "https://www.roblox.com/it/catalog/133965942144109/Purple-Sparkle-Time-Fedora"}
]

price_history = {}

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)

def get_item_price(item_id):
    try:
        url = f"https://api.roblox.com/marketplace/productinfo?assetId={item_id}"
        response = requests.get(url, timeout=15)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        item_name = data.get("Name", "Unknown")
        is_limited = data.get("IsLimited") or data.get("IsLimitedUnique")
        
        if is_limited:
            resellers_url = f"https://economy.roblox.com/v1/assets/{item_id}/resellers?limit=10"
            resell_response = requests.get(resellers_url, timeout=15)
            
            if resell_response.status_code == 200:
                resell_data = resell_response.json()
                
                if resell_data.get("data") and len(resell_data["data"]) > 0:
                    prices = [r["price"] for r in resell_data["data"] if r.get("price")]
                    
                    if prices:
                        lowest_price = min(prices)
                        log(f"💎 {item_name} - {lowest_price:,} Robux")
                        return {"price": lowest_price, "name": item_name}
                
                return {"price": 0, "name": item_name}
        
        normal_price = data.get("PriceInRobux", 0)
        log(f"✓ {item_name} - {normal_price:,} Robux")
        return {"price": normal_price, "name": item_name}
            
    except Exception as e:
        log(f"❌ Errore: {str(e)}")
        return None

def send_discord(item, old_price, new_price):
    if old_price == new_price:
        return
        
    try:
        change = new_price - old_price
        color = 0xFF0000 if change > 0 else 0x00FF00
        emoji = "📈" if change > 0 else "📉"
        
        embed = {
            "title": f"{emoji} {item['name']}",
            "url": item["url"],
            "color": color,
            "fields": [
                {"name": "💰 Nuovo", "value": f"**{new_price:,} Robux**", "inline": True},
                {"name": "📊 Vecchio", "value": f"{old_price:,} Robux", "inline": True},
                {"name": "📈 Cambio", "value": f"{change:+,} Robux", "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        requests.post(WEBHOOK_URL, json={"embeds": [embed]}, timeout=10)
        log(f"✅ Notifica Discord inviata!")
    except:
        pass

def check():
    log("🔍 Controllo prezzi...")
    
    for item in ITEMS:
        info = get_item_price(item["id"])
        
        if info:
            new_price = info["price"]
            old_price = price_history.get(item["id"], {}).get("price")
            
            if old_price is None:
                log(f"🆕 Primo controllo: {new_price:,} Robux")
            elif old_price != new_price:
                log(f"💰 CAMBIO: {old_price:,} → {new_price:,}")
                send_discord(item, old_price, new_price)
            
            price_history[item["id"]] = info
        
        time.sleep(2)
    
    log("✅ Completato\n")

log("🎮 ROBLOX PRICE MONITOR")
log("🌐 Running on Render.com\n")
check()

while True:
    time.sleep(CHECK_INTERVAL)
    check()
```

Clicca **"Commit changes"**

---

## 📄 **File 2: requirements.txt**

Clicca **"Add file" → "Create new file"**

Nome file: `requirements.txt`

Copia:
```
requests==2.32.5
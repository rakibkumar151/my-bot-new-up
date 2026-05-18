import asyncio
import aiohttp
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import time
import json
import sys
import re
import sys
import asyncio
import aiohttp
import json
import time
import hashlib
import os
from aiohttp import web

# Fix Windows console emoji printing error
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# GLOBAL STORAGE
MENU_CACHE = {}
ACTIVE_ORDERS = {}
TOKEN_LIST = []
BOT_TOKEN = None
bot = None

# ==========================================
# 🌍 WORLDWIDE FLAGS DATABASE (FIXED)
# ==========================================
FLAGS = {
    "Afghanistan": "🇦🇫", "Albania": "🇦🇱", "Algeria": "🇩🇿", "Andorra": "🇦🇩", "Angola": "🇦🇴",
    "Argentina": "🇦🇷", "Armenia": "🇦🇲", "Australia": "🇦🇺", "Austria": "🇦🇹", "Azerbaijan": "🇦🇿",
    "Bahrain": "🇧🇭", "Bangladesh": "🇧🇩", "Barbados": "🇧🇧", "Belarus": "🇧🇾", "Belgium": "🇧🇪",
    "Belize": "🇧🇿", "Benin": "🇧🇯", "Bhutan": "🇧🇹", "Bolivia": "🇧🇴", "Bosnia": "🇧🇦",
    "Botswana": "🇧🇼", "Brazil": "🇧🇷", "Brunei": "🇧🇳", "Bulgaria": "🇧🇬", "Burkina Faso": "🇧🇫",
    "Burundi": "🇧🇮", "Cambodia": "🇰🇭", "Cameroon": "🇨🇲", "Canada": "🇨🇦", "Cape Verde": "🇨🇻",
    "Central African Rep": "🇨🇫", "Chad": "🇹🇩", "Chile": "🇨🇱", "China": "🇨🇳", "Colombia": "🇨🇴",
    "Comoros": "🇰🇲", "Congo": "🇨🇬", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷", "Cuba": "🇨🇺",
    "Cyprus": "🇨🇾", "Czech Republic": "🇨🇿", "Denmark": "🇩🇰", "Djibouti": "🇩🇯", "Dominica": "🇩🇲",
    "Dominican Republic": "🇩🇴", "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "El Salvador": "🇸🇻",
    "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷", "Estonia": "🇪🇪", "Ethiopia": "🇪🇹", "Fiji": "🇫🇯",
    "Finland": "🇫🇮", "France": "🇫🇷", "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Georgia": "🇬🇪",
    "Germany": "🇩🇪", "Ghana": "🇬🇭", "Greece": "🇬🇷", "Grenada": "🇬🇩", "Guatemala": "🇬🇹",
    
    # 🔥 GUINEA FIX (BOTH NAMES ADDED) 🔥
    "Guinea": "🇬🇳", 
    "Guinea Republic": "🇬🇳", 
    
    "Guinea-Bissau": "🇬🇼", "Guyana": "🇬🇾", "Haiti": "🇭🇹", "Honduras": "🇭🇳",
    "Hong Kong": "🇭🇰", "Hungary": "🇭🇺", "Iceland": "🇮🇸", "India": "🇮🇳", "Indonesia": "🇮🇩",
    "Iran": "🇮🇷", "Iraq": "🇮🇶", "Ireland": "🇮🇪", "Israel": "🇮🇱", "Italy": "🇮🇹",
    "Ivory Coast": "🇨🇮", "Jamaica": "🇯🇲", "Japan": "🇯🇵", "Jordan": "🇯🇴", "Kazakhstan": "🇰🇿",
    "Kenya": "🇰🇪", "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬", "Laos": "🇱🇦", "Latvia": "🇱🇻",
    "Lebanon": "🇱🇧", "Lesotho": "🇱🇸", "Liberia": "🇱🇷", "Libya": "🇱🇾", "Liechtenstein": "🇱🇮",
    "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺", "Macau": "🇲🇴", "Macedonia": "🇲🇰", "Madagascar": "🇲🇬",
    "Malawi": "🇲🇼", "Malaysia": "🇲🇾", "Maldives": "🇲🇻", "Mali": "🇲🇱", "Malta": "🇲🇹",
    "Mauritania": "🇲🇷", "Mauritius": "🇲🇺", "Mexico": "🇲🇽", "Moldova": "🇲🇩", "Monaco": "🇲🇨",
    "Mongolia": "🇲🇳", "Montenegro": "🇲🇪", "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Myanmar": "🇲🇲",
    "Namibia": "🇳🇦", "Nepal": "🇳🇵", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿", "Nicaragua": "🇳🇮",
    "Niger": "🇳🇪", "Nigeria": "🇳🇬", "North Korea": "🇰🇵", "Norway": "🇳🇴", "Oman": "🇴🇲",
    "Pakistan": "🇵🇰", "Palestine": "🇵🇸", "Panama": "🇵🇦", "Papua New Guinea": "🇵🇬", "Paraguay": "🇵🇾",
    "Peru": "🇵🇪", "Philippines": "🇵🇭", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦",
    "Romania": "🇷🇴", "Russia": "🇷🇺", "Rwanda": "🇷🇼", "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳",
    "Serbia": "🇷🇸", "Seychelles": "🇸🇨", "Sierra Leone": "🇸🇱", "Singapore": "🇸🇬", "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮", "Somalia": "🇸🇴", "South Africa": "🇿🇦", "South Korea": "🇰🇷", "South Sudan": "🇸🇸",
    "Spain": "🇪🇸", "Sri Lanka": "🇱🇰", "Sudan": "🇸🇩", "Suriname": "🇸🇷", "Swaziland": "🇸🇿",
    "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "Syria": "🇸🇾", "Taiwan": "🇹🇼", "Tajikistan": "🇹🇯",
    "Tanzania": "🇹🇿", "Thailand": "🇹🇭", "Timor-Leste": "🇹🇱", "Togo": "🇹🇬", "Tunisia": "🇹🇳",
    "Turkey": "🇹🇷", "Turkmenistan": "🇹🇲", "Uganda": "🇺🇬", "Ukraine": "🇺🇦", "UAE": "🇦🇪",
    "UK": "🇬🇧", "USA": "🇺🇸", "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿", "Venezuela": "🇻🇪",
    "Vietnam": "🇻🇳", "Yemen": "🇾🇪", "Zambia": "🇿🇲", "Zimbabwe": "🇿🇼"
}

# ==========================================
# 🔢 PREFIX DATABASE (ALL COUNTRY CODES)
# ==========================================
PREFIX_DB = {
    "93": "Afghanistan", "355": "Albania", "213": "Algeria", "376": "Andorra", "244": "Angola",
    "54": "Argentina", "374": "Armenia", "61": "Australia", "43": "Austria", "994": "Azerbaijan",
    "973": "Bahrain", "880": "Bangladesh", "1246": "Barbados", "375": "Belarus", "32": "Belgium",
    "501": "Belize", "229": "Benin", "975": "Bhutan", "591": "Bolivia", "387": "Bosnia",
    "267": "Botswana", "55": "Brazil", "673": "Brunei", "359": "Bulgaria", "226": "Burkina Faso",
    "257": "Burundi", "855": "Cambodia", "237": "Cameroon", "1": "USA", "238": "Cape Verde",
    "236": "Central African Rep", "235": "Chad", "56": "Chile", "86": "China", "57": "Colombia",
    "269": "Comoros", "242": "Congo", "506": "Costa Rica", "385": "Croatia", "53": "Cuba",
    "357": "Cyprus", "420": "Czech Republic", "45": "Denmark", "253": "Djibouti", "593": "Ecuador",
    "20": "Egypt", "503": "El Salvador", "240": "Equatorial Guinea", "291": "Eritrea", "372": "Estonia",
    "251": "Ethiopia", "679": "Fiji", "358": "Finland", "33": "France", "241": "Gabon",
    "220": "Gambia", "995": "Georgia", "49": "Germany", "233": "Ghana", "30": "Greece",
    "502": "Guatemala", 
    
    "224": "Guinea", # 🔥 Prefix for Guinea
    
    "245": "Guinea-Bissau", "592": "Guyana", "509": "Haiti",
    "504": "Honduras", "852": "Hong Kong", "36": "Hungary", "354": "Iceland", "91": "India",
    "62": "Indonesia", "98": "Iran", "964": "Iraq", "353": "Ireland", "972": "Israel",
    "39": "Italy", "225": "Ivory Coast", "1876": "Jamaica", "81": "Japan", "962": "Jordan",
    "7": "Russia", "77": "Kazakhstan", "254": "Kenya", "965": "Kuwait", "996": "Kyrgyzstan",
    "856": "Laos", "371": "Latvia", "961": "Lebanon", "266": "Lesotho", "231": "Liberia",
    "218": "Libya", "423": "Liechtenstein", "370": "Lithuania", "352": "Luxembourg", "853": "Macau",
    "389": "Macedonia", "261": "Madagascar", "265": "Malawi", "60": "Malaysia", "960": "Maldives",
    "223": "Mali", "356": "Malta", "222": "Mauritania", "230": "Mauritius", "52": "Mexico",
    "373": "Moldova", "377": "Monaco", "976": "Mongolia", "382": "Montenegro", "212": "Morocco",
    "258": "Mozambique", "95": "Myanmar", "264": "Namibia", "977": "Nepal", "31": "Netherlands",
    "64": "New Zealand", "505": "Nicaragua", "227": "Niger", "234": "Nigeria", "850": "North Korea",
    "47": "Norway", "968": "Oman", "92": "Pakistan", "970": "Palestine", "507": "Panama",
    "675": "Papua New Guinea", "595": "Paraguay", "51": "Peru", "63": "Philippines", "48": "Poland",
    "351": "Portugal", "974": "Qatar", "40": "Romania", "7": "Russia", "250": "Rwanda",
    "966": "Saudi Arabia", "221": "Senegal", "381": "Serbia", "248": "Seychelles", "232": "Sierra Leone",
    "65": "Singapore", "421": "Slovakia", "386": "Slovenia", "252": "Somalia", "27": "South Africa",
    "82": "South Korea", "211": "South Sudan", "34": "Spain", "94": "Sri Lanka", "249": "Sudan",
    "597": "Suriname", "268": "Swaziland", "46": "Sweden", "41": "Switzerland", "963": "Syria",
    "886": "Taiwan", "992": "Tajikistan", "255": "Tanzania", "66": "Thailand", "670": "Timor-Leste",
    "228": "Togo", "216": "Tunisia", "90": "Turkey", "993": "Turkmenistan", "256": "Uganda",
    "380": "Ukraine", "971": "UAE", "44": "UK", "1": "USA", "598": "Uruguay",
    "998": "Uzbekistan", "58": "Venezuela", "84": "Vietnam", "967": "Yemen", "260": "Zambia",
    "263": "Zimbabwe"
}

# ==========================================
# ⚙️ HELPER: DETECT COUNTRY
# ==========================================

def detect_country(full_num):
    """
    Detects country name and flag from phone number prefix.
    Logic: Checks longest prefix first (e.g., checks 1876 before 1).
    """
    full_num = str(full_num)
    
    # Sort prefixes by length (Longest first) to avoid conflict
    # Example: 1876 (Jamaica) vs 1 (USA)
    sorted_prefixes = sorted(PREFIX_DB.keys(), key=len, reverse=True)
    
    for prefix in sorted_prefixes:
        if full_num.startswith(prefix):
            name = PREFIX_DB[prefix]
            return name, FLAGS.get(name, "🌍")
            
    return "Unknown", "🌍"



# ==========================================
#   🔥 CONFIGURATION AREA
# ==========================================

LIVE_GROUP_ID = -1003211549283   # <--- লাইভ ফিড গ্রুপ ID
FORCE_GROUP_ID = -1003211549283  # <--- মেইন গ্রুপ ID (যেখানে মেম্বার চেক হবে)

# এই লিংকগুলো বাটনে সেট হবে
FORCE_LINK = "https://t.me/+u6r8dxTcekVlZGU9"      # <--- Channel/Group Link
BOT_LINK = "https://t.me/Riyad2992"          # <--- Bot Link (e.g. https://t.me/FastOTPBot)
# ==========================================
#   🔥 CONFIGURATION AREA (SECURE)
# ==========================================

MY_PROXY_URL = "https://little-breeze-a466.uumarrakom.workers.dev"

# API ENDPOINTS
URL_CONFIG = f"{MY_PROXY_URL}/get-secret-config"
URL_CONSOLE = f"{MY_PROXY_URL}/mapi/v1/mdashboard/console/info"
URL_BUY = f"{MY_PROXY_URL}/mapi/v1/mdashboard/getnum/number"
URL_STATUS = f"{MY_PROXY_URL}/mapi/v1/mdashboard/getnum/info"

# 🔥 নতুন HEADERS (সাথে পাসওয়ার্ড যোগ করা হলো)
HEADERS = {
    "Host": "little-breeze-a466.uumarrakom.workers.dev",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    
    # 🔒 এই সেই সিক্রেট চাবি (এটা না থাকলে Cloudflare ঢুকতে দিবে না)
    "X-My-Bot-Secret": "Rakib123456", 
    
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}

# ==========================================
#   📡 SYSTEM UTILS
# ==========================================

# (বাকি সব কোড আগের মতোই থাকবে, কারণ তারা এখন গ্লোবাল HEADERS ব্যবহার করছে)

# গ্লোবাল ভেরিয়েবল
BOT_TOKEN = ""
TOKEN_LIST = []

# ==========================================
#   📡 SYSTEM UTILS (RESTORE & LOAD)
# ==========================================

# 1. কনফিগ লোড ফাংশন
async def load_configurations():
    global BOT_TOKEN, TOKEN_LIST
    #print("⚠️ Connection Error")

    connector = aiohttp.TCPConnector(ssl=False)
    
    # এখানে global HEADERS ব্যবহার করা হচ্ছে
    async with aiohttp.ClientSession(connector=connector, headers=HEADERS) as session:
        try:
            async with session.get(URL_CONFIG, timeout=30) as r:
                if r.status == 200:
                    data = json.loads(await r.text())
                    BOT_TOKEN = data.get("bot_token", "").strip()
                    TOKEN_LIST = data.get("mnit_tokens", [])
                    #print("✅ Config Loaded Successfully!")
                else:
                    print(f"⚠️ Cloudflare Blocked Config! Status: {r.status}")
        except Exception as e:
            print(f"⚠️ Network Error: {e}")
            sys.exit()

    if not BOT_TOKEN or not TOKEN_LIST:
        print("⚠️ CRITICAL: Missing Tokens!")
        sys.exit()

# 2. পুরানো সেশন রিস্টোর ফাংশন (যেখানে সমস্যা হচ্ছিল)
async def check_server_history(session, token):
    try:
        # টোকেন হেডারে অ্যাড করা হলো
        local_headers = HEADERS.copy()
        local_headers["Authorization"] = f"Bearer {token}"
        
        # SSL False করে রিকোয়েস্ট পাঠানো হচ্ছে
        async with session.get(URL_CONSOLE, headers=local_headers, ssl=False, timeout=10) as r:
            if r.status == 200:
                data = await r.json()
                if data.get("code") == 200:
                    return {"token": token, "num": data["data"]["mobile_no"]}
    except:
        pass
    return None

async def restore_old_sessions():
    #print("♻️ Restoring sessions...")
    connector = aiohttp.TCPConnector(ssl=False)
    
    # এখানেও global HEADERS ব্যবহার করা হচ্ছে
    async with aiohttp.ClientSession(connector=connector, headers=HEADERS) as session:
        tasks = [check_server_history(session, t) for t in TOKEN_LIST]
        results = await asyncio.gather(*tasks)
        
        count = 0
        for res in results:
            if res:
                # ACTIVE_ORDERS ডিকশনারি আপনার মেইন কোডে আছে ধরে নিচ্ছি
                if 'ACTIVE_ORDERS' in globals():
                    ACTIVE_ORDERS[res['num']] = res
                count += 1
        # print(f"✅ Restored {count} active sessions.")

# ==========================================
#   🔒 FORCE JOIN CHECKER
# ==========================================

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(FORCE_GROUP_ID, user_id)
        if member.status in ['creator', 'administrator', 'member', 'restricted']:
            return True
        return False
    except:
        return True # If bot isn't admin, allow access to prevent stuck

async def send_join_alert(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📢 JOIN GROUP", url=FORCE_LINK))
    kb.add(types.InlineKeyboardButton("✅ I HAVE JOINED", callback_data="check_join"))
    await bot.reply_to(message, 
        "🚫 **ACCESS DENIED!**\n\n"
        "You must join our group to use this bot.\n"
        "বট ব্যবহার করতে আমাদের গ্রুপে জয়েন করুন।", 
        reply_markup=kb, parse_mode='Markdown'
    )

# ==========================================
#   ⚙️ HELPER FUNCTIONS
# ==========================================

def get_flag(country_name):
    return FLAGS.get(country_name, "🌍")

def mask_number(full_num):
    if len(full_num) > 5:
        return full_num[:5] + "x" * (len(full_num) - 5)
    return full_num[:2] + "xxxx"

def mask_message_content(text):
    matches = re.findall(r'\b\d{4,8}\b', text)
    masked_text = text
    for code in matches:
        if len(code) >= 4:
            masked_code = code[:2] + 'x' * (len(code) - 2)
            masked_text = masked_text.replace(code, masked_code)
    return masked_text

# ==========================================
#   ⚔️ CORE ENGINE (UPDATED BUY LOGIC)
# ==========================================

async def restore_old_sessions():
    print("⚠️Something Error")
    async with aiohttp.ClientSession() as session:
        tasks = [check_server_history(session, t) for t in TOKEN_LIST]
        results = await asyncio.gather(*tasks)
        for res in results:
            if res: ACTIVE_ORDERS[res['num']] = res

async def check_server_history(session, token):
    try:
        h = HEADERS.copy()
        h['mauthtoken'] = token
        async with session.get(URL_CONSOLE, headers=h, timeout=8) as resp:
            if resp.status == 200:
                data = await resp.json()
                for log in data.get('data', {}).get('logs', []):
                    if str(log.get('status')).lower() in ['pending', 'processing']:
                        return {
                            'num': log.get('number'), 
                            'chat_id': None, 
                            'token': token, 
                            'start': time.time(),
                            'country': log.get('country', 'Unknown')
                        }
    except: pass
    return None

async def buy_attack_single(session, token, payload):
    h = HEADERS.copy()
    h['mauthtoken'] = token
    try:
        async with session.post(URL_BUY, headers=h, json=payload, timeout=5) as resp:
            if resp.status == 200:
                data = (await resp.json()).get('data', {})
                if str(data.get('status')).lower() == 'pending':
                    return {"success": True, "token": token, "num": data.get('full_number', '').replace('+', '')}
    except: pass
    return None

# এই ফাংশনটি রিপ্লেস করুন
# এই ফাংশনটি দিয়ে আগেরটি রিপ্লেস করুন
# এই ফাংশনটি কপি করে আগের shotgun_buy এর জায়গায় বসান
# এই ফাংশনটি পুরোটা কপি করে রিপ্লেস করুন
async def shotgun_buy(chat_id, country, rng, message_to_edit=None):
    payload = {"range": rng, "is_national": False, "remove_plus": False}
    
    if not message_to_edit:
        msg_wait = await bot.send_message(chat_id, "⏳ **Finding...**")
    else:
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit.message_id, text="🔄 **Exchanging...**", parse_mode='Markdown')
        except: pass

    async with aiohttp.ClientSession() as session:
        tasks = [buy_attack_single(session, t, payload) for t in TOKEN_LIST]
        results = await asyncio.gather(*tasks)
        winner = next((res for res in results if res and res['success']), None)
        
        if winner:
            full_num = winner['num']
            
            # 🔥 NEW: অটোমেটিক দেশ ডিটেকশন
            detected_name, detected_flag = detect_country(full_num)
            
            # যদি ডিটেক্ট না হয়, তবে মেনু থেকে সিলেক্ট করা নামই থাকবে
            if detected_name == "Unknown":
                final_country = country
                final_flag = get_flag(country)
            else:
                final_country = detected_name
                final_flag = detected_flag
            
            ACTIVE_ORDERS[full_num] = {
                'num': full_num,
                'chat_id': chat_id,
                'token': winner['token'],
                'start': time.time(),
                'country': final_country  # সেভ করা হলো সঠিক নাম
            }
            
            kb = types.InlineKeyboardMarkup()
            btn_change = types.InlineKeyboardButton("🔄 Change", callback_data=f"buy|{country}|{rng}")
            btn_clear = types.InlineKeyboardButton("🗑️ Clear", callback_data="clean_me")
            kb.row(btn_change, btn_clear)
            
            msg_text = (
                f"✅ **Assigned:** `{full_num}`\n"
                f"🌍 {final_flag} {final_country}\n"
                f"⏳ **Waiting for OTP...**"
            )

            if message_to_edit:
                try:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit.message_id, text=msg_text, parse_mode='Markdown', reply_markup=kb)
                except: pass
            else:
                await bot.delete_message(chat_id, msg_wait.message_id)
                await bot.send_message(chat_id, msg_text, parse_mode='Markdown', reply_markup=kb)

        else:
            fail_text = "❌ **Stock Out!** Try again."
            kb_fail = types.InlineKeyboardMarkup()
            btn_retry = types.InlineKeyboardButton("🔄 Retry", callback_data=f"buy|{country}|{rng}")
            kb_fail.row(btn_retry)
            
            if message_to_edit:
                try:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit.message_id, text=fail_text, parse_mode='Markdown', reply_markup=kb_fail)
                except: pass
            else:
                await bot.delete_message(chat_id, msg_wait.message_id)
                await bot.send_message(chat_id, fail_text, parse_mode='Markdown', reply_markup=kb_fail)
# ==========================================
#   👀 OTP MONITOR (UPDATED FOR GROUP BUTTONS)
# ==========================================

# এই ফাংশনটি রিপ্লেস করুন
async def otp_monitor_loop():
    #print("👀 OTP Monitor Started...")
    async with aiohttp.ClientSession() as session:
        while True:
            if not ACTIVE_ORDERS:
                await asyncio.sleep(1)
                continue
            
            current_list = list(ACTIVE_ORDERS.values())
            
            for order in current_list:
                full_num = order['num']
                country_name = order.get('country', 'Unknown')
                flag = get_flag(country_name)

                if time.time() - order['start'] > 180:
                    if full_num in ACTIVE_ORDERS: del ACTIVE_ORDERS[full_num]
                    continue

                try:
                    h = HEADERS.copy()
                    h['mauthtoken'] = order['token']
                    async with session.get(f"{URL_STATUS}?search={full_num}", headers=h, timeout=5) as resp:
                        if resp.status == 200:
                            js = await resp.json()
                            items = js.get('data', {}).get('numbers', [])
                            if items:
                                item = items[0]
                                status = str(item.get('status')).lower()
                                
                                if status == 'success':
                                    otp_raw = item.get('otp') or item.get('message') or ""
                                    code = "".join(filter(str.isdigit, str(otp_raw)))
                                    
                                    # 1. ইউজার মেসেজ
                                    msg_user = (
                                        f"✅ **OTP RECEIVED!**\n"
                                        f"🏳️ {flag} {country_name}\n"
                                        f"📱 `{full_num}`\n"
                                        f"🔢 Code: `{code}`\n"
                                        f"📩 Row: `{otp_raw}`"
                                    )
                                    
                                    if order['chat_id']:
                                        # ইউজার চ্যাট ক্লিন রাখার জন্য এখানেও বাটন দিতে পারেন
                                        kb_user = types.InlineKeyboardMarkup()
                                        kb_user.row(types.InlineKeyboardButton("🗑️ Clear", callback_data="clean_me"))
                                        await bot.send_message(order['chat_id'], msg_user, parse_mode='Markdown', reply_markup=kb_user)
                                    
                                    # 2. লাইভ ফিড (গ্রুপ মেসেজ)
                                    if LIVE_GROUP_ID:
                                        masked_num = mask_number(full_num)
                                        masked_msg = mask_message_content(otp_raw)
                                        
                                        live_msg = (
                                            f"🔴 **LIVE OTP FEED**\n"
                                            f"🌍 {flag} {country_name}\n"
                                            f"📱 Num: `{masked_num}`\n"
                                            f"🔢 Code: `xxxxxx`\n"
                                            f"📩 Msg: `{masked_msg}`\n"
                                            f"🤖 Bot: FastBot"
                                        )

                                        # 🔥 পরিবর্তন ২: বাটন লেআউট ফিক্স (Bot Link & Channel Link পাশাপাশি)
                                        kb_group = types.InlineKeyboardMarkup()
                                        b1 = types.InlineKeyboardButton("👽 Admin Contact", url=BOT_LINK)
                                        b2 = types.InlineKeyboardButton("📢 Main Channel", url=FORCE_LINK)
                                        
                                        # .row() ব্যবহার করার কারণে এগুলো স্ক্রিন সাইজ অনুযায়ী অটো অ্যাডজাস্ট হবে
                                        kb_group.row(b1, b2)
                                        
                                        try:
                                            await bot.send_message(LIVE_GROUP_ID, live_msg, parse_mode='Markdown', reply_markup=kb_group)
                                        except: pass

                                    if full_num in ACTIVE_ORDERS: del ACTIVE_ORDERS[full_num]
                                
                                elif status in ['failed', 'canceled']:
                                    if full_num in ACTIVE_ORDERS: del ACTIVE_ORDERS[full_num]
                except: pass
            await asyncio.sleep(1.5)
# ==========================================
#   📡 MENU & HANDLERS
# ==========================================

# এই ফাংশনটি পুরোটা কপি করে আগের menu_sync_loop এর জায়গায় বসান
async def menu_sync_loop():
    #print("📡 Menu Syncer Started...")
    
    # যে শব্দগুলো আপনি মেনুতে চান না (Block List)
    BLACKLIST_WORDS = ["postpaid", "prepaid", "unknown", "test", "demo"]

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # প্রতিবার র‍্যান্ডম টোকেন দিয়ে চেক করবে
                token = TOKEN_LIST[int(time.time()) % len(TOKEN_LIST)]
                h = HEADERS.copy()
                h['mauthtoken'] = token
                
                async with session.get(URL_CONSOLE, headers=h, timeout=6) as resp:
                    if resp.status == 200:
                        js = await resp.json()
                        logs = js.get('data', {}).get('logs', [])
                        temp = {}
                        
                        for log in logs:
                            app_name = str(log.get('app_name', '')).lower()
                            country_name = str(log.get('country', '')).strip()
                            
                            # ১. শুধুমাত্র ফেইসবুক রিলেটেড সার্ভিস নিবে
                            if "face" in app_name:
                                
                                # ২. যদি দেশের নাম 'PostPaid' বা ব্ল্যাকলিস্টে থাকে, সেটা বাদ দিবে
                                if any(bad_word in country_name.lower() for bad_word in BLACKLIST_WORDS):
                                    continue
                                
                                # ৩. ভ্যালিড দেশ হলে লিস্টে অ্যাড করবে
                                temp[country_name] = log.get('number')
                        
                        # যদি ভ্যালিড ডাটা পায়, তবেই মেনু আপডেট করবে
                        if temp:
                            MENU_CACHE.clear()
                            MENU_CACHE.update(temp)
                            
            except Exception as e:
                pass
                
            # ৮ সেকেন্ড পর পর চেক করবে
            await asyncio.sleep(8)

# ==========================================
#   🌐 WEB SERVER FOR RENDER & UPTIMEROBOT
# ==========================================
async def handle_ping(request):
    return web.Response(text="Bot is running! UptimeRobot can ping this.")

async def web_server():
    try:
        app = web.Application()
        app.router.add_get('/', handle_ping)
        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.environ.get("PORT", 8000))
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        while True:
            await asyncio.sleep(3600)
    except Exception as e:
        pass

async def main():
    global bot
    await load_configurations()
    bot = AsyncTeleBot(BOT_TOKEN)
    
    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        if not await check_subscription(message.from_user.id):
            await send_join_alert(message)
            return
        
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton("🚀 FAST MENU 🚀"), types.KeyboardButton("🧹 CLEAR CHAT"))
        await bot.reply_to(message, "⚡ **System Online!**", reply_markup=kb)

    @bot.message_handler(func=lambda m: m.text == "🚀 FAST MENU 🚀")
    async def send_menu(message):
        if not await check_subscription(message.from_user.id):
            await send_join_alert(message)
            return

        if not MENU_CACHE:
            await bot.reply_to(message, "⚠️ **Syncing...** Wait 2s.")
            return
        
        mk = types.InlineKeyboardMarkup(row_width=2)
        btns = []
        for c, r in list(MENU_CACHE.items())[:24]:
             flag = get_flag(c)
             btns.append(types.InlineKeyboardButton(f"{flag} {c}", callback_data=f"buy|{c}|{r}"))
        mk.add(*btns)
        await bot.reply_to(message, "🌍 **Select Country:**", reply_markup=mk)

    @bot.message_handler(func=lambda m: m.text == "🧹 CLEAR CHAT")
    async def clear_chat_btn(message):
        try:
            current_id = message.message_id
            for i in range(current_id, current_id - 6, -1):
                try:
                    await bot.delete_message(message.chat.id, i)
                except: pass
            msg = await bot.send_message(message.chat.id, "🧹 **Chat Cleared!**")
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, msg.message_id)
        except: pass

    # NEW: Single Message Delete Button Callback
    @bot.callback_query_handler(func=lambda call: call.data == "clean_me")
    async def callback_clean_one(call):
        try:
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass

    @bot.callback_query_handler(func=lambda call: call.data.startswith('buy|'))
    async def handle_buy(call):
        if not await check_subscription(call.from_user.id):
            await bot.answer_callback_query(call.id, "❌ Join Group First!")
            await send_join_alert(call.message)
            return

        await bot.answer_callback_query(call.id, "🚀 Processing...")
        _, c, r = call.data.split('|')
        
        # LOGIC: যদি মেসেজে "Assigned" থাকে তার মানে এটি Change Request, তাই মেসেজ এডিট হবে।
        # আর যদি "Select Country" থাকে তার মানে এটি Menu Request, তাই নতুন মেসেজ হবে।
        
        is_change_request = "Assigned" in call.message.text or "Stock Out" in call.message.text
        
        if is_change_request:
            # Edit existing message (No New Box)
            asyncio.create_task(shotgun_buy(call.message.chat.id, c, r, message_to_edit=call.message))
        else:
            # New Message
            asyncio.create_task(shotgun_buy(call.message.chat.id, c, r, message_to_edit=None))

    @bot.callback_query_handler(func=lambda call: call.data == "check_join")
    async def recheck_join(call):
        if await check_subscription(call.from_user.id):
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.answer_callback_query(call.id, "✅ Verified!")
            await send_welcome(call.message)
        else:
            await bot.answer_callback_query(call.id, "❌ Not Joined Yet!", show_alert=True)

    await restore_old_sessions()
    asyncio.create_task(otp_monitor_loop())
    asyncio.create_task(menu_sync_loop())
    asyncio.create_task(web_server())
    
    #print("⚠️ Connection Error")
    while True:
        try:
            await bot.polling(non_stop=True, timeout=90)
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random

def run_news():
    # مصدر أخبار الرياضة
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك الربحي من Adsterra (استخدم نفس الرابط أو أنشئ Direct Link جديد)
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # عناوين شريط الأخبار الرياضية
        breaking_titles = " ⚽ ".join([item.title.text for item in items[:10]])

        news_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            
            # كرت الخبر الرياضي
            news_html += f'''
            <div class="sport-card">
                <a href="{my_direct_link}" target="_blank" class="card-link">
                    <div class="img-box">
                        <img src="{img_url}" loading="lazy">
                        <span class="live-tag">مباشر ⚽</span>
                    </div>
                    <div class="card-body">
                        <h2 class="card-title">{title}</h2>
                    </div>
                </a>
                <div class="card-footer">
                    <a href="{news_url}" target="_blank" class="read-more">التفاصيل الكاملة</a>
                </div>
            </div>'''
            
            # مربع إعلاني "توقع واربح" أو "تحميل" بعد كل 3 أخبار
            if (i + 1) % 3 == 0:
                ad_imgs = ["https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500", "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=500"]
                news_html += f'''
                <div class="sport-card ad-card">
                    <a href="{my_direct_link}" target="_blank" class="card-link">
                        <div class="img-box">
                            <img src="{random.choice(ad_imgs)}">
                            <span class="ad-tag">إعلان</span>
                        </div>
                        <div class="card-body">
                            <h2 class="card-title" style="color:#27ae60;">توقع نتائج المباريات اليوم واربح جوائز فورية!</h2>
                            <div class="ad-btn">اشترك الآن مجاناً</div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال سبورت | Alnidal Sport</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --sp-green: #27ae60; --sp-blue: #2c3e50; --sp-red: #e74c3c; }}
        body {{ background: #f4f4f4; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 60px; }}
        header {{ background: var(--sp-blue); color: white; padding: 15px 5%; border-bottom: 5px solid var(--sp-green); position: sticky; top:0; z-index:1000; display:flex; justify-content:space-between; align-items:center; }}
        .logo {{ font-size: 24px; font-weight: 900; }}
        .logo span {{ color: var(--sp-green); }}
        .grid {{ max-width: 1200px; margin: 20px auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; padding: 0 15px; }}
        .sport-card {{ background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; }}
        .img-box {{ position: relative; height: 180px; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
        .live-tag {{ position: absolute; top: 10px; right: 10px; background: var(--sp-red); color: white; padding: 3px 10px; font-size: 12px; border-radius: 5px; animation: pulse 1.5s infinite; }}
        @keyframes pulse {{ 0%{{opacity:1;}} 50%{{opacity:0.5;}} 100%{{opacity:1;}} }}
        .card-body {{ padding: 15px; flex-grow: 1; }}
        .card-title {{ font-size: 16px; font-weight: 700; margin: 0; color: #333; line-height: 1.5; }}
        .card-footer {{ background: #f9f9f9; padding: 10px; border-top: 1px solid #eee; }}
        .read-more {{ font-size: 12px; color: var(--sp-blue); text-decoration: none; font-weight: bold; }}
        .ad-btn {{ background: var(--sp-green); color: white; text-align: center; padding: 8px; margin-top: 10px; border-radius: 5px; font-weight: bold; }}
        .ad-tag {{ position: absolute; top: 10px; left: 10px; background: #3498db; color: white; padding: 2px 8px; font-size: 10px; border-radius: 3px; }}
        .card-link {{ text-decoration: none; color: inherit; }}
        
        .ticker {{ position: fixed; bottom: 0; width: 100%; background: var(--sp-blue); color: white; height: 45px; display: flex; align-items: center; border-top: 3px solid var(--sp-green); }}
        .ticker-label {{ background: var(--sp-green); padding: 0 20px; height: 100%; display: flex; align-items: center; font-weight: 900; z-index: 2; }}
        .ticker-text {{ white-space: nowrap; animation: move 50s linear infinite; padding-right: 100%; font-size: 14px; }}
        @keyframes move {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <div class="logo">النضال <span>سبورت</span> ⚽</div>
        <div style="font-size: 12px;">تحديث: {now}</div>
    </header>
    <div class="grid">{news_html}</div>
    <div class="ticker">
        <div class="ticker-label">أهم النتائج</div>
        <div class="ticker-text">{breaking_titles}</div>
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()

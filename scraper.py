import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        breaking_titles = " ⚽ ".join([item.title.text for item in items[:12]])

        news_html = ""
        for i, item in enumerate(items[:20]):
            title = item.title.text
            news_url = item.link.text
            
            # محاولة جلب الفيديو أو الصورة
            media_content = item.find('enclosure')
            media_url = media_content.get('url') if media_content else ""
            media_type = media_content.get('type') if media_content else ""
            
            # التمييز بين الفيديو والصورة
            is_video = "video" in media_type or media_url.endswith(('.mp4', '.m4v'))
            
            display_media = ""
            if is_video:
                display_media = f'''
                <div class="video-container">
                    <video muted loop autoplay playsinline poster="https://via.placeholder.com/600x400/1e272e/ffffff?text=Video+Loading...">
                        <source src="{media_url}" type="video/mp4">
                    </video>
                    <span class="video-badge">فيديو 🎬</span>
                </div>'''
            else:
                img_src = media_url if media_url else "https://via.placeholder.com/600x400/2c3e50/ffffff?text=Alnidal+Sport"
                display_media = f'''
                <div class="img-box">
                    <img src="{img_src}" loading="lazy">
                    <span class="live-tag">مباشر ⚽</span>
                </div>'''

            news_html += f'''
            <div class="sport-card">
                <a href="{my_direct_link}" target="_blank" class="card-link">
                    {display_media}
                    <div class="card-body">
                        <h2 class="card-title">{title}</h2>
                    </div>
                </a>
                <div class="card-footer">
                    <a href="{news_url}" target="_blank" class="read-more">مشاهدة المصدر 🔗</a>
                </div>
            </div>'''
            
            # إعلان رياضي فخم بعد كل 4 عناصر
            if (i + 1) % 4 == 0:
                ad_imgs = [
                    "https://cdn.pixabay.com/photo/2016/05/20/21/57/football-1406106_1280.jpg",
                    "https://cdn.pixabay.com/photo/2016/11/29/02/05/audience-1866738_1280.jpg"
                ]
                news_html += f'''
                <div class="sport-card ad-card">
                    <a href="{my_direct_link}" target="_blank" class="card-link">
                        <div class="img-box">
                            <img src="{random.choice(ad_imgs)}">
                            <span class="ad-tag">هدايا 🎁</span>
                        </div>
                        <div class="card-body">
                            <h2 class="card-title" style="color:#27ae60; text-align:center;">🏆 مـسابقة الـيوم: اضغط هنا للمشاركة في السحب الأسبوعي!</h2>
                            <div class="ad-btn">اشترك الآن</div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال سبورت | Alnidal Sport TV</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --sp-green: #27ae60; --sp-blue: #1e272e; --sp-red: #ef5350; }}
        body {{ background: #000; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 70px; color: white; }}
        
        header {{ background: var(--sp-blue); color: white; padding: 15px 5%; border-bottom: 3px solid var(--sp-green); position: sticky; top:0; z-index:1000; display:flex; justify-content:space-between; align-items:center; }}
        .logo {{ font-size: 24px; font-weight: 900; }}
        .logo span {{ color: var(--sp-green); }}

        .grid {{ max-width: 1200px; margin: 10px auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; padding: 0 10px; }}
        
        .sport-card {{ background: #111; border-radius: 15px; overflow: hidden; display: flex; flex-direction: column; border: 1px solid #222; }}
        
        .img-box, .video-container {{ position: relative; height: 350px; overflow: hidden; background: #000; }}
        .img-box img, .video-container video {{ width: 100%; height: 100%; object-fit: cover; }}
        
        .video-badge {{ position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); color: #fff; padding: 5px 12px; border-radius: 5px; font-size: 12px; }}
        .live-tag {{ position: absolute; top: 10px; right: 10px; background: var(--sp-red); color: white; padding: 4px 12px; font-size: 12px; border-radius: 5px; animation: blink 1.2s infinite; }}
        @keyframes blink {{ 0%{{opacity:1;}} 50%{{opacity:0.4;}} 100%{{opacity:1;}} }}

        .card-body {{ padding: 15px; flex-grow: 1; background: linear-gradient(transparent, rgba(0,0,0,0.9)); margin-top: -100px; position: relative; z-index: 2; }}
        .card-title {{ font-size: 16px; font-weight: 700; color: #fff; line-height: 1.4; text-shadow: 2px 2px 4px #000; }}
        
        .card-footer {{ background: #111; padding: 10px; text-align: center; border-top: 1px solid #222; }}
        .read-more {{ font-size: 12px; color: var(--sp-green); text-decoration: none; font-weight: bold; }}

        .ad-btn {{ background: var(--sp-green); color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; }}
        .card-link {{ text-decoration: none; color: inherit; }}

        .ticker {{ position: fixed; bottom: 0; width: 100%; background: var(--sp-blue); color: white; height: 50px; display: flex; align-items: center; border-top: 3px solid var(--sp-green); z-index: 2000; }}
        .ticker-label {{ background: var(--sp-green); padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: 900; }}
        .ticker-text {{ white-space: nowrap; animation: scroll 40s linear infinite; padding-right: 100%; font-size: 14px; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} .img-box, .video-container {{ height: 450px; }} }}
    </style>
</head>
<body>
    <header>
        <div class="logo">النضال <span>TV</span> ⚽</div>
        <div style="font-size: 11px;">تحديث: {now}</div>
    </header>

    <div class="grid">{news_html}</div>

    <div class="ticker">
        <div class="ticker-label">عاجل</div>
        <div class="ticker-text">{breaking_titles}</div>
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()

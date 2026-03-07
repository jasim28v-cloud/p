import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_news():
    # المصدر الرياضي
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك الربحي الذكي
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        breaking_titles = " • ".join([item.title.text for item in items[:10]])
        news_html = ""

        for i, item in enumerate(items[:20]):
            title = item.title.text
            news_url = item.link.text
            media = item.find('enclosure')
            url = media.get('url') if media else ""
            m_type = media.get('type') if media else ""
            
            # فحص ذكي: هل هو فيديو حقيقي؟
            is_video = "video" in m_type or url.endswith(('.mp4', '.m4v'))
            
            if is_video:
                display_media = f'''
                <div class="media-box">
                    <video autoplay muted loop playsinline class="main-media">
                        <source src="{url}" type="video/mp4">
                    </video>
                    <span class="badge">فيديو حصري 🎥</span>
                </div>'''
            else:
                # إذا لم يتوفر فيديو، نضع الصورة بشكل فخم جداً (Zoom effect) لمنع الشاشة السوداء
                img_src = url if url else "https://cdn.pixabay.com/photo/2016/05/20/21/57/football-1406106_1280.jpg"
                display_media = f'''
                <div class="media-box">
                    <img src="{img_src}" class="main-media zoom-img">
                    <span class="badge">أخبار الملاعب ⚽</span>
                </div>'''

            news_html += f'''
            <div class="reel-card">
                <a href="{my_direct_link}" target="_blank" class="main-link">
                    {display_media}
                    <div class="overlay"></div>
                    <div class="content">
                        <h2 class="title">{title}</h2>
                        <div class="btn">إضغط للمشاهدة كاملة ⚡</div>
                    </div>
                </a>
            </div>'''
            
            # إضافة إعلان جذاب كل 3 أخبار لضمان الربح
            if (i + 1) % 3 == 0:
                news_html += f'''
                <div class="reel-card ad-card">
                    <a href="{my_direct_link}" target="_blank" class="main-link">
                        <div class="ad-bg">
                            <div class="ad-wrap">
                                <div class="icon">🎁</div>
                                <h2 class="title">مبروك! فزت بفرصة للمشاركة في سحب اليوم</h2>
                                <div class="btn ad-btn">إستلم جائزتك الآن</div>
                            </div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال سبورت LIVE</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #000; color: #fff; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 60px; }}
        header {{ background: #111; padding: 15px; border-bottom: 3px solid #e74c3c; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
        .logo {{ font-size: 22px; font-weight: 900; color: #e74c3c; }}
        .grid {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 10px; padding: 10px; }}
        .reel-card {{ background: #1a1a1a; border-radius: 15px; height: 500px; overflow: hidden; position: relative; border: 1px solid #333; }}
        .media-box {{ width: 100%; height: 100%; position: relative; }}
        .main-media {{ width: 100%; height: 100%; object-fit: cover; }}
        .zoom-img {{ animation: zoom 20s infinite alternate; }}
        @keyframes zoom {{ from {{ transform: scale(1); }} to {{ transform: scale(1.2); }} }}
        .overlay {{ position: absolute; bottom: 0; width: 100%; height: 60%; background: linear-gradient(transparent, rgba(0,0,0,0.9)); }}
        .content {{ position: absolute; bottom: 20px; right: 15px; left: 15px; z-index: 2; }}
        .title {{ font-size: 16px; font-weight: 700; margin-bottom: 15px; text-shadow: 2px 2px 4px #000; }}
        .btn {{ background: #e74c3c; color: #fff; text-align: center; padding: 10px; border-radius: 30px; font-weight: bold; font-size: 13px; }}
        .badge {{ position: absolute; top: 15px; right: 15px; background: rgba(231, 76, 60, 0.8); padding: 5px 12px; border-radius: 5px; font-size: 11px; font-weight: bold; }}
        .ad-bg {{ height: 100%; background: linear-gradient(45deg, #1e272e, #000); display: flex; align-items: center; justify-content: center; text-align: center; }}
        .ad-btn {{ background: #f1c40f; color: #000; }}
        .main-link {{ text-decoration: none; color: inherit; }}
        .ticker {{ position: fixed; bottom: 0; width: 100%; background: #e74c3c; color: #fff; height: 40px; display: flex; align-items: center; z-index: 1000; }}
        .ticker-text {{ white-space: nowrap; animation: scroll 40s linear infinite; padding-right: 100%; font-size: 14px; font-weight: bold; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} .reel-card {{ height: 85vh; border-radius: 0; }} }}
    </style>
</head>
<body>
    <header><div class="logo">النضال سبورت LIVE</div><div style="font-size:11px;">{now}</div></header>
    <div class="grid">{news_html}</div>
    <div class="ticker"><div class="ticker-text">{breaking_titles}</div></div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()

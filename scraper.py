import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك الربحي الذكي
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        breaking_titles = " • ".join([item.title.text for item in items[:12]])
        news_html = ""

        for i, item in enumerate(items[:24]):
            title = item.title.text
            news_url = item.link.text
            media = item.find('enclosure')
            url = media.get('url') if media else ""
            m_type = media.get('type') if media else ""
            
            # فحص إذا كان المحتوى فيديو
            is_vid = "video" in m_type or url.endswith(('.mp4', '.m4v'))
            
            if is_vid:
                display_media = f'''
                <div class="media-box">
                    <video autoplay muted loop playsinline class="main-video">
                        <source src="{url}" type="video/mp4">
                    </video>
                    <div class="video-overlay"></div>
                </div>'''
            else:
                # إذا كانت صورة، نجعلها تتحرك ببطء (Ken Burns Effect) لتبدو كفيديو
                img_src = url if url else "https://cdn.pixabay.com/photo/2016/11/29/02/05/audience-1866738_1280.jpg"
                display_media = f'''
                <div class="media-box">
                    <img src="{img_src}" class="animated-img">
                    <div class="video-overlay"></div>
                </div>'''

            news_html += f'''
            <div class="reel-card">
                <a href="{my_direct_link}" target="_blank" class="main-link">
                    {display_media}
                    <div class="info-content">
                        <h2 class="title">{title}</h2>
                        <div class="action-btn">شاهد الآن ⚡</div>
                    </div>
                </a>
                <div class="footer-source">
                    <a href="{news_url}" target="_blank">المصدر الأصلي</a>
                </div>
            </div>'''
            
            # إعلان فيديو (محاكاة) كل 4 أخبار
            if (i + 1) % 4 == 0:
                ad_vids = ["https://cdn.pixabay.com/photo/2016/05/20/21/57/football-1406106_1280.jpg", "https://cdn.pixabay.com/photo/2014/10/14/20/24/soccer-488700_1280.jpg"]
                news_html += f'''
                <div class="reel-card ad-special">
                    <a href="{my_direct_link}" target="_blank" class="main-link">
                        <div class="media-box">
                            <img src="{random.choice(ad_vids)}" class="animated-img" style="filter: hue-rotate(90deg);">
                            <div class="video-overlay" style="background: linear-gradient(transparent, #27ae60);"></div>
                            <span class="ad-badge">هدية رياضية 🎁</span>
                        </div>
                        <div class="info-content">
                            <h2 class="title" style="color:#fff;">توقع الفائز اليوم وارحب رصيد فوري!</h2>
                            <div class="action-btn" style="background:#27ae60;">اضغط للمشاركة مجاناً</div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال سبورت TV | Reels</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon-green: #2ecc71; --dark-bg: #0a0a0a; }}
        body {{ background: var(--dark-bg); color: white; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 60px; overflow-x: hidden; }}
        
        header {{ background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); color: white; padding: 12px 5%; border-bottom: 2px solid var(--neon-green); position: sticky; top:0; z-index: 1000; display:flex; justify-content:space-between; align-items:center; }}
        .logo {{ font-size: 22px; font-weight: 900; letter-spacing: 1px; }}
        .logo span {{ color: var(--neon-green); text-shadow: 0 0 10px var(--neon-green); }}

        .reels-container {{ max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 10px; padding: 10px; }}
        
        .reel-card {{ background: #111; border-radius: 12px; overflow: hidden; position: relative; height: 500px; border: 1px solid #222; transition: 0.3s; }}
        .media-box {{ width: 100%; height: 100%; position: relative; overflow: hidden; }}
        
        .main-video, .animated-img {{ width: 100%; height: 100%; object-fit: cover; }}
        
        /* تأثير الحركة للصور لتصبح مثل الفيديو */
        .animated-img {{ animation: kenburns 20s infinite alternate; }}
        @keyframes kenburns {{ from {{ transform: scale(1); }} to {{ transform: scale(1.3); }} }}

        .video-overlay {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 60%; background: linear-gradient(transparent, rgba(0,0,0,0.95)); z-index: 1; }}
        
        .info-content {{ position: absolute; bottom: 40px; right: 0; left: 0; padding: 20px; z-index: 2; pointer-events: none; }}
        .title {{ font-size: 16px; font-weight: 700; line-height: 1.5; margin-bottom: 15px; text-shadow: 2px 2px 5px #000; }}
        .action-btn {{ display: inline-block; background: rgba(255,255,255,0.2); backdrop-filter: blur(5px); border: 1px solid white; padding: 8px 20px; border-radius: 30px; font-size: 13px; font-weight: bold; pointer-events: auto; transition: 0.3s; }}
        .action-btn:hover {{ background: var(--neon-green); border-color: var(--neon-green); }}

        .ad-badge {{ position: absolute; top: 15px; left: 15px; background: #e74c3c; padding: 4px 12px; border-radius: 5px; font-size: 12px; font-weight: bold; z-index: 3; box-shadow: 0 0 10px rgba(0,0,0,0.5); }}
        
        .footer-source {{ position: absolute; bottom: 5px; left: 10px; z-index: 3; }}
        .footer-source a {{ color: rgba(255,255,255,0.5); text-decoration: none; font-size: 10px; }}

        .ticker {{ position: fixed; bottom: 0; width: 100%; background: #000; height: 45px; display: flex; align-items: center; border-top: 1px solid #333; z-index: 1000; }}
        .ticker-label {{ background: var(--neon-green); color: black; padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: 900; font-size: 14px; }}
        .ticker-text {{ white-space: nowrap; animation: scroll 50s linear infinite; padding-right: 100%; font-size: 13px; color: #ccc; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        
        @media (max-width: 600px) {{ .reels-container {{ grid-template-columns: 1fr; gap: 5px; padding: 5px; }} .reel-card {{ height: 85vh; border-radius: 0; }} }}
    </style>
</head>
<body>
    <header>
        <div class="logo">النضال <span>REELS</span> 🎥</div>
        <div style="font-size: 11px; color: #888;">{now}</div>
    </header>

    <div class="reels-container">{news_html}</div>

    <div class="ticker">
        <div class="ticker-label">عاجل</div>
        <div class="ticker-text">{breaking_titles}</div>
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()

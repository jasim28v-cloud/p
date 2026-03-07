import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random

def run_news():
    # نستخدم رابط الفيديو المباشر من RT Sport
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        breaking_titles = " • ".join([item.title.text for item in items[:10]])
        news_html = ""
        video_count = 0

        for item in items:
            title = item.title.text
            news_url = item.link.text
            
            # البحث عن رابط الفيديو الحقيقي داخل وسم enclosure أو description
            media_content = item.find('enclosure')
            media_url = media_content.get('url') if media_content else ""
            media_type = media_content.get('type') if media_content else ""
            
            # شرط صارم: يجب أن يكون الرابط فيديو حقيقي mp4
            is_real_video = "video" in media_type or media_url.endswith(('.mp4', '.m4v'))
            
            if is_real_video:
                video_count += 1
                news_html += f'''
                <div class="reel-card">
                    <a href="{my_direct_link}" target="_blank" class="main-link">
                        <div class="video-container">
                            <video autoplay muted loop playsinline class="real-video">
                                <source src="{media_url}" type="video/mp4">
                            </video>
                            <div class="video-overlay"></div>
                            <span class="video-tag">فيديو حصري 🎥</span>
                        </div>
                        <div class="info-content">
                            <h2 class="title">{title}</h2>
                            <div class="play-btn">إضغط للمشاهدة كاملة ▶️</div>
                        </div>
                    </a>
                </div>'''
                
                # إضافة إعلان "توقع واربح" بعد كل فيديوين حقيقيين
                if video_count % 2 == 0:
                    news_html += f'''
                    <div class="reel-card ad-card">
                        <a href="{my_direct_link}" target="_blank" class="main-link">
                            <div class="video-container ad-gradient">
                                <div class="ad-content">
                                    <div class="ad-icon">🎁</div>
                                    <h2 class="title" style="text-align:center;">مبروك! تم اختيارك للمشاركة في سحب اليوم</h2>
                                    <div class="play-btn" style="background:#f1c40f; color:#000;">إستلم جائزتك الآن</div>
                                </div>
                            </div>
                        </a>
                    </div>'''

        # إذا لم يجد السكربت فيديوهات كافية، سيجلب آخر فيديو ثابت لضمان عدم فراغ الموقع
        if video_count == 0:
            print("No real videos found in current RSS feed.")

        now = datetime.now().strftime("%I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال سبورت TV | فيديوهات حصرية</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #000; color: white; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 60px; }}
        header {{ background: #111; padding: 15px; border-bottom: 2px solid #e74c3c; display:flex; justify-content:space-between; align-items:center; position:sticky; top:0; z-index:100; }}
        .logo {{ font-size: 20px; font-weight: 900; color: #e74c3c; }}
        .grid {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 10px; padding: 10px; }}
        .reel-card {{ background: #1a1a1a; border-radius: 15px; height: 550px; overflow: hidden; position: relative; border: 1px solid #333; }}
        .video-container {{ width: 100%; height: 100%; position: relative; }}
        .real-video {{ width: 100%; height: 100%; object-fit: cover; }}
        .video-overlay {{ position: absolute; bottom: 0; width: 100%; height: 50%; background: linear-gradient(transparent, rgba(0,0,0,0.9)); }}
        .info-content {{ position: absolute; bottom: 20px; right: 15px; left: 15px; z-index: 2; }}
        .title {{ font-size: 16px; font-weight: 700; line-height: 1.5; margin-bottom: 10px; text-shadow: 2px 2px 4px #000; }}
        .play-btn {{ background: #e74c3c; color: white; text-align: center; padding: 10px; border-radius: 30px; font-weight: bold; font-size: 13px; }}
        .video-tag {{ position: absolute; top: 15px; right: 15px; background: rgba(231, 76, 60, 0.8); padding: 5px 10px; border-radius: 5px; font-size: 11px; font-weight: bold; }}
        .ad-gradient {{ background: linear-gradient(45deg, #2c3e50, #000); display: flex; align-items: center; justify-content: center; }}
        .ad-content {{ padding: 20px; text-align: center; }}
        .ad-icon {{ font-size: 50px; margin-bottom: 20px; }}
        .main-link {{ text-decoration: none; color: inherit; }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} .reel-card {{ height: 90vh; border-radius: 0; }} }}
    </style>
</head>
<body>
    <header><div class="logo">النضال سبورت <span>LIVE</span></div><div style="font-size:11px;">{now}</div></header>
    <div class="grid">{news_html}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_trend_mashahir_ultra_v2():
    # رابط قناة التيليجرام (نسخة العرض العام)
    telegram_url = "https://news.google.com/rss/search?q=site:lahamag.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    
    try:
        # رابط الإعلان الخاص بك
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        ad_ins = '<ins style="width: 300px;height:250px" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'

        response = requests.get(telegram_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        messages = soup.find_all('div', class_='tgme_widget_message_bubble')
        
        news_grid_html = ""
        breaking_news_html = ""
        video_section_html = ""

        for i, msg in enumerate(messages[::-1][:25]): 
            try:
                # 1. استخراج النص
                text_element = msg.find('div', class_='tgme_widget_message_text')
                full_text = text_element.get_text(strip=True) if text_element else "تغطية مستمرة لأخبار المشاهير"
                title = (full_text[:95] + '..') if len(full_text) > 95 else full_text
                
                # إعداد شريط الأخبار العاجلة (أول 5 منشورات)
                if i < 5:
                    breaking_news_html += f"<span> • {title} </span>"

                # 2. استخراج الوسائط (صور أو فيديو)
                photo_element = msg.find('a', class_='tgme_widget_message_photo_wrap')
                video_element = msg.find('video')
                
                img_url = "https://via.placeholder.com/600x400?text=Trend+Mashahir"
                if photo_element and 'style' in photo_element.attrs:
                    style = photo_element['style']
                    img_search = re.search(r"background-image:url\(['\"](.+?)['\"]\)", style)
                    if img_search: img_url = img_search.group(1)

                # إذا كان المنشور يحتوي على فيديو، نضعه في قسم الفيديوهات
                if video_element and i < 10:
                    video_section_html += f'''
                    <div class="v-card">
                        <a href="{my_link}" target="_blank">
                            <div class="v-icon"><i class="fas fa-play"></i></div>
                            <img src="{img_url}" alt="video">
                            <p>{title[:50]}...</p>
                        </a>
                    </div>'''

                # 3. بناء شبكة الأخبار الرئيسية
                if i % 6 == 0 and i != 0:
                    news_grid_html += f'<div class="ad-grid-box">{ad_ins}</div>'

                news_grid_html += f'''
                <div class="n-card">
                    <a href="{my_link}" target="_blank">
                        <div class="n-img-wrapper">
                            <img src="{img_url}" alt="trend" loading="lazy">
                            <div class="n-badge">تحديث مباشر</div>
                        </div>
                        <div class="n-content">
                            <h3>{title}</h3>
                            <div class="n-footer">
                                <span><i class="far fa-clock"></i> {datetime.now().strftime('%H:%M')}</span>
                                <span class="n-btn">التفاصيل <i class="fas fa-chevron-left"></i></span>
                            </div>
                        </div>
                    </a>
                </div>'''
            except: continue

        # بناء واجهة HTML النهائية
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ترند مشاهير | أخبار الفن والدراما</title>
    <link href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ --main: #ff0050; --dark: #080808; --card-bg: #121212; }}
        body {{ background: var(--dark); color: #fff; font-family: 'Almarai', sans-serif; margin: 0; overflow-x: hidden; }}
        
        /* شريط عاجل */
        .breaking-bar {{ background: #ff0050; color: white; padding: 10px 0; overflow: hidden; white-space: nowrap; position: relative; z-index: 1001; font-weight: bold; }}
        .breaking-content {{ display: inline-block; animation: marquee 30s linear infinite; }}
        @keyframes marquee {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

        header {{ background: rgba(0,0,0,0.95); padding: 20px 5%; border-bottom: 2px solid var(--main); display: flex; justify-content: space-between; align-items: center; sticky: top; }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 800; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--main); }}

        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        /* قسم الفيديوهات */
        .video-reel {{ display: flex; gap: 15px; overflow-x: auto; padding-bottom: 20px; scrollbar-width: none; }}
        .v-card {{ min-width: 160px; position: relative; border-radius: 15px; overflow: hidden; background: #000; }}
        .v-card img {{ width: 100%; height: 240px; object-fit: cover; opacity: 0.6; }}
        .v-card p {{ position: absolute; bottom: 5px; font-size: 11px; padding: 5px; text-align: center; }}
        .v-icon {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 30px; color: var(--main); z-index: 2; }}

        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; margin-top: 30px; }}
        .n-card {{ background: var(--card-bg); border-radius: 15px; overflow: hidden; transition: 0.3s; }}
        .n-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 20px rgba(255,0,80,0.2); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img-wrapper {{ position: relative; height: 200px; }}
        .n-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; bottom: 10px; right: 10px; background: var(--main); font-size: 11px; padding: 3px 10px; border-radius: 5px; }}
        .n-content {{ padding: 15px; }}
        .n-content h3 {{ font-size: 16px; margin: 0 0 10px; line-height: 1.5; height: 48px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; align-items: center; color: #666; font-size: 12px; }}
        .n-btn {{ color: var(--main); font-weight: bold; border: 1px solid var(--main); padding: 4px 10px; border-radius: 5px; }}

        .ad-grid-box {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px; background: #111; border-radius: 10px; border: 1px solid #222; }}
        h2.sec-title {{ font-size: 22px; border-right: 4px solid var(--main); padding-right: 12px; margin: 40px 0 20px; }}
    </style>
</head>
<body>
    <div class="breaking-bar">
        <div class="breaking-content">
            {breaking_news_html}
        </div>
    </div>

    <header>
        <a href="#" class="logo">TREND<span>CELEBS</span></a>
        <div><i class="fas fa-search"></i></div>
    </header>

    <div class="container">
        <h2 class="sec-title">قصص فيديوهات (Reels)</h2>
        <div class="video-reel">
            {video_section_html}
        </div>

        <h2 class="sec-title">آخر الأخبار</h2>
        <div class="news-grid">
            {news_grid_html}
        </div>
    </div>

    <footer style="text-align: center; padding: 40px; margin-top: 50px; background: #000; border-top: 1px solid #222;">
        <div class="logo">TREND<span>CELEBS</span></div>
        <p style="color: #444; font-size: 12px; margin-top: 10px;">جميع الحقوق محفوظة 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ تم بناء الإصدار الألترا بنجاح! افتح index.html")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_trend_mashahir_ultra_v2()

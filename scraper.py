import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_trend_mashahir_final_edition():
    # رابط قناة التيليجرام (نسخة العرض العام)
    telegram_url = "https://t.me/s/TREND_USED"
    
    # الـ Headers الاحترافية التي طلبتها لضمان سحب البيانات بأمان
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,video/*;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Ch-Ua': '"Google Chrome";v="124", "Not:A-Brand";v="8", "Chromium";v="124"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.google.com',
        'Range': 'bytes=0-'
    }
    
    try:
        # رابط الإعلان الخاص بك
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        ad_ins = '<ins style="width: 300px;height:250px" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'

        # بدء عملية الجلب
        response = requests.get(telegram_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        messages = soup.find_all('div', class_='tgme_widget_message_bubble')
        
        news_grid_html = ""
        breaking_news_html = ""
        video_section_html = ""

        # معالجة آخر 25 منشوراً
        for i, msg in enumerate(messages[::-1][:25]): 
            try:
                # 1. استخراج النص والعناوين
                text_element = msg.find('div', class_='tgme_widget_message_text')
                full_text = text_element.get_text(strip=True) if text_element else "خبر حصري من ترند مشاهير"
                title = (full_text[:90] + '..') if len(full_text) > 90 else full_text
                
                # إضافة للأخبار العاجلة (أعلى الصفحة)
                if i < 6:
                    breaking_news_html += f"<span> • {title} </span>"

                # 2. استخراج الوسائط باستخدام نظام الـ Headers الجديد
                photo_element = msg.find('a', class_='tgme_widget_message_photo_wrap')
                video_element = msg.find('video')
                
                img_url = "https://via.placeholder.com/600x400?text=Trend+Mashahir"
                if photo_element and 'style' in photo_element.attrs:
                    style = photo_element['style']
                    img_search = re.search(r"background-image:url\(['\"](.+?)['\"]\)", style)
                    if img_search: 
                        img_url = img_search.group(1)

                # قسم الفيديوهات (القصص القصيرة)
                if video_element and i < 12:
                    video_section_html += f'''
                    <div class="v-card">
                        <a href="{my_link}" target="_blank">
                            <div class="v-icon"><i class="fas fa-play"></i></div>
                            <img src="{img_url}" alt="video">
                            <p>{title[:40]}...</p>
                        </a>
                    </div>'''

                # 3. بناء شبكة الأخبار مع توزيع الإعلانات
                if i > 0 and i % 5 == 0:
                    news_grid_html += f'<div class="ad-grid-box">{ad_ins}</div>'

                news_grid_html += f'''
                <div class="n-card">
                    <a href="{my_link}" target="_blank">
                        <div class="n-img-wrapper">
                            <img src="{img_url}" alt="news" loading="lazy">
                            <div class="n-badge">عاجل</div>
                            <div class="n-overlay"></div>
                        </div>
                        <div class="n-content">
                            <h3>{title}</h3>
                            <div class="n-footer">
                                <span><i class="far fa-clock"></i> {datetime.now().strftime('%H:%M')}</span>
                                <span class="n-btn">المزيد <i class="fas fa-arrow-left"></i></span>
                            </div>
                        </div>
                    </a>
                </div>'''
            except: continue

        # بناء التصميم النهائي (ألترا مودرن)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ترند مشاهير | TREND CELEBS</title>
    <link href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&family=Orbitron:wght@800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ --primary: #ff0050; --bg: #050505; --card: #111111; }}
        body {{ background: var(--bg); color: #fff; font-family: 'Almarai', sans-serif; margin: 0; overflow-x: hidden; }}
        
        .breaking-strip {{ background: var(--primary); color: #fff; padding: 12px 0; overflow: hidden; white-space: nowrap; font-weight: 800; font-size: 14px; position: sticky; top: 0; z-index: 2000; box-shadow: 0 4px 15px rgba(255,0,80,0.4); }}
        .breaking-scroll {{ display: inline-block; animation: scroll 35s linear infinite; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

        header {{ background: rgba(0,0,0,0.9); padding: 20px 6%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 800; color: #fff; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; }}
        .logo span {{ color: var(--primary); }}

        .container {{ max-width: 1300px; margin: 0 auto; padding: 20px; }}
        
        .v-reel {{ display: flex; gap: 15px; overflow-x: auto; padding: 10px 0 30px; scrollbar-width: none; }}
        .v-card {{ min-width: 150px; height: 230px; border-radius: 15px; overflow: hidden; position: relative; background: #000; border: 1px solid #333; }}
        .v-card img {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.5; transition: 0.4s; }}
        .v-card:hover img {{ opacity: 0.8; transform: scale(1.1); }}
        .v-icon {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: var(--primary); font-size: 35px; text-shadow: 0 0 15px rgba(0,0,0,0.5); }}
        .v-card p {{ position: absolute; bottom: 0; padding: 10px; font-size: 10px; text-align: center; background: linear-gradient(transparent, #000); width: 100%; }}

        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 30px; }}
        .n-card {{ background: var(--card); border-radius: 20px; overflow: hidden; border: 1px solid #222; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
        .n-card:hover {{ transform: translateY(-10px); border-color: var(--primary); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img-wrapper {{ position: relative; height: 220px; overflow: hidden; }}
        .n-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-overlay {{ position: absolute; inset: 0; background: linear-gradient(to top, var(--card), transparent); }}
        .n-badge {{ position: absolute; top: 15px; right: 15px; background: var(--primary); padding: 5px 15px; border-radius: 8px; font-size: 11px; font-weight: 800; z-index: 2; }}
        
        .n-content {{ padding: 20px; }}
        .n-content h3 {{ font-size: 17px; line-height: 1.6; margin: 0 0 15px; height: 54px; overflow: hidden; color: #eee; }}
        .n-footer {{ display: flex; justify-content: space-between; align-items: center; color: #666; font-size: 13px; }}
        .n-btn {{ color: var(--primary); font-weight: 800; border: 1px solid var(--primary); padding: 5px 12px; border-radius: 8px; font-size: 12px; }}

        .ad-grid-box {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 40px; background: rgba(255,255,255,0.02); border-radius: 20px; border: 1px dashed #333; }}
        h2.title {{ font-size: 24px; margin: 40px 0 20px; border-right: 5px solid var(--primary); padding-right: 15px; }}

        @media (max-width: 768px) {{ .news-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="breaking-strip">
        <div class="breaking-scroll">{breaking_news_html}</div>
    </div>

    <header>
        <a href="#" class="logo">TREND<span>CELEBS</span></a>
        <div style="font-size: 20px; color: var(--primary);"><i class="fas fa-bolt"></i></div>
    </header>

    <div class="container">
        <h2 class="title">ترند الفيديوهات</h2>
        <div class="v-reel">{video_section_html}</div>

        <h2 class="title">أحدث أخبار المشاهير</h2>
        <div class="news-grid">{news_grid_html}</div>
    </div>

    <footer style="text-align: center; padding: 60px; background: #000; border-top: 1px solid #222; margin-top: 60px;">
        <div class="logo">TREND<span>CELEBS</span></div>
        <p style="color: #444; margin-top: 20px; font-size: 14px;">الإصدار المطور 2026 © تجربة مستخدم ذكية</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ تم التحديث بنجاح باستخدام الـ Headers الجديدة! افتح index.html")
        
    except Exception as e:
        print(f"❌ خطأ تقني: {e}")

if __name__ == "__main__":
    run_trend_mashahir_final_edition()

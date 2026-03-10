import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_trend_mashahir_scraper():
    # القناة المستهدفة (نسخة الويب للمعاينة)
    telegram_url = "https://t.me/s/muraselonDrama"
    matches_url = "https://www.yallakora.com/match-center"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        # رابط الإعلان الخاص بك من المعلومات المحفوظة
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # أكواد الإعلانات
        ad_ins = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'

        # 1. جلب مباريات اليوم (YallaKora)
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        for m in match_soup.select('.allMatchesList .matchCard')[:8]:
            try:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                score_spans = m.find('div', class_='MResult').find_all('span')
                score = f"{score_spans[0].text}-{score_spans[1].text}" if len(score_spans) > 1 else "قادم"
                matches_html += f'''
                <div class="m-card">
                    <div class="m-teams-row">
                        <span class="m-team">{t1}</span>
                        <span class="m-score">{score}</span>
                        <span class="m-team">{t2}</span>
                    </div>
                </div>'''
            except: continue

        # 2. جلب أخبار المشاهير (Telegram Scraping)
        response = requests.get(telegram_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        messages = soup.find_all('div', class_='tgme_widget_message_bubble')
        
        news_grid_html = ""
        for i, msg in enumerate(messages[::-1][:18]):  # جلب آخر 18 منشور
            try:
                # استخراج النص
                text_element = msg.find('div', class_='tgme_widget_message_text')
                title = text_element.get_text(strip=True)[:100] + "..." if text_element else "خبر جديد من ترند مشاهير"
                
                # استخراج الصورة من الـ Style (Background-image)
                photo_element = msg.find('a', class_='tgme_widget_message_photo_wrap')
                img_url = "https://via.placeholder.com/600x400?text=Trend+Mashahir"
                if photo_element and 'style' in photo_element.attrs:
                    style = photo_element['style']
                    img_search = re.search(r"background-image:url\(['\"](.+?)['\"]\)", style)
                    if img_search:
                        img_url = img_search.group(1)

                if i % 6 == 0 and i != 0:
                    news_grid_html += f'<div class="ad-grid-box">{ad_ins}</div>'

                news_grid_html += f'''
                <div class="n-card">
                    <a href="{my_link}" target="_blank">
                        <div class="n-img-wrapper">
                            <img src="{img_url}" alt="news" loading="lazy">
                            <div class="n-overlay"></div>
                            <div class="n-badge">حصري</div>
                        </div>
                        <div class="n-content">
                            <h3>{title}</h3>
                            <div class="n-footer">
                                <span><i class="far fa-clock"></i> {datetime.now().strftime('%H:%M')}</span>
                                <span class="n-btn">تفاصيل <i class="fas fa-external-link-alt"></i></span>
                            </div>
                        </div>
                    </a>
                </div>'''
            except: continue

        # 3. الواجهة النهائية (ترند مشاهير - النسخة الاحترافية)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ترند مشاهير | TREND CELEBS</title>
    <link href="https://fonts.googleapis.com/css2?family=Almarai:wght@300;700;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ --main: #ff0050; --gold: #ffd700; --dark: #0a0a0a; --glass: rgba(255, 255, 255, 0.05); }}
        body {{ background: var(--dark); color: #fff; font-family: 'Almarai', sans-serif; margin: 0; overflow-x: hidden; }}
        header {{ background: rgba(0,0,0,0.9); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--main); position: sticky; top: 0; z-index: 1000; backdrop-filter: blur(10px); }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 24px; font-weight: 800; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--main); }}
        .container {{ max-width: 1300px; margin: 0 auto; padding: 20px; }}
        
        .match-ticker {{ display: flex; gap: 15px; overflow-x: auto; padding: 20px 0; scrollbar-width: none; }}
        .m-card {{ background: var(--glass); min-width: 220px; padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }}
        .m-score {{ color: var(--gold); font-weight: bold; font-size: 18px; margin: 0 10px; }}
        
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .n-card {{ background: #151515; border-radius: 15px; overflow: hidden; border-bottom: 4px solid transparent; transition: 0.3s; height: 100%; }}
        .n-card:hover {{ transform: translateY(-10px); border-color: var(--main); box-shadow: 0 10px 30px rgba(255,0,80,0.3); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img-wrapper {{ position: relative; height: 220px; }}
        .n-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; top: 10px; right: 10px; background: var(--main); padding: 4px 12px; border-radius: 5px; font-size: 12px; }}
        .n-content {{ padding: 20px; }}
        .n-content h3 {{ font-size: 17px; line-height: 1.6; margin: 0 0 15px; height: 54px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #888; }}
        .n-btn {{ color: var(--main); font-weight: bold; border: 1px solid var(--main); padding: 4px 10px; border-radius: 5px; }}
        
        .ad-grid-box {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px; background: var(--glass); border-radius: 15px; }}
        h2.section-title {{ font-size: 24px; margin: 40px 0; border-right: 4px solid var(--main); padding-right: 15px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">TREND<span>CELEBS</span></a>
        <div style="color: var(--gold);"><i class="fas fa-fire"></i> ترند مشاهير</div>
    </header>

    <div class="container">
        <div class="match-ticker">{matches_html}</div>
        
        <h2 class="section-title">أحدث أخبار الدراما والمشاهير</h2>
        <div class="news-grid">{news_grid_html}</div>
    </div>

    <footer style="text-align: center; padding: 50px; margin-top: 50px; background: #000;">
        <div class="logo">TREND<span>CELEBS</span></div>
        <p style="color: #666; margin-top: 15px;">جميع الحقوق محفوظة © 2026 - منصة ترند مشاهير</p>
    </footer>
</body>
</html>'''

        with open("trend_mashahir.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ تم التحديث! اسم الملف الجديد: trend_mashahir.html")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_trend_mashahir_scraper()

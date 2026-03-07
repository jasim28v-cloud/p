import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك الربحي من Adsterra
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # استخراج العناوين لشريط الأخبار المتحرك
        ticker_text = " • ".join([item.title.text for item in items[:15]])

        news_html = ""
        for i, item in enumerate(items[:24]):
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400/111/fff?text=Malaeb+Live"
            
            # تصميم كرت الخبر (شبيه بأسلوب كووورة الاحترافي)
            news_html += f'''
            <div class="news-item">
                <a href="{my_direct_link}" target="_blank" class="main-link">
                    <div class="img-container">
                        <img src="{img_url}" loading="lazy">
                        <div class="overlay-tag">أخبار حصرية</div>
                    </div>
                    <div class="details">
                        <h2 class="title">{title}</h2>
                        <div class="meta-info">
                            <span>📅 اليوم</span>
                            <span>⏱️ الآن</span>
                        </div>
                    </div>
                </a>
                <div class="footer-link">
                    <a href="{news_url}" target="_blank">قراءة الخبر بالكامل ←</a>
                </div>
            </div>'''
            
            # إعلان "جدول مباريات اليوم" (صيد نقرات فخم)
            if (i + 1) % 4 == 0:
                ad_imgs = [
                    "https://images.pexels.com/photos/46798/the-ball-stadion-football-the-pitch-46798.jpeg?auto=compress&cs=tinysrgb&w=600",
                    "https://images.pexels.com/photos/114296/pexels-photo-114296.jpeg?auto=compress&cs=tinysrgb&w=600"
                ]
                news_html += f'''
                <div class="news-item ad-special">
                    <a href="{my_direct_link}" target="_blank" class="main-link">
                        <div class="img-container">
                            <img src="{random.choice(ad_imgs)}" style="filter: brightness(0.5);">
                            <div class="ad-center">
                                <div class="ad-icon">⚽</div>
                                <h3>جدول مباريات اليوم</h3>
                                <p>شاهد القنوات الناقلة والتشكيلة المتوقعة</p>
                                <span class="ad-btn">دخول مباشر</span>
                            </div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ملاعب لايف - Malaeb Live</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #004d40; --secondary: #ffc107; --bg: #f0f2f5; --text: #1a1a1b; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding-top: 100px; }}
        
        /* الهيدر الرئيسي */
        header {{ background: var(--primary); color: white; padding: 10px 5%; position: fixed; top: 0; width: 100%; z-index: 2000; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border-bottom: 4px solid var(--secondary); display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; }}
        .logo {{ font-size: 26px; font-weight: 900; text-decoration: none; color: white; }}
        .logo span {{ color: var(--secondary); }}
        
        /* شريط عاجل (مثل القنوات الإخبارية) */
        .breaking-bar {{ background: #fff; height: 40px; border-bottom: 1px solid #ddd; position: fixed; top: 60px; width: 100%; z-index: 1500; display: flex; align-items: center; }}
        .breaking-label {{ background: #d32f2f; color: white; padding: 0 20px; height: 100%; display: flex; align-items: center; font-weight: bold; font-size: 14px; z-index: 5; box-shadow: 5px 0 10px rgba(0,0,0,0.1); }}
        .ticker-wrap {{ overflow: hidden; flex-grow: 1; }}
        .ticker-move {{ white-space: nowrap; animation: move 45s linear infinite; font-size: 14px; color: #333; }}
        @keyframes move {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

        /* شبكة الأخبار */
        .main-container {{ max-width: 1200px; margin: 20px auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 15px; padding: 0 15px; }}
        
        .news-item {{ background: #fff; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; transition: 0.3s; display: flex; flex-direction: column; }}
        .news-item:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        
        .img-container {{ position: relative; height: 200px; overflow: hidden; }}
        .img-container img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .news-item:hover .img-container img {{ transform: scale(1.1); }}
        
        .overlay-tag {{ position: absolute; top: 10px; right: 10px; background: rgba(0, 77, 64, 0.9); color: white; padding: 4px 12px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        
        .details {{ padding: 15px; flex-grow: 1; }}
        .title {{ font-size: 17px; font-weight: 700; line-height: 1.6; margin: 0; color: #222; }}
        .meta-info {{ margin-top: 10px; font-size: 11px; color: #777; display: flex; gap: 15px; }}
        
        .footer-link {{ border-top: 1px solid #eee; padding: 10px 15px; background: #fdfdfd; }}
        .footer-link a {{ text-decoration: none; color: var(--primary); font-size: 12px; font-weight: bold; }}

        /* تصميم الإعلان */
        .ad-special {{ border: 2px solid var(--secondary); background: #fffdf2; }}
        .ad-center {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; text-align: center; padding: 20px; }}
        .ad-icon {{ font-size: 40px; margin-bottom: 10px; }}
        .ad-btn {{ background: var(--secondary); color: #000; padding: 8px 25px; border-radius: 20px; font-weight: 900; margin-top: 10px; font-size: 14px; box-shadow: 0 4px 0 #c79a00; }}
        
        .main-link {{ text-decoration: none; color: inherit; }}

        @media (max-width: 600px) {{ 
            body {{ padding-top: 90px; }}
            header {{ padding: 10px 15px; }}
            .breaking-bar {{ top: 52px; }}
            .main-container {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">ملاعب <span>لايف</span> 🏟️</a>
        <div style="font-size: 11px; background: rgba(0,0,0,0.2); padding: 5px 10px; border-radius: 4px;">{now}</div>
    </header>

    <div class="breaking-bar">
        <div class="breaking-label">عاجل</div>
        <div class="ticker-wrap">
            <div class="ticker-move">{ticker_text}</div>
        </div>
    </div>

    <div class="main-container">{news_html}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()

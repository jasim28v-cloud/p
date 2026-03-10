import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_lumina_prime_scraper():
    rss_url = "https://t.me/s/muraselonDrama"
    matches_url = "https://www.yallakora.com/match-center"
    
    # الـ Headers الاحترافية لضمان سحب البيانات بأمان وسرعة
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
        
        # أكواد الإعلانات
        ad_ins = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'
        ad_script = '<script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>'

        # 1. جلب المباريات (بتنسيق ألترا العائم)
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        # جلب أول 8 مباريات لضمان مظهر ضخم
        for league in match_soup.find_all('div', class_='matchCard')[:6]:
            for m in league.find_all('div', class_='allMatchesList')[:1]:
                try:
                    t1 = m.find('div', class_='teamA').text.strip()
                    t2 = m.find('div', class_='teamB').text.strip()
                    res = m.find('div', class_='MResult').find_all('span')
                    score = f"{res[0].text}-{res[1].text}" if len(res) > 1 else "قادم"
                    matches_html += f'''
                    <div class="m-card">
                        <div class="m-status">مباشر</div>
                        <div class="m-teams-row">
                            <span class="m-team">{t1}</span>
                            <span class="m-score">{score}</span>
                            <span class="m-team">{t2}</span>
                        </div>
                    </div>'''
                except: continue

        # 2. جلب الأخبار (بتنسيق ألترا السينمائي)
        response = requests.get(rss_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        news_grid_html = ""
        # جلب أول 15 خبر لضمان مظهر ضخم
        for i, item in enumerate(soup.find_all('item')[:15]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            
            # إدراج الإعلان بذكاء داخل شبكة الأخبار
            if i == 5:
                news_grid_html += f'<div class="ad-grid-box">{ad_ins}</div>'
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img-wrapper">
                        <img src="{img}" alt="news" loading="lazy">
                        <div class="n-overlay"></div>
                        <div class="n-badge">عاجل</div>
                    </div>
                    <div class="n-content">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span><i class="far fa-clock"></i> {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-btn">المزيد <i class="fas fa-chevron-left"></i></span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. بناء الواجهة النهائية (LUMINA PRIME ULTRA - Cinematic Edition)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUMINA PRIME ULTRA | السينمائي</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;600;800&family=Orbitron:wght@500;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ 
            --gold: #ffcf4b; 
            --accent: #00f2ff;
            --dark: #05070a;
            --card-bg: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.08);
        }}
        
        html {{ scroll-behavior: smooth; }}
        * {{ box-sizing: border-box; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        
        body {{ 
            background: var(--dark); color: #e0e0e0; font-family: 'Cairo', sans-serif; margin: 0; 
            background-image: radial-gradient(circle at 50% 50%, #0a111a 0%, #030508 100%);
            min-height: 100vh; overflow-x: hidden;
        }}

        /* Header Ultra */
        header {{ 
            background: rgba(5, 7, 10, 0.8); backdrop-filter: blur(25px); 
            padding: 15px 5%; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; 
        }}
        .logo {{ font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; text-transform: uppercase; letter-spacing: 2px; }}
        .logo span {{ color: var(--gold); text-shadow: 0 0 20px rgba(255,207,75,0.4); }}

        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

        /* شريط المباريات المتطور */
        .match-ticker {{ 
            display: flex; gap: 15px; overflow-x: auto; padding: 10px 0 30px; 
            scrollbar-width: none;
        }}
        .match-ticker::-webkit-scrollbar {{ display: none; }}
        
        .m-card {{ 
            background: var(--card-bg); min-width: 260px; padding: 20px; border-radius: 18px; 
            border: 1px solid var(--border); position: relative; backdrop-filter: blur(10px);
        }}
        .m-card:hover {{ background: rgba(255,255,255,0.07); border-color: var(--accent); }}
        .m-status {{ font-size: 10px; background: #ff4b4b; color: white; padding: 2px 8px; border-radius: 4px; position: absolute; top: 10px; right: 10px; animation: pulse 2s infinite; }}
        .m-teams-row {{ display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }}
        .m-team {{ font-size: 13px; font-weight: 600; flex: 1; text-align: center; color: #aaa; }}
        .m-score {{ color: var(--accent); font-family: 'Orbitron'; font-weight: 700; font-size: 20px; margin: 0 15px; }}

        /* شبكة الأخبار السينمائية الضخمة */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 25px; }}
        .n-card {{ 
            background: var(--card-bg); border-radius: 22px; overflow: hidden; 
            border: 1px solid var(--border); height: 100%; position: relative;
        }}
        .n-card:hover {{ transform: scale(1.03); border-color: var(--gold); box-shadow: 0 20px 40px rgba(0,0,0,0.6); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        
        .n-img-wrapper {{ position: relative; height: 260px; overflow: hidden; }}
        .n-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); }}
        .n-card:hover .n-img-wrapper img {{ transform: scale(1.1); }}
        
        .n-overlay {{ position: absolute; inset: 0; background: linear-gradient(to top, var(--dark) 10%, transparent 60%); }}
        .n-badge {{ position: absolute; top: 15px; left: 15px; background: var(--gold); color: #000; font-size: 11px; font-weight: 800; padding: 4px 15px; border-radius: 6px; }}
        
        .n-content {{ padding: 25px; margin-top: -60px; position: relative; z-index: 2; }}
        .n-content h3 {{ font-size: 18px; margin: 0 0 15px; line-height: 1.6; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        .n-meta {{ display: flex; justify-content: space-between; align-items: center; color: #888; font-size: 12px; }}
        .n-btn {{ color: var(--gold); font-weight: 800; border: 1px solid var(--gold); padding: 5px 15px; border-radius: 10px; font-size: 13px; }}

        /* الإعلانات بتنسيق ألترا */
        .ad-slot-ultra {{ display: flex; justify-content: center; align-items: center; margin: 50px 0; border: 1px dashed var(--border); padding: 20px; border-radius: 20px; }}
        .ad-grid-box {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px; }}

        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
        
        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
            .container {{ padding: 15px; }}
            .logo {{ font-size: 20px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">LUMINA<span>PRIME</span></a>
        <div style="font-size: 11px; border: 1px solid var(--accent); padding: 5px 15px; border-radius: 50px; color: var(--accent); font-weight: 600;">ULTRA CONNECT</div>
    </header>

    <div class="container">
        <div class="match-ticker">
            {matches_html}
        </div>

        <div class="ad-slot-ultra">
            {ad_ins}
        </div>

        <h2 style="font-size: 28px; font-weight: 800; margin: 50px 0 30px; display: flex; align-items: center; gap: 15px; border-right: 5px solid var(--gold); padding-right: 15px;">
            <i class="fas fa-bolt" style="color:var(--gold)"></i> آخر الأخبار
        </h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="ad-slot-ultra" style="border:none;">
            {ad_script}
        </div>
    </div>

    <footer style="text-align: center; padding: 80px 20px; background: rgba(0,0,0,0.4); border-top: 1px solid var(--border); margin-top: 80px;">
        <div class="logo">LUMINA<span>PRIME</span></div>
        <p style="opacity: 0.4; margin-top: 20px; font-size: 14px;">تجربة مستخدم "ألترا" فائقة الفخامة © 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ Done: The Ultra Cinematic Version is ready! Open index.html.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_lumina_prime_scraper()

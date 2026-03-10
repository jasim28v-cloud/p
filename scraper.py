import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import random

def create_lahavision_site():
    # رابط RSS الخاص بجوجل نيوز لملا مغازين
    rss_url = "https://news.google.com/rss/search?q=site:lahamag.com"

    # رؤوس HTTP محسنة
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml,application/xml,text/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        # جلب المحتوى من RSS
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:12]  # أخذ أول 12 خبر

        # إنشاء شريط الأخبار المتحرك
        ticker_items = " • ".join([item.title.text for item in items[:8]])

        # بناء محتوى الأخبار
        news_html = ""
        for i, item in enumerate(items):
            title = item.title.text
            link = item.link.text
            pub_date = item.pubdate.text if hasattr(item, 'pubdate') else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

            # تحديد فئة الخبر
            category = ["حصري", "عاجل", "مهم", "ثقافة", "فن", "مجتمع"][i % 6]

            news_html += f'''
            <article class="news-card">
                <div class="category-badge {category.lower()}">{category}</div>
                <div class="card-content">
                    <h2 class="card-title">{title}</h2>
                    <div class="meta-data">
                        <span>🕒 {datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M")}</span>
                        <span>👁 {random.randint(100, 5000)}</span>
                    </div>
                    <div class="action-area">
                        <a href="{link}" target="_blank" class="btn-read">قراءة الخبر</a>
                    </div>
                </div>
            </article>'''

        # إنشاء الصفحة الكاملة
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LahaVision | آخر أخبار لها مغازين</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #6c5ce7;
            --secondary: #a29bfe;
            --text-main: #333;
            --text-light: #666;
            --bg-light: #f9f9f9;
            --card-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Cairo', sans-serif;
            background-color: var(--bg-light);
            color: var(--text-main);
            line-height: 1.6;
            padding: 20px;
        }}
        header {{
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid #eee;
            margin-bottom: 20px;
        }}
        .logo {{
            font-size: 32px;
            font-weight: 700;
            color: var(--primary);
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        .ticker-wrap {{
            background: var(--primary);
            color: white;
            padding: 10px 0;
            overflow: hidden;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        .ticker-title {{
            background: rgba(0,0,0,0.2);
            padding: 5px 20px;
            display: inline-block;
            margin-right: 10px;
        }}
        .ticker-scroll {{
            display: inline-block;
            white-space: nowrap;
            animation: scroll 60s linear infinite;
            font-size: 14px;
        }}
        @keyframes scroll {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-200%); }}
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .news-card {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: var(--card-shadow);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }}
        .news-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }}
        .category-badge {{
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 600;
            color: white;
            border-radius: 15px;
        }}
        .category-badge.حصري {{ background: #e74c3c; }}
        .category-badge.عاجل {{ background: #e67e22; }}
        .category-badge.مهم {{ background: #3498db; }}
        .category-badge.ثقافة {{ background: #9b59b6; }}
        .category-badge.فن {{ background: #1abc9c; }}
        .category-badge.مجتمع {{ background: #2ecc71; }}
        .card-content {{
            padding: 20px;
        }}
        .card-title {{
            font-size: 18px;
            margin-bottom: 10px;
            line-height: 1.4;
            color: var(--text-main);
        }}
        .meta-data {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: var(--text-light);
            margin-bottom: 15px;
        }}
        .action-area {{
            text-align: center;
        }}
        .btn-read {{
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .btn-read:hover {{
            background: var(--secondary);
            transform: translateY(-2px);
        }}
        footer {{
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            color: var(--text-light);
            font-size: 14px;
            border-top: 1px solid #eee;
        }}
        @media (max-width: 768px) {{
            .container {{ grid-template-columns: 1fr; }}
            body {{ padding: 10px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="logo">LahaVision</div>
        <p style="text-align: center; color: var(--text-light); margin-top: 10px;">آخر أخبار لها مغازين</p>
    </header>

    <div class="ticker-wrap">
        <span class="ticker-title">أهم العناوين</span>
        <div class="ticker-scroll">{ticker_items}</div>
    </div>

    <main class="container">
        {news_html}
    </main>

    <footer>
        <p>© {datetime.now().year} LahaVision | جميع الحقوق محفوظة</p>
    </footer>
</body>
</html>'''

        # حفظ الملف على سطح المكتب
        desktop_path = os.path.expanduser("~/Desktop")
        file_path = os.path.join(desktop_path, "lahavision.html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_html)

        print(f"✅ تم إنشاء موقع LahaVision بنجاح!")
        print(f"يمكنك العثور على الملف في: {file_path}")
        print("افتح الملف باستخدام متصفحك المفضل لمشاهدة الأخبار.")

    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في جلب البيانات: {e}")
        print("قد يكون هناك حظر للطلب من قبل الموقع أو مشكلة في الاتصال بالإنترنت.")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    create_lahavision_site()

#!/usr/bin/env python3
"""
HK Property Slides Generator
Creates HTML slides for presentation
"""
import os

SLIDE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>香港地產市場分析 2026</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
        }}
        .slide {{
            display: none;
            min-height: 100vh;
            padding: 60px;
            box-sizing: border-box;
        }}
        .slide.active {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        h1 {{
            font-size: 48px;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        h2 {{
            font-size: 36px;
            color: #ffd700;
            margin-bottom: 20px;
        }}
        table {{
            background: rgba(255,255,255,0.1);
            border-collapse: collapse;
            width: 80%;
            margin: 20px 0;
        }}
        th, td {{
            padding: 15px;
            text-align: left;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        th {{
            background: rgba(0,0,0,0.3);
        }}
        .emoji {{
            font-size: 24px;
        }}
        .nav {{
            position: fixed;
            bottom: 20px;
            right: 20px;
        }}
        .nav button {{
            background: #ffd700;
            border: none;
            padding: 15px 25px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 5px;
        }}
        .progress {{
            position: fixed;
            bottom: 0;
            left: 0;
            height: 5px;
            background: #ffd700;
        }}
    </style>
</head>
<body>

<div class="slide active" id="slide1">
    <h1>🏠 香港地產市場分析 2026</h1>
    <h2>全面市場透視與投資策略</h2>
    <p style="font-size: 24px; margin-top: 30px;">投資者必備指南</p>
</div>

<div class="slide" id="slide2">
    <h2>📊 市場概覽</h2>
    <table>
        <tr><th>指標</th><th>現狀</th><th>趨勢</th></tr>
        <tr><td>住宅價格</td><td>調整中</td><td>📉 下降</td></tr>
        <tr><td>寫字樓</td><td>供過於求</td><td>📉 下跌</td></tr>
        <tr><td>零售鋪位</td><td>復甦中</td><td>📈 回升</td></tr>
        <tr><td>工業大廈</td><td>穩定</td><td>➡️ 持平</td></tr>
    </table>
</div>

<div class="slide" id="slide3">
    <h2>📈 住宅市場</h2>
    <table>
        <tr><th>地區</th><th>價格 (港幣/平方尺)</th><th>變化</th></tr>
        <tr><td>港島</td><td>$18,000-25,000</td><td>-5%</td></tr>
        <tr><td>九龍</td><td>$15,000-20,000</td><td>-3%</td></tr>
        <tr><td>新界東</td><td>$12,000-16,000</td><td>-2%</td></tr>
        <tr><td>新界西</td><td>$10,000-14,000</td><td>持平</td></tr>
    </table>
    <p>✅ 剛需強勁 | ❌ 投資者觀望</p>
</div>

<div class="slide" id="slide4">
    <h2>💼 寫字樓市場</h2>
    <table>
        <tr><th>地區</th><th>空置率</th><th>預測</th></tr>
        <tr><td>中環</td><td>15-20%</td><td>持續高</td></tr>
        <tr><td>灣仔</td><td>12-18%</td><td>平穩</td></tr>
        <tr><td>港東</td><td>10-15%</td><td>改善</td></tr>
        <tr><td>九龍東</td><td>18-25%</td><td>嚴峻</td></tr>
    </table>
    <p>📉 需求疲弱 | 💰 租金下調壓力</p>
</div>

<div class="slide" id="slide5">
    <h2>🎯 投資機會</h2>
    <table>
        <tr><th>類型</th><th>風險</th><th>回報</th><th>建議</th></tr>
        <tr><td>細價住宅</td><td>中</td><td>5-8%</td><td>✅ 考慮</td></tr>
        <tr><td>車位</td><td>低</td><td>3-5%</td><td>✅ 穩健</td></tr>
        <tr><td>重建項目</td><td>高</td><td>20%+</td><td>💰 專業</td></tr>
    </table>
    <h3>關注區域: 北部都會區、將軍澳、東涌</h3>
</div>

<div class="slide" id="slide6">
    <h2>⚠️ 風險因素</h2>
    <ul style="font-size: 28px; line-height: 2;">
        <li>📈 利率繼續上升</li>
        <li>🇨🇳 中國經濟放緩</li>
        <li>🏠 房屋政策轉變</li>
        <li>🌍 全球經濟衰退</li>
    </ul>
    <h3 style="margin-top: 40px;">建議: 做好水位計算、保持現金流、分散投資</h3>
</div>

<div class="slide" id="slide7">
    <h2>🔮 2026預測</h2>
    <table>
        <tr><th>季度</th><th>住宅</th><th>寫字樓</th><th>零售</th></tr>
        <tr><td>Q1</td><td>-3%</td><td>-5%</td><td>+2%</td></tr>
        <tr><td>Q2</td><td>-2%</td><td>-3%</td><td>+3%</td></tr>
        <tr><td>Q3</td><td>持平</td><td>-2%</td><td>+4%</td></tr>
        <tr><td>Q4</td><td>+2%</td><td>持平</td><td>+5%</td></tr>
    </table>
</div>

<div class="slide" id="slide8">
    <h2>🎯 總結</h2>
    <h3 style="font-size: 36px; color: #ffd700;">市場立場: 審慎樂觀</h3>
    <ul style="font-size: 24px; line-height: 2;">
        <li>🏠 住宅: 等待 Q3-Q4</li>
        <li>💼 寫字樓: 繼續觀望</li>
        <li>🛍️ 零售: 優質鋪位可考慮</li>
        <li>🏭 工業: 平穩，可適度投資</li>
    </ul>
    <p style="margin-top: 40px; font-size: 20px;">關注: 利率走向、中國經濟、房屋供應</p>
</div>

<div class="progress" id="progress"></div>
<div class="nav">
    <button onclick="nextSlide()">下一頁 →</button>
</div>

<script>
let currentSlide = 1;
const totalSlides = 8;

function showSlide(n) {{
    document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
    document.getElementById('slide' + n).classList.add('active');
    document.getElementById('progress').style.width = (n / totalSlides * 100) + '%';
}}

function nextSlide() {{
    currentSlide = currentSlide >= totalSlides ? 1 : currentSlide + 1;
    showSlide(currentSlide);
}}

document.addEventListener('keydown', (e) => {{
    if(e.key === 'ArrowRight' || e.key === ' ') nextSlide();
}});

showSlide(1);
</script>
</body>
</html>
"""

with open("/Users/macbookpro/.openclaw/workspace/company/hk_property_slides.html", "w") as f:
    f.write(SLIDE_TEMPLATE)

print("✅ Created 8-page HTML slides!")
print("File: hk_property_slides.html")
print("\nOpen in browser to present!")

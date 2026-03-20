#!/usr/bin/env python3
"""
Mobile-Friendly HK Property Slides Generator
Responsive design for phone viewing
"""
import os

SLIDE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>香港地產市場分析 2026</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            overflow: hidden;
        }
        
        .slide {
            display: none;
            width: 100vw;
            height: 100vh;
            padding: 20px;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .slide.active { display: block; }
        
        h1 { font-size: 28px; margin-bottom: 20px; text-align: center; }
        h2 { font-size: 22px; color: #ffd700; margin-bottom: 15px; text-align: center; }
        h3 { font-size: 16px; margin: 10px 0; }
        
        table {
            width: 100%;
            font-size: 12px;
            background: rgba(255,255,255,0.1);
            border-collapse: collapse;
            margin: 10px 0;
        }
        
        th, td {
            padding: 8px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
            word-break: break-word;
        }
        
        th { background: rgba(0,0,0,0.3); }
        
        ul { padding-left: 20px; }
        li { margin: 8px 0; font-size: 14px; }
        
        .emoji { font-size: 20px; }
        
        .nav {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 100;
        }
        
        .nav button {
            background: #ffd700;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        
        .progress {
            position: fixed;
            bottom: 0;
            left: 0;
            height: 5px;
            background: #ffd700;
            transition: width 0.3s;
        }
        
        .page-num {
            position: fixed;
            bottom: 25px;
            left: 20px;
            font-size: 14px;
            opacity: 0.7;
        }
        
        .swipe-hint {
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 12px;
            opacity: 0.5;
        }
        
        @media (max-width: 400px) {
            h1 { font-size: 22px; }
            h2 { font-size: 18px; }
            table { font-size: 10px; }
            th, td { padding: 5px; }
        }
    </style>
</head>
<body>

<div class="swipe-hint">👆 Swipe</div>

<div class="slide active" id="slide1">
    <h1>🏠 香港地產市場<br>分析 2026</h1>
    <h2>全面市場透視與投資策略</h2>
    <p style="text-align:center;margin-top:20px;font-size:16px;">投資者必備指南</p>
</div>

<div class="slide" id="slide2">
    <h2>📊 市場概覽</h2>
    <table>
        <tr><th>指標</th><th>現狀</th><th>趨勢</th></tr>
        <tr><td>住宅價格</td><td>調整中</td><td>📉</td></tr>
        <tr><td>寫字樓</td><td>供過於求</td><td>📉</td></tr>
        <tr><td>零售鋪位</td><td>復甦中</td><td>📈</td></tr>
        <tr><td>工業大廈</td><td>穩定</td><td>➡️</td></tr>
    </table>
</div>

<div class="slide" id="slide3">
    <h2>📈 住宅市場</h2>
    <table>
        <tr><th>地區</th><th>價格/尺</th><th>變化</th></tr>
        <tr><td>港島</td><td>$18-25k</td><td>-5%</td></tr>
        <tr><td>九龍</td><td>$15-20k</td><td>-3%</td></tr>
        <tr><td>新界東</td><td>$12-16k</td><td>-2%</td></tr>
        <tr><td>新界西</td><td>$10-14k</td><td>持平</td></tr>
    </table>
    <h3>✅ 剛需強 | ❌ 觀望</h3>
</div>

<div class="slide" id="slide4">
    <h2>💼 寫字樓市場</h2>
    <table>
        <tr><th>地區</th><th>空置率</th><th>預測</th></tr>
        <tr><td>中環</td><td>15-20%</td><td>高</td></tr>
        <tr><td>灣仔</td><td>12-18%</td><td>平穩</td></tr>
        <tr><td>港東</td><td>10-15%</td><td>改善</td></tr>
        <tr><td>九龍東</td><td>18-25%</td><td>嚴峻</td></tr>
    </table>
    <h3>📉 需求弱 | 💰 租金跌</h3>
</div>

<div class="slide" id="slide5">
    <h2>🎯 投資機會</h2>
    <table>
        <tr><th>類型</th><th>風險</th><th>回報</th><th>建議</th></tr>
        <tr><td>細價住宅</td><td>中</td><td>5-8%</td><td>✅</td></tr>
        <tr><td>車位</td><td>低</td><td>3-5%</td><td>✅</td></tr>
        <tr><td>重建</td><td>高</td><td>20%+</td><td>💰</td></tr>
    </table>
    <h3>關注: 北部都會區、將軍澳、東涌</h3>
</div>

<div class="slide" id="slide6">
    <h2>⚠️ 風險因素</h2>
    <ul>
        <li>📈 利率上升</li>
        <li>🇨🇳 中國經濟放緩</li>
        <li>🏠 房屋政策轉變</li>
        <li>🌍 全球經濟衰退</li>
    </ul>
    <h3 style="margin-top:20px;">建議: 做好水位、保持現金流、分散投資</h3>
</div>

<div class="slide" id="slide7">
    <h2>🔮 2026預測</h2>
    <table>
        <tr><th>Q</th><th>住宅</th><th>寫字樓</th><th>零售</th></tr>
        <tr><td>Q1</td><td>-3%</td><td>-5%</td><td>+2%</td></tr>
        <tr><td>Q2</td><td>-2%</td><td>-3%</td><td>+3%</td></tr>
        <tr><td>Q3</td><td>持平</td><td>-2%</td><td>+4%</td></tr>
        <tr><td>Q4</td><td>+2%</td><td>持平</td><td>+5%</td></tr>
    </table>
</div>

<div class="slide" id="slide8">
    <h2>🎯 總結</h2>
    <h3 style="color:#ffd700;font-size:24px;margin:20px 0;">市場立場: 審慎樂觀</h3>
    <ul>
        <li>🏠 住宅: 等待 Q3-Q4</li>
        <li>💼 寫字樓: 繼續觀望</li>
        <li>🛍️ 零售: 優質鋪位可考慮</li>
        <li>🏭 工業: 平穩，可適度投資</li>
    </ul>
    <h3 style="margin-top:20px;">關注: 利率、中國經濟、房屋供應</h3>
</div>

<div class="page-num" id="pageNum">1 / 8</div>
<div class="progress" id="progress"></div>
<div class="nav">
    <button onclick="nextSlide()">下一頁 →</button>
</div>

<script>
let currentSlide = 1;
const totalSlides = 8;
let startX = 0;

function showSlide(n) {
    document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
    document.getElementById('slide' + n).classList.add('active');
    document.getElementById('progress').style.width = (n / totalSlides * 100) + '%';
    document.getElementById('pageNum').textContent = n + ' / ' + totalSlides;
}

function nextSlide() {
    currentSlide = currentSlide >= totalSlides ? 1 : currentSlide + 1;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = currentSlide <= 1 ? totalSlides : currentSlide - 1;
    showSlide(currentSlide);
}

// Touch/swipe support
document.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
});

document.addEventListener('touchend', (e) => {
    const diff = startX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
        if (diff > 0) nextSlide();
        else prevSlide();
    }
});

// Keyboard
document.addEventListener('keydown', (e) => {
    if(e.key === 'ArrowRight' || e.key === ' ') nextSlide();
    if(e.key === 'ArrowLeft') prevSlide();
});

showSlide(1);
</script>
</body>
</html>
"""

with open("/Users/macbookpro/.openclaw/workspace/company/hk_property_mobile.html", "w") as f:
    f.write(SLIDE_TEMPLATE)

print("✅ Mobile-friendly slides created!")
print("File: hk_property_mobile.html")

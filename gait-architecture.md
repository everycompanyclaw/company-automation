# Gait Analysis App - Architecture Note

## 1. iPhone Camera Capabilities

### What Can Be Done with Just iPhone?

#### Reality Check
| Capability | Limit | Notes |
|------------|-------|-------|
| Frame rate | 240fps (slow-mo) | Enough for gait |
| Resolution | 4K | Good detail |
| ARKit | Yes | Body tracking available |
| LiDAR | iPhone 12+ | Depth sensing |
| Accuracy | ~95% vs markers | Clinical vs research |

#### Key Limitations
- **Lighting**: Needs good lighting
- **Angle**: Must see full body
- **Distance**: 2-4 meters optimal
- **Clothing**: Loose clothes may affect

### ARKit Body Tracking
- `ARKit 5+` has body tracking
- 57 skeleton joints
- Real-time pose estimation
- Works without markers

---

## 2. MVP Feature Set

### Phase 1 (MVP) - 3 months

#### Core Features
1. **Video Capture**
   - Record walking (front/side view)
   - Guide user positioning
   - Auto-detect gait cycle

2. **Basic Analysis**
   - Step frequency (cadence)
   - Step length
   - Walking speed
   - Symmetry score

3. **Report Generation**
   - PDF report
   - Simple visualizations
   - Recommendations

4. **History**
   - Track over time
   - Compare sessions

#### What Can Work Offline?
- Video capture: Yes
- Basic analysis: Yes (on-device ML)
- Report generation: Yes

#### Cloud-Only Features
- Advanced analysis (optional)
- Share with clinic
- Enterprise features

---

## 3. Tech Stack Comparison

### Option A: Native iOS (Swift)

| Factor | Rating | Notes |
|--------|--------|-------|
| Performance | ⭐⭐⭐⭐⭐ | Best |
| Dev Speed | ⭐⭐⭐ | Slower |
| Cost | ⭐⭐ | Mac only |
| ARKit Access | ⭐⭐⭐⭐⭐ | Native |
| Cross-platform | ❌ | iOS only |

**Pros**: Best performance, native ARKit
**Cons**: Single platform, slower development

### Option B: Flutter

| Factor | Rating | Notes |
|--------|--------|-------|
| Performance | ⭐⭐⭐⭐ | Good |
| Dev Speed | ⭐⭐⭐⭐ | Fast |
| Cost | ⭐⭐⭐ | Cross-platform |
| ARKit Access | ⭐⭐⭐ | Plugins exist |
| Web Support | ⭐⭐⭐ | Limited |

**Pros**: Cross-platform, fast dev
**Cons**: ARKit plugins less mature

### Option C: React Native

| Factor | Rating | Notes |
|--------|--------|-------|
| Performance | ⭐⭐⭐ | Good |
| Dev Speed | ⭐⭐⭐⭐ | Fast |
| Cost | ⭐⭐⭐ | Cross-platform |
| ARKit Access | ⭐⭐⭐ | Via native modules |
| Web Support | ⭐⭐⭐⭐ | Good |

**Pros**: Large ecosystem, web support
**Cons**: More complex for AR

### Option D: Web Portal (Separate)

| Factor | Rating | Notes |
|--------|--------|-------|
| Tech | React/Vue | Modern stack |
| Purpose | Reports only | Web dashboard |
| Hosting | Vercel/Netlify | Cheap |

---

## 4. Recommendation

### Primary: Native iOS (Swift)
- Best ARKit access
- Most mature body tracking
- Clinical-grade accuracy

### Secondary: Flutter
- If cross-platform needed later
- Faster initial development

### Web Portal
- Separate project
- React + Next.js
- For detailed reports

---

## 5. Phased Roadmap

### Phase 1: MVP (Months 1-3)
- [ ] iOS app with video capture
- [ ] Basic gait analysis (cadence, length, speed)
- [ ] Simple PDF report
- [ ] Local storage
- **Target**: Launch to 50 beta users

### Phase 2: Enhanced (Months 4-6)
- [ ] ARKit body tracking integration
- [ ] More metrics (angles, posture)
- [ ] History + trends
- [ ] Basic subscription (Freemium)
- **Target**: 500 users, first revenue

### Phase 3: Enterprise (Months 7-12)
- [ ] Clinic dashboard (Web portal)
- [ ] API for physiotherapists
- [ ] Export to clinical formats
- [ ] B2B pricing
- **Target**: 10 clinic partners

### Phase 4: Scale (Year 2)
- [ ] Android support (Flutter)
- [ ] Regional expansion (Singapore, Taiwan)
- [ ] Wearable integration (Apple Watch)
- [ ] AI insights

---

## 6. Technical Architecture

### App Architecture
```
┌─────────────────────────────────┐
│         iOS App (Swift)         │
├─────────────────────────────────┤
│  UI Layer (SwiftUI)            │
│  Business Logic (MVVM)          │
│  ML Core (CoreML + ARKit)       │
│  Local Storage (SQLite)         │
└─────────────────────────────────┘
              │
              ▼ (optional)
┌─────────────────────────────────┐
│      Backend (if needed)        │
├─────────────────────────────────┤
│  API (Node.js/FastAPI)          │
│  Auth (Firebase/Supabase)       │
│  Storage (S3)                   │
│  Analytics                      │
└─────────────────────────────────┘
```

### Web Portal Architecture
```
┌─────────────────────────────────┐
│      Web Portal (React)         │
├─────────────────────────────────┤
│  Next.js 14 (App Router)        │
│  Dashboard + Reports            │
│  Auth integration               │
│  Hosting: Vercel                │
└─────────────────────────────────┘
```

---

## 7. Key Trade-offs

### Native iOS vs Cross-Platform

| Decision | Recommendation | Reason |
|----------|---------------|--------|
| First platform | iOS | ARKit maturity |
| When to add Android | After market validation | Focus |
| Web portal timing | After MVP | Separate team |
| Cloud backend | Minimal initially | Keep simple |

### Cost Estimates

| Phase | Cost (HK$) | Time |
|-------|------------|------|
| MVP | $50-80k | 3 months |
| Phase 2 | $80-120k | 6 months |
| Phase 3 | $100-150k | 12 months |
| **Total Year 1** | **$230-350k** | |

---

## 8. Privacy Architecture

### Data Strategy
1. **On-device first** - Process locally
2. **Minimal cloud** - Only if user chooses
3. **No biometric storage** - Delete after analysis
4. **HK data centers** - If cloud needed

### Compliance
- PDPO compliant
- No special license needed (not medical device)
- Disclaimer: Not for clinical diagnosis

---

## 9. Success Metrics

### KPIs
| Metric | Target (6 months) |
|--------|------------------|
| Downloads | 5,000 |
| Active users | 1,000 |
| Paid conversions | 5% |
| Clinic partnerships | 5 |

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Accuracy not clinical-grade | Clear disclaimers, target wellness not clinical |
| Competition | Focus on HK/China, Chinese language |
| Privacy concerns | Local processing, clear policy |
| Apple policy changes | Build web fallback |

---

*Architecture Note v1.0*
*More details available on request*

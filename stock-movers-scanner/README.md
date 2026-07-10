# NIFTY 500 Stock Movers Scanner

Har date ke liye NIFTY 500 stocks ke top gainers/losers (>=3% move) — Python backend + Flutter app (macOS/iOS/Android).

---

## STEP 1 — Supabase Setup

1. https://supabase.com pe naya project banao
2. **SQL Editor** kholo, `supabase_schema.sql` ka poora content paste karke run karo
3. **Project Settings → API** se copy karo:
   - `Project URL` → yeh `SUPABASE_URL`
   - `anon public` key → Flutter app ke liye
   - `service_role` key → Python backend ke liye (zyada permissions, secret rakhna)

---

## STEP 2 — Python Backend (local test)

```bash
cd python
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# .env file kholo aur SUPABASE_URL + SUPABASE_KEY (service_role key) daal do
```

**Test run (aaj ki date ke liye):**
```bash
python main.py
```

**Specific date ke liye:**
```bash
python main.py 2026-07-09
```

**Backfill — last 30 din ka data ek saath:**
```bash
python backfill.py 30
```
Yeh 1-1 second gap ke saath 30 din loop karega. Weekend/holiday automatically skip ho jayega (NSE data hi nahi milega us din).

`watchlist.json` mein already tumhari 500 NIFTY symbols daal di hain (uploaded CSV se generate ki hain).

---

## STEP 3 — GitHub Actions (daily automation)

1. Is poore `stock-movers-scanner` folder ko naye GitHub repo mein push karo:
```bash
cd stock-movers-scanner
git init
git add .
git commit -m "initial setup"
git remote add origin https://github.com/<tumhara-username>/stock-movers-scanner.git
git push -u origin main
```

2. GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**
   - `SUPABASE_URL` add karo
   - `SUPABASE_KEY` add karo (service_role key)

3. Workflow already `.github/workflows/daily_scan.yml` mein hai — roz 6:30 PM IST (market close ke baad) automatically chalega. Manual trigger ke liye **Actions tab → Daily Stock Movers Scan → Run workflow**.

---

## STEP 4 — Flutter App

```bash
cd flutter_app
flutter create . --platforms=macos,ios,android   # existing files overwrite nahi honge, sirf platform folders add honge
flutter pub get
```

`lib/main.dart` kholo aur yeh 2 lines apni Supabase details se replace karo:
```dart
const supabaseUrl = 'https://your-project-ref.supabase.co';
const supabaseAnonKey = 'your-anon-key';   // anon key, service_role NAHI (security ke liye)
```

**Run karo:**
```bash
flutter run -d macos      # Mac
flutter run -d chrome     # quick test browser mein
flutter run               # connected iOS/Android device
```

iOS/macOS build ke liye Xcode installed hona chahiye, Android ke liye Android Studio SDK.

---

## Flow Summary

```
NSE Bhavcopy (daily CSV)
      ↓
Python: fetch → filter (NIFTY 500 watchlist) → compute % change → filter >=3%
      ↓
Supabase (daily_movers table)
      ↓
Flutter app: date pick → query Supabase → show Gainers/Losers tabs
```

GitHub Actions roz automatically Python script chalayega — tumhe kuch manually nahi karna padega, sirf app kholke date select karni hai.

---

## Notes

- NSE bhavcopy sirf trading days ke liye available hota hai — weekend/holiday pe empty result aayega, yeh normal hai.
- `THRESHOLD_PCT` `compute_movers.py` mein change kar sakte ho agar 3% ke alawa kuch aur chahiye.
- Watchlist update karni ho to `python/watchlist.json` edit karo — symbol add/remove karke seedha save.
- Service role key kabhi Flutter app ya client-side code mein mat daalna — sirf Python backend/GitHub Actions secrets mein.

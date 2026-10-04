# Django Web 練習專案

以 Django 製作的網站練習作品，包含會員登入、商品訂購、購物車，以及電子發票自動查詢功能。

## 功能

- **會員登入／登出**：未登入時無法進入其他頁面
- **側邊欄導覽**：選單項目存放在資料庫，支援父子節點摺疊
- **商品菜單**：以卡片顯示商品圖片與價格，可選擇數量加入訂購車
- **訂購車**：修改數量、移除商品，自動重新計算總金額
- **電子發票查詢**：
  - 以 Selenium 自動登入財政部電子發票整合服務平台
  - 以 Tesseract OCR 自動辨識圖形驗證碼，辨識失敗會自動重試
  - 依指定日期區間抓取發票資料並顯示在表格中
  - 可將查詢結果匯出成 Excel

## 使用技術

| 類別 | 技術 |
|---|---|
| 後端 | Python 3.11、Django 5.2 |
| 前端 | Bootstrap 4、Vue 2、Vue Easytable、SweetAlert2、SheetJS |
| 爬蟲 | Selenium、webdriver-manager、BeautifulSoup |
| 驗證碼辨識 | Tesseract OCR、pytesseract、Pillow |
| 資料處理 | pandas |
| 資料庫 | SQLite |

## 專案結構

```
├── requirements.txt
└── mysite/                 # Django 專案根目錄
    ├── manage.py
    ├── config/             # 專案設定 (settings、urls)
    ├── accounts/           # 會員登入／登出
    ├── webapp/
    │   ├── models/         # 商品、訂單、導覽選單
    │   ├── views/          # 各頁面的處理邏輯
    │   └── utils/          # 導覽選單、發票爬蟲與 Tesseract-OCR
    └── templates/          # 網頁模板
```

## 安裝

需要先安裝：

- Python 3.11
- Google Chrome (發票查詢功能使用)

建立虛擬環境並安裝套件：

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Tesseract OCR 已放在 `mysite/webapp/utils/Tesseract-OCR/`，不需另外安裝。

## 執行

**方法一：VS Code**

用 VS Code 開啟專案資料夾，按 `F5` 選擇「Django: 啟動網站」。

**方法二：終端機**

```powershell
cd mysite
..\.venv\Scripts\python.exe manage.py runserver
```

啟動後開啟瀏覽器進入 http://127.0.0.1:8000/

## 使用方式

1. 在登入頁輸入帳號密碼登入
2. 從左側選單切換頁面
3. **商品菜單**：選擇數量後加入訂購車
4. **訂購車**：修改數量或移除商品
5. **發票查詢**：
   1. 輸入電子發票平台的手機條碼帳號與密碼
   2. 選擇起始與結束日期 (須在同一個月，且在可查詢的期數內)
   3. 想看瀏覽器自動操作的過程，可勾選「開啟有頭模式」
   4. 按下查詢，等待程式自動登入並抓取資料
   5. 查詢完成後可按「匯成 EXCEL」下載結果

管理後台：http://127.0.0.1:8000/admin/ (需管理員帳號)，可管理商品與導覽選單。

## 常見問題

**Q：按 F5 或執行時出現 `No module named 'django'`？**
A：套件沒有裝進 `.venv`，請依「安裝」步驟執行 `pip install -r requirements.txt`。

**Q：忘記網站登入密碼？**
A：密碼經過加密無法查回，可重設：

```powershell
cd mysite
..\.venv\Scripts\python.exe manage.py changepassword 帳號
```

**Q：發票查詢一直失敗或卡住？**
A：

- 確認電腦已安裝 Google Chrome
- 第一次執行時 webdriver-manager 會自動下載 ChromeDriver，需要網路連線
- 驗證碼辨識有時會失敗，程式會自動重試，請稍候
- 財政部網站改版可能導致抓不到元素，需要調整 `webapp/utils/invoice.py`

**Q：為什麼發票日期不能跨月？**
A：電子發票平台一次只能查詢同一個月份的資料。

**Q：執行後 `db.sqlite3`、`captcha.png` 出現在變更清單？**
A：登入網站會寫入登入紀錄，發票查詢會下載新的驗證碼圖片，屬於正常現象，不需要 commit。

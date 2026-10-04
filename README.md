# Django 網站練習

以 Django 製作的快餐店訂購網站，登入後可以瀏覽菜單、加入訂購車，並自動登入財政部電子發票平台查詢發票資料。

> 聯成電腦 Python Django 課程的練習作品，重新整理的版本。

## 功能

- **會員登入／登出**，未登入時無法進入其他頁面
- 左側選單存放在資料庫，可以在管理後台新增、調整順序，支援**父子節點摺疊**
- **菜單**：以卡片顯示商品圖片、說明與價格，選擇數量後加入訂購車
- **訂購車**：修改數量、移除商品，**自動重新計算總金額**
- **發票資料查詢**：
  - 用 Selenium 自動登入[財政部電子發票整合服務平台](https://www.einvoice.nat.gov.tw/)
  - 用 Tesseract OCR **自動辨識圖形驗證碼**，辨識失敗會自動換一張重試
  - 依日期區間抓取所有分頁的發票，顯示在表格中
  - 查詢結果可以一鍵**匯出成 Excel**
- 所有提示訊息使用 SweetAlert2 跳窗

| 類別 | 使用技術 |
|---|---|
| 後端 | Django 5.2、SQLite |
| 前端 | Bootstrap 4、Vue 2、Vue Easytable、SweetAlert2、SheetJS |
| 爬蟲 | Selenium、webdriver-manager、BeautifulSoup、pandas |
| 驗證碼辨識 | Tesseract OCR、pytesseract、Pillow |

---

## 安裝

### 1. 事前準備

| 項目 | 說明 |
|---|---|
| **Python 3.10 以上** | 到 [python.org](https://www.python.org/downloads/) 下載 |
| **Google Chrome** | 發票查詢透過 Chrome 開啟網頁抓資料，一定要安裝 |

> 不需要自己下載 chromedriver 和 Tesseract：chromedriver 第一次查詢時會自動下載（需要網路），Tesseract 已附在專案裡。

### 2. 下載專案

```
git clone https://github.com/tedchen05/django-web-practice.git
cd django-web-practice
```

### 3. 建立虛擬環境並安裝套件

在專案資料夾開啟終端機，執行：

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> 套件會裝在專案內的 `.venv`，不會影響電腦上其他的 Python。

---

## 執行

### 方法一：終端機

在專案資料夾執行：

```
cd mysite
..\.venv\Scripts\python.exe manage.py runserver
```

### 方法二：VS Code 按 F5

1. 用 VS Code 開啟專案資料夾（第一次開啟時，右下角會建議安裝 Python 擴充功能，按「安裝」）
2. 按 **F5**，會自動使用專案內的 `.venv` 啟動網站

在「執行與偵錯」面板（`Ctrl + Shift + D`）上方的選項是「**Django: 啟動網站**」，按 `Shift + F5` 停止。

啟動後用瀏覽器開啟 http://127.0.0.1:8000/

---

## 使用方式

1. 在登入頁輸入帳號、密碼登入
2. 從左側選單切換頁面：
   - **快餐店 → 菜單**：輸入數量，按「訂購」加入訂購車
   - **快餐店 → 訂購車**：按「修改」調整數量，或按「移除」刪除商品，下方顯示總金額
   - **爬蟲 → 發票資料**：查詢電子發票（見下方）
   - **管理**：進入 Django 管理後台，新增商品、調整選單（需要管理員帳號）
3. 左側選單上方按「**登出**」離開

**發票資料查詢**

1. 輸入電子發票平台的**手機條碼帳號**與密碼
2. 選擇起始與結束日期（必須在**同一個月**；雙月可查最近 4 期、單月可查最近 5 期）
3. 想看瀏覽器自動操作的過程，可以勾選「**開啟有頭模式**」
4. 按「**確定**」，等待程式登入並抓取資料（按 Enter 也可以）
5. 查詢完成後按「**匯成 EXCEL**」，下載 `發票資料_起始日_結束日.xlsx`

> 發票帳密只用來登入平台，不會存進資料庫或任何檔案。

---

## 已知限制

- **網站改版可能失效**：發票爬蟲依賴平台的網頁結構，改版後需要修改 `mysite/webapp/utils/invoice.py` 中的 XPath
- **日期不能跨月**：電子發票平台一次只能查詢同一個月份

---

## 常見問題

**Q：出現 `ModuleNotFoundError: No module named 'django'`？**
執行用的 Python 沒有安裝套件。照「安裝」第 3 步建立 `.venv` 並安裝套件，再用 `.venv` 執行。

**Q：VS Code 在 `import django` 底下畫波浪線，顯示「無法解析匯入」？**
VS Code 選到的 Python 不是 `.venv`。按 `Ctrl + Shift + P`，輸入 `Python: Select Interpreter`，選擇 `.venv`。

**Q：忘記網站的登入密碼？**
密碼經過加密無法查回，只能重設：

```
cd mysite
..\.venv\Scripts\python.exe manage.py changepassword 帳號
```

**Q：發票查詢第一次很久，或出現 chromedriver 相關錯誤？**
第一次會自動下載 chromedriver，需要網路，請稍等。並確認電腦已安裝 Google Chrome。

**Q：發票查詢顯示「使用者帳號或密碼錯誤」？**
這是電子發票平台回傳的訊息，請確認輸入的是平台的手機條碼帳號與密碼，不是這個網站的帳密。

**Q：執行後 `db.sqlite3`、`captcha.png` 出現在 git 的變更清單？**
登入網站會寫入登入紀錄，查詢發票會存下新的驗證碼圖片，屬於正常現象，捨棄變更即可。

---

## 檔案說明

```
django-web-practice/
├── requirements.txt               # 需要安裝的套件
├── mysite/
│   ├── manage.py                  # Django 執行入口
│   ├── db.sqlite3                 # 資料庫（帳號、商品、選單、訂購車）
│   ├── config/                    # 專案設定（settings、網址總表）
│   ├── accounts/                  # 會員登入／登出
│   ├── webapp/
│   │   ├── models/                # 資料表：商品、訂購車、選單
│   │   ├── views/                 # 各頁面的處理：菜單、訂購車、發票
│   │   └── utils/
│   │       ├── home.py            # 組出左側選單的父子節點
│   │       ├── invoice.py         # 發票爬蟲：登入、辨識驗證碼、抓取資料
│   │       └── Tesseract-OCR/     # 驗證碼辨識程式
│   └── templates/                 # 網頁模板
└── .vscode/
    ├── launch.json                # VS Code 按 F5 的執行設定
    └── extensions.json            # 建議安裝的 VS Code 擴充功能
```

## 注意事項

本專案僅供學習 Django 與 Python 爬蟲使用。發票查詢請使用自己的帳號，並避免短時間大量查詢，以免造成平台負擔。

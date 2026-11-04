# 公開披露證據帳本

[English](README.md) · [網站](https://filings.vesperai.space/zh-Hant/)

把使用者提供的公開披露引文與數值，整理成本機 Markdown 帳本與 JSON 欄位缺漏清單。

## 執行

需要 Python 3.10+。clone 後在儲存庫根目錄操作：

```sh
git clone https://github.com/Vesper2026/filing-evidence-ledger.git
cd filing-evidence-ledger
# No runtime dependencies; Python 3.10+ is sufficient.
python filing_evidence.py examples/sample.json --output examples/output
```

不需要第三方執行期套件。也可在本專案的 venv 內安裝 `.` 以取得 CLI 入口；直接執行腳本不必安裝。

## 輸入與真實範例輸出

```text
{"evidence":[{"id":"E01","question":"Revenue?","title":"Synthetic","source_url":"https://github.com/Vesper2026/filing-evidence-ledger/blob/main/examples/sample.json","location":"synthetic p12","quote":"Revenue was USD 12 million for FY2025.","value":"12.00","currency":"USD","unit":"million","period":"FY2025"}]}
```

隨附完整範例（不只是上面的縮寫說明）會產生：

```text
3 evidence rows; 2 need field review. Sources not verified.
```

隨附合成範例有三筆資料。E01 保留 `12.00`；E02 產生 `missing:period`；E03 產生 `missing:quote`。輸出 `ledger.json` 與 `ledger.md`。數值應使用 JSON 字串。必要欄位為 id、question、title、source_url、location、quote；有非空數值時還要 unit 與 period。currency 與 disclosed_on 原樣保存，不自行推斷。重複 ID 逐筆保留並標示。預設 `unreviewed`，`reviewed` 只記錄你的狀態，不是程式批准。

## 核心測試

```sh
python -m unittest discover -p "test_*.py"
```

測試驗證核心規則與合成範例，不驗證使用者文件的事實或翻譯品質。

## 限制與資料處理

不抓來源、不檢查網址是否在線、不核實引文、不計算財務或提供投資建議。欄位完整不代表事實成立。合成範例的來源連結指向範例自身，不是發行人公告。本機讀取輸入並寫報告，不上傳文件。輸出轉義 Markdown 特殊字元與 HTML；若整合到其他系統，仍應把內容視為使用者輸入。

## 本工具的獨立雙語站

```sh
python site/build.py
python -m http.server 8090 --directory docs
```

開啟 http://localhost:8090/zh-Hant/ 或 /en/。來源在 `site/`，輸出在 `docs/`，範例複製到 `docs/downloads/`。每種語言有兩篇原創文章，以及獨立 hostname、canonical、sitemap、robots 與 CNAME；沒有追蹤分析或上傳表單。

## 實用工具

[Eqvero](https://eqvero.com/) 可搭配本工具使用。KolmoPDF 雲端服務會上傳文件，本機開源 CLI 不取代其專有解析器。

## 授權

自有程式、合成資料、文件與靜態站來源採 MIT，見 LICENSE；第三方依賴保留原授權。

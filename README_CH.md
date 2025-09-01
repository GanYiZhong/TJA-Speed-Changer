## 專案簡介
TJA Speed Changer GUI 是一個用於太鼓譜面（TJA）與音源變速的圖形化工具，透過介面操作即可同時調整譜面參數與音訊速度並輸出 OGG 檔案。
本工具以 Python 的 Tkinter 建構 GUI，並整合 FFmpeg 的 atempo 音訊濾鏡，達成變速同時維持音高的處理流程。

## 功能
- GUI 介面：以 Tkinter 提供易用的視覺化操作，無需撰寫指令即可完成變速與轉檔。  
- 多語系支援：提供英文、繁體中文與日文（日本語），介面可即時切換顯示語言。  
- 智慧音訊處理：自動將 MP3/WAV/FLAC/M4A/AAC 等音訊轉為 OGG（Vorbis），並同時進行變速處理
- TJA 檔處理：可調整 BPM、OFFSET、DEMOSTART、#BPMCHANGE、#DELAY 等，並自動更新 WAVE 指向之音檔副檔名與名稱後綴。  
- 彈性音訊輸入：自動在同資料夾搜尋多種副檔名的音源檔以進行處理（mp3、wav、ogg、flac、m4a、aac）。  
- 獨立可執行檔：可打包為單一執行檔，並夾帶 FFmpeg 或使用系統已安裝的 FFmpeg 執行檔運行。

## 系統需求
- 執行檔模式：Windows 10/11（64 位元），免安裝其他依賴（FFmpeg 可隨執行檔附帶）。  
- 開發模式：Python 3.8+、先安裝 requirements.txt 之套件、並準備可用的 FFmpeg 二進位檔以供執行。

## 安裝
### 方式一：下載已編譯執行檔
1. 於發行頁下載 TJASpeedChangerGUI.exe 後直接執行，無需安裝其他軟體。  
2. 若內含 FFmpeg，將可直接進行音訊變速與 OGG 轉檔；否則可改用系統路徑中的 FFmpeg。

### 方式二：從原始碼建置
1. 取得原始碼  
   ```bash
   # 若使用 git
   git clone https://github.com/GanYiZhong/TJA-Speed-Changer
   ```
   以上步驟取得程式碼後進入專案目錄以便安裝與執行。  
2. 安裝依賴  
   ```bash
   pip install -r requirements.txt
   ```
   先安裝相依套件方能正確載入 GUI 與執行音訊處理功能
3. 下載 FFmpeg  
   ```bash
   python download_ffmpeg.py
   ```
   準備 FFmpeg 二進位以供後續處理 OGG/Vorbis 編碼與 atempo 濾鏡變速。
4. 執行 GUI  
   ```bash
   # 進階版（建議，功能完整）
   python TJASpeedChangerGUI_Enhanced.py
   # 或精簡版（不依賴拖放外掛）
   python TJASpeedChangerGUI_Simple.py
   ```
   若使用拖放功能則需 tkinterdnd2；無拖放需求可使用純 Tkinter 版本。
5. 打包單一執行檔（選用）  
   ```bash
   python build_exe.py
   ```
   可透過 PyInstaller 的單檔模式（--onefile）與附帶資料機制（如以 sys._MEIPASS 取用捆綁資源）完成分發封裝。

## 使用方式
### 圖形介面
1. 選擇 TJA 檔案  
   - 點擊「Browse…」選取 .tja 檔案，或直接拖放至視窗（進階版）。
2. 調整速度  
   - 以滑桿設定倍率（0.5x 至 2.0x），介面會即時顯示選取速度。  
3. 語言切換  
   - 由下拉選單切換語言，介面文字將即時更新。  
4. 開始處理  
   - 點擊「Process Files」，於結果區觀察進度，完成後會產生含速度後綴的新檔案。

### 指令列（原始）
```bash
python TJASpeedChanger.py song.tja 1.2 --lang en
```
指令列模式可直接指定 TJA 路徑、速度倍率與語言代碼，適合自動化與批次處理情境。

## 檔案處理內容
### TJA 譜面
- BPM：依速度倍率成比例調整（乘上倍率）以維持節奏關係。  
- OFFSET：依速度倍率反比調整（除以倍率）以維持對齊起點感受。
- DEMOSTART：依速度倍率反比調整以維持展示段落時間點。
- BPMCHANGE：譜面內部的節奏變化全部依倍率等比調整。  
- DELAY：延遲指令依倍率等比調整以維持節奏推進一致。  
- WAVE：自動更新音檔檔名與副檔名（改為 OGG 並加上速度後綴）。  
- TITLE：標題將附加速度標記，利於辨識多版本輸出。  

### 音訊
- 自動尋找多種常見副檔名（mp3、wav、ogg、flac、m4a、aac），減少手動指定負擔。  
- 一律轉為 OGG（Vorbis）以維持專案的一致性與相容性。  
- 使用 FFmpeg atempo 濾鏡進行變速，於標準範圍內可維持音高不變（不改變頻率）。
- 以 Vorbis 品質參數（-q:a）或位元率（-b:a）配置高品質輸出；品質等級與位元率具對應關係可供參考。  
- 對於極端倍率可串接多個 atempo 節點以獲得更穩定的處理結果。  

## 輸出檔案
工具會建立附帶速度後綴的新檔：  
- song_1.20x.tja（已更新 WAVE 指向與譜面參數）。  
- audio_1.20x.ogg（變速後且轉為 OGG/Vorbis 的音檔）。
注意：所有音訊最終輸出皆為 OGG 格式，原始檔案不會被覆寫或修改。  

## 語言支援
- 支援語言：English（en）、繁體中文（zh-tw）、日本語（ja），可於 GUI 即時切換。  
- 語言檔位於 languages/ 目錄，新增語言時可複製既有 JSON 作為模板以擴充。  

## 技術細節
### 架構
- GUI：採用 Tkinter，進階版可整合 tkinterdnd2 提供拖放體驗。
- 音訊處理：使用 FFmpeg（libavfilter）與 atempo 濾鏡以達成變速處理。
- 編碼偵測：讀取 TJA 檔時做編碼處理，確保內容可正確解析與重寫。  
- 執行緒：背景執行處理流程以維持 GUI 的回應與操作流暢度。  

### FFmpeg 整合
- 可夾帶靜態 FFmpeg 到可執行檔，或自動回落使用系統的 FFmpeg。
- atempo 可於 0.5–2.0 範圍直接運作；更極端倍率可藉由串接多個 atempo 節點實現目標速度。
- 以 libvorbis 編碼 OGG，常用參數如 -q:a（品質）或 -b:a（位元率）可依需求取捨。  

### 打包系統
- 使用 PyInstaller 產生單一檔案的可執行程式（--onefile）以利分發。  
- 附加資料（如 FFmpeg、語言檔、圖檔）可透過打包選項與在執行時以 sys._MEIPASS 取用。  
- 若使用 .spec 檔，對應之命令列選項需遵循版本相容規則（例如 --onefile 與 .spec 的行為差異）。  

## 疑難排解
- 「找不到 FFmpeg」：於開發模式先執行下載腳本或安裝系統 FFmpeg；打包版通常已內含或可設定搜尋路徑。
- 「無法讀取 TJA 檔」：請檢查檔案是否損壞或編碼不相容，可先以文字編輯器檢視，再重試處理。  
- 「無效的檔案類型」：僅支援 .tja，請確認副檔名與檔案內容格式。  
- 「音訊處理失敗」：請確認音檔存在且可解碼、磁碟空間足夠，必要時可僅轉成 OGG 再行測試。

## 效能說明
- 大型音訊檔轉檔時間較長，變速與轉碼會依檔案長度與設定而影響耗時。  
- 極端變速倍率需串接 atempo，處理時間與資源占用將增加。  
- 處理於背景執行，GUI 在過程中仍保持可操作與回應。  

## 開發資訊
### 專案結構（範例）
```
taikojiro292/
├── TJASpeedChangerGUI_Enhanced.py     # 進階 GUI（含新功能）
├── TJASpeedChangerGUI_Simple.py       # 精簡 GUI（無外部拖放依賴）
├── TJASpeedChangerGUI.py              # 原始 GUI（參考）
├── TJASpeedChanger.py                 # 增強的指令列工具
├── download_ffmpeg.py                 # 下載 FFmpeg 工具
├── build_exe.py                       # 產生可執行檔腳本
├── test_enhanced_features.py          # 新功能測試腳本
├── requirements.txt                   # 依賴套件
├── languages/                         # 語言資源
│   ├── en.json
│   ├── zh-tw.json
│   └── ja.json
└── README.md                          # 本文件
```
此結構利於區隔 GUI、指令列、打包與語系資源，便於維護與擴充。  
### 新增語言
1. 於 languages/ 新增對應語言 JSON，建議複製既有檔作為模板。  
2. 將語言代碼加入 GUI 的語言選單與載入流程並測試顯示。  

### 修改打包流程
- 可於 build_exe.py 調整 PyInstaller 參數（如單檔模式、隱藏匯入、資料檔）以符合分發需求。  
- 依需求更新 requirements 與版本資訊，確保相依套件與標示一致。  

## 授權
本專案以開源方式提供，允許修改與再散布，請遵循所選授權條款與相依專案（如 FFmpeg、PyInstaller）之授權要求。

## 貢獻
歡迎提出 PR／Issue：請於提交前完成測試、更新文件，並維持既有程式風格與多語系字串同步。

## 致謝
- FFmpeg 專案（音訊處理、atempo 濾鏡、OGG/Vorbis 編碼）。
- Tkinter 與相關生態（含 tkinterdnd2 拖放外掛於進階版）。
- PyInstaller（可執行檔打包與單檔分發）。

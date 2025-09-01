# ZhongTaiko Logo Setup

## 自動設置（推薦）

執行設置腳本來自動安裝相依性並創建Logo：

```bash
python setup.py
```

## 手動設置

### 1. 安裝Pillow（圖片處理）

```bash
pip install Pillow
```

### 2. 創建Logo

```bash
python create_logo.py
```

這會創建 `LOGO_BLACK_TRANS.png` 檔案。

### 3. 使用你自己的Logo

如果你有自己的 `LOGO_BLACK_TRANS.png` 檔案：

1. 將檔案放在與程式相同的目錄中
2. 確保檔案名稱為 `LOGO_BLACK_TRANS.png`
3. 建議尺寸：寬度不超過300px以獲得最佳顯示效果

## Logo功能

- **點擊Logo**：會自動在預設瀏覽器中打開 https://taiko.ac
- **作者資訊**：顯示 "by ZhongTaiko Studios"
- **自動調整**：Logo會自動縮放至適當大小（最大寬度150px）
- **後備顯示**：如果沒有圖片檔案或Pillow，會顯示文字Logo

## 故障排除

### Logo不顯示
- 確認 `LOGO_BLACK_TRANS.png` 在程式目錄中
- 安裝Pillow：`pip install Pillow`
- 如果仍有問題，程式會使用文字Logo

### 無法點擊
- 確認網路連接
- 檢查預設瀏覽器設定

### Logo太大/太小
- 程式會自動調整大小
- 如果需要調整，可以編輯原始圖片檔案
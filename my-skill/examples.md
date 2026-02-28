# 使用示例

## 基本用法

### 示例 1：提取本地 PDF
```
用户：提取 PDF: D:\documents\report.pdf
助手：正在读取 PDF 文件：D:\documents\report.pdf
助手：========================================
      PDF 文件：report.pdf
      总页数：15
      ========================================
      
      [第 1 页]
      这是第一页的内容...
      
      [第 2 页]
      这是第二页的内容...
      
      ========================================
      提取完成
      ========================================
```

### 示例 2：使用相对路径
```
用户：读取 PDF 内容：./docs/manual.pdf
助手：正在读取 PDF 文件：./docs/manual.pdf
助手：✓ 共提取 8 页内容
```

### 示例 3：提取加密 PDF
```
用户：提取 PDF: C:\secure\confidential.pdf
助手：⚠ 该 PDF 文件已加密，请输入密码
用户：123456
助手：✓ 密码验证成功，正在提取内容...
```

## 错误处理示例

### 文件不存在
```
用户：提取 PDF: D:\not_exists.pdf
助手：✗ 错误：文件不存在 - D:\not_exists.pdf
助手：请检查文件路径是否正确
```

### 不是 PDF 文件
```
用户：提取 PDF: D:\document.docx
助手：✗ 错误：不是有效的 PDF 文件 - document.docx
助手：请确保文件扩展名为 .pdf
```

### 扫描版 PDF（无文本）
```
用户：提取 PDF: D:\scanned.pdf
助手：⚠ 警告：该 PDF 可能是扫描版（图片格式），无法提取文本内容
助手：建议使用 OCR 工具处理
```

### 密码错误
```
用户：提取 PDF: C:\secure\file.pdf
助手：⚠ 该 PDF 文件已加密，请输入密码
用户：wrong_password
助手：✗ 密码错误，无法打开文件
```

## 命令行用法

```bash
# 基本用法
python scripts/helper.py "D:\documents\report.pdf"

# 带密码
python scripts/helper.py "C:\secure\file.pdf" -p "123456"

# 输出到文件
python scripts/helper.py "report.pdf" -o "output.txt"

# 只显示指定页码
python scripts/helper.py "report.pdf" --pages 1-5
```

## 支持的文件类型

- 标准文本 PDF
- 加密 PDF（需提供密码）
- 多语言 PDF（中文、英文、日文等）

## 不支持的文件类型

- 纯图片扫描版 PDF（无文本层）
- 损坏的 PDF 文件

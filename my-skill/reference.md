# PDF 内容提取技能 - 参考文档

## 技术背景

### PyMuPDF (fitz)

PyMuPDF 是一个高性能的 PDF 处理库，基于 MuPDF 引擎。它提供了：

- 快速的 PDF 文本提取
- 支持加密 PDF
- 多语言文本支持（包括中文）
- 跨平台兼容（Windows/Linux/macOS）

### 安装

```bash
pip install PyMuPDF
```

### 基本用法

```python
import fitz

# 打开 PDF
doc = fitz.open("document.pdf")

# 遍历所有页面
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text")
    print(text)

# 关闭文档
doc.close()
```

## 常见问题

### 1. 扫描版 PDF 无法提取文本

**问题**：某些 PDF 是由图片组成的扫描件，没有文本层。

**解决方案**：
- 使用 OCR 工具（如 Tesseract）进行文字识别
- 或使用 Adobe Acrobat 的"识别文本"功能预处理

### 2. 加密 PDF 处理

**问题**：PDF 文件有密码保护。

**解决方案**：
- 需要用户提供正确的密码
- 使用 `fitz.open(path, password="xxx")` 打开

### 3. 中文乱码

**问题**：提取的中文显示为乱码。

**解决方案**：
- 确保终端/控制台使用 UTF-8 编码
- Windows 可运行 `chcp 65001` 切换代码页

## 性能优化

### 大文件处理

对于大型 PDF 文件（>100MB），建议：

1. 分页提取，避免一次性加载
2. 使用生成器逐页输出
3. 考虑添加进度条显示

### 内存管理

```python
# 推荐：及时关闭文档
doc = fitz.open("large.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    # 处理文本...
    del page  # 释放页面内存
doc.close()
```

## 扩展功能

### 提取特定页面

```python
def extract_pages(file_path: str, pages: list) -> str:
    doc = fitz.open(file_path)
    content = ""
    for page_num in pages:
        if 0 <= page_num < len(doc):
            page = doc[page_num]
            content += page.get_text("text")
    doc.close()
    return content
```

### 提取目录/大纲

```python
def extract_toc(file_path: str) -> list:
    doc = fitz.open(file_path)
    toc = doc.get_toc()  # 返回 [(level, title, page), ...]
    doc.close()
    return toc
```

### 提取元数据

```python
def extract_metadata(file_path: str) -> dict:
    doc = fitz.open(file_path)
    metadata = doc.metadata
    doc.close()
    return metadata
# 返回：{'title': '...', 'author': '...', 'subject': '...', ...}
```

## 相关资源

- [PyMuPDF 官方文档](https://pymupdf.readthedocs.io/)
- [MuPDF 官网](https://mupdf.com/)
- [GitHub 仓库](https://github.com/pymupdf/PyMuPDF)

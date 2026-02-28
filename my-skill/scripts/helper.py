#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 内容提取助手

功能：从指定的 PDF 文件中提取文本内容并输出到控制台
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("错误：缺少 PyMuPDF 库")
    print("请运行：pip install PyMuPDF")
    sys.exit(1)


def extract_pdf_text(file_path: str, password: str = None) -> dict:
    """
    提取 PDF 文件的文本内容

    Args:
        file_path: PDF 文件路径
        password: 可选的密码（用于加密的 PDF）

    Returns:
        dict: 包含提取结果和状态信息的字典
    """
    result = {
        "success": False,
        "message": "",
        "content": "",
        "page_count": 0,
        "file_name": ""
    }

    # 验证文件路径
    path = Path(file_path)
    if not path.exists():
        result["message"] = f"错误：文件不存在 - {file_path}"
        return result

    if not path.is_file():
        result["message"] = f"错误：路径不是文件 - {file_path}"
        return result

    if path.suffix.lower() != ".pdf":
        result["message"] = f"错误：不是有效的 PDF 文件 - {path.name}"
        return result

    result["file_name"] = path.name

    doc = None
    try:
        # 打开 PDF
        if password:
            doc = fitz.open(path, filetype="pdf", password=password)
        else:
            doc = fitz.open(path)

        # 检查是否需要密码
        if doc.is_encrypted and not password:
            doc.close()
            result["message"] = "encrypted"
            result["success"] = "need_password"
            return result

        page_count = len(doc)
        result["page_count"] = page_count
        content_parts = []

        # 提取每一页的文本
        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text("text")
            content_parts.append(f"[第 {page_num + 1} 页]\n{text}")

        doc.close()

        result["content"] = "\n\n".join(content_parts)
        result["success"] = True
        result["message"] = f"成功提取 {page_count} 页内容"

        # 检查是否为扫描版（无文本）
        total_text_length = sum(len(part) for part in content_parts)
        if total_text_length < 50:
            result["message"] = "警告：该 PDF 可能是扫描版（图片格式），提取的文本内容很少"

    except Exception as e:
        if doc:
            doc.close()
        error_msg = str(e)
        if "password" in error_msg.lower() or "encrypted" in error_msg.lower():
            result["message"] = "错误：密码错误，无法打开文件"
        elif "cannot open" in error_msg.lower() or "damaged" in error_msg.lower():
            result["message"] = f"错误：文件损坏或格式不正确 - {path.name}"
        else:
            result["message"] = f"错误：{str(e)}"

    return result


def print_result(result: dict, output_file: str = None):
    """
    打印或保存提取结果

    Args:
        result: 提取结果字典
        output_file: 可选的输出文件路径
    """
    separator = "=" * 50

    if result["success"] == "need_password":
        print("⚠ 该 PDF 文件已加密，请输入密码")
        return

    if not result["success"]:
        print(f"✗ {result['message']}")
        return

    output_text = []
    output_text.append(separator)
    output_text.append(f"PDF 文件：{result['file_name']}")
    output_text.append(f"总页数：{result['page_count']}")
    output_text.append(separator)
    output_text.append("")
    output_text.append(result["content"])
    output_text.append("")
    output_text.append(separator)
    output_text.append("提取完成")
    output_text.append(separator)

    final_output = "\n".join(output_text)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"✓ 内容已保存到：{output_file}")
    else:
        print(final_output)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="PDF 内容提取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python helper.py "D:\\documents\\report.pdf"
  python helper.py "C:\\secure\\file.pdf" -p "123456"
  python helper.py "report.pdf" -o "output.txt"
        """
    )

    parser.add_argument(
        "file_path",
        help="PDF 文件路径"
    )
    parser.add_argument(
        "-p", "--password",
        default=None,
        help="PDF 密码（用于加密文件）"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="输出文件路径（可选，默认输出到控制台）"
    )

    args = parser.parse_args()

    print(f"正在读取 PDF 文件：{args.file_path}")

    result = extract_pdf_text(args.file_path, args.password)

    # 如果需要密码，交互式获取
    if result["success"] == "need_password":
        import getpass
        password = getpass.getpass("请输入 PDF 密码：")
        result = extract_pdf_text(args.file_path, password)

    print_result(result, args.output)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF转文本工具
使用pypdf库提取PDF文件内容并保存为TXT文件
"""

import os
import sys
import re
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    从PDF文件中提取文本内容
    
    Args:
        pdf_path (str): PDF文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        # 遍历所有页面
        for page_num, page in enumerate(reader.pages, 1):
            try:
                page_text = page.extract_text()
                if page_text.strip():  # 只有当页面有文本内容时才添加
                    text += page_text
                    text += "\n"
            except Exception as e:
                print(f"警告: 提取第 {page_num} 页时出错: {e}")
                continue
                
        return text.strip()
    
    except Exception as e:
        print(f"错误: 无法读取PDF文件 {pdf_path}: {e}")
        return None


def clean_text(text):
    """
    清理文本内容
    1. 删除页码标记（如 "— 9 —", "— 10 —"）
    2. 删除所有换行符，将文本合并为一行
    3. 清理多余的空格
    4. 在"第x章"、"第x条"前添加换行符
    5. 删除所有空格
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return text
    
    # 1. 删除页码标记（匹配类似 "— 数字 —" 的模式）
    # 支持各种破折号和数字格式
    page_number_patterns = [
        r'[—–-]\s*\d+\s*[—–-]',  # — 9 —, – 10 –, - 11 -
        r'[—–-]\s*\d+\s*[—–-]\s*\n?',  # 包含可能的换行
        r'\n\s*[—–-]\s*\d+\s*[—–-]\s*\n?',  # 前后可能有换行的页码
    ]
    
    for pattern in page_number_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    
    # 2. 删除所有换行符，将文本合并为一行
    text = re.sub(r'\n+', ' ', text)
    
    # 3. 清理多余的空格
    text = re.sub(r'\s+', ' ', text)
    
    # 4. 在"第x章"、"第x条"前添加换行符
    # 汉字数字映射
    chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', 
                      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                      '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', '二十七', '二十八', '二十九', '三十',
                      '三十一', '三十二', '三十三', '三十四', '三十五', '三十六', '三十七', '三十八', '三十九', '四十',
                      '零', '〇']
    
    # 构建匹配"第x章"、"第x条"的正则表达式
    # 支持多位数汉字数字组合
    chapter_pattern = r'第[一二三四五六七八九十零〇]+章'
    article_pattern = r'第[一二三四五六七八九十零〇]+条'
    
    # 在这些模式前添加换行符（如果前面不是换行符的话）
    text = re.sub(r'(?<!^)(?<!\n)(' + chapter_pattern + ')', r'\n\1', text)
    text = re.sub(r'(?<!^)(?<!\n)(' + article_pattern + ')', r'\n\1', text)
    
    # 5. 删除所有空格
    text = text.replace(' ', '')

    # 清理开头的空白字符
    text = text.strip()
    
    return text


def process_pdf_folder(folder_path, output_folder=None):
    """
    处理文件夹中的所有PDF文件
    
    Args:
        folder_path (str): 包含PDF文件的文件夹路径
        output_folder (str): 输出文件夹路径，如果为None则在原文件夹中创建txt文件
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"错误: 文件夹 {folder_path} 不存在")
        return
    
    if not folder_path.is_dir():
        print(f"错误: {folder_path} 不是一个文件夹")
        return
    
    # 设置输出文件夹
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = folder_path
    
    # 查找所有PDF文件
    pdf_files = list(folder_path.glob("*.pdf"))
    pdf_files.extend(list(folder_path.glob("*.PDF")))  # 包含大写扩展名
    
    if not pdf_files:
        print(f"在文件夹 {folder_path} 中没有找到PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    
    successful_count = 0
    failed_count = 0
    
    for pdf_file in pdf_files:
        print(f"\n正在处理: {pdf_file.name}")
        
        # 提取文本
        text = extract_text_from_pdf(pdf_file)
        
        if text is None:
            failed_count += 1
            continue
        
        if not text:
            print(f"警告: PDF文件 {pdf_file.name} 中没有可提取的文本内容")
            failed_count += 1
            continue
        
        # 清理文本内容
        cleaned_text = clean_text(text)
        
        # 生成输出文件名
        txt_filename = pdf_file.stem + ".txt"
        txt_path = output_path / txt_filename
        
        try:
            # 保存文本文件
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"文件名: {pdf_file.name}\n\n")
                f.write(cleaned_text)
            
            print(f"成功: 已保存到 {txt_path}")
            successful_count += 1
            
        except Exception as e:
            print(f"错误: 无法保存文件 {txt_path}: {e}")
            failed_count += 1
    
    print(f"\n处理完成!")
    print(f"成功处理: {successful_count} 个文件")
    print(f"处理失败: {failed_count} 个文件")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python pdf_to_text.py <PDF文件夹路径> [输出文件夹路径]")
        print("示例: python pdf_to_text.py ./pdfs")
        print("示例: python pdf_to_text.py ./pdfs ./output")
        return
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("PDF转文本工具")
    print("=" * 40)
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder if output_folder else '与输入文件夹相同'}")
    print("=" * 40)
    
    process_pdf_folder(input_folder, output_folder)


if __name__ == "__main__":
    main()

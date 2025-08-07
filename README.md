# PDF to Text Converter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

一个简单而强大的命令行工具，用于从PDF文件中提取文本内容，并进行智能清理，最终保存为`.txt`文件。

## ✨ 功能特性

- **批量处理**: 一次性转换指定文件夹内的所有PDF文件。
- **智能文本清理**:
  - 自动删除页码标记 (例如, `— 9 —`)。
  - 移除多余的换行和空格，使文本更整洁。
  - 在章节和条款标题（如“第一章”、“第二条”）前自动添加换行，保持段落结构。
  - 清除所有空格，使文本内容紧凑。
- **灵活的输出路径**: 您可以将转换后的文本文件保存在原始文件夹或指定一个新的输出文件夹。
- **支持不区分大小写的`.pdf`扩展名**: 同时识别 `.pdf` 和 `.PDF` 文件。

## ⚙️ 安装指南

1. **克隆或下载项目**

    ```bash
    git clone https://github.com/your-username/pdf-to-text.git
    cd pdf-to-text
    ```

2. **安装依赖**

    本项目使用 [pypdf](https://pypi.org/project/pypdf/) 库来处理PDF文件。

    **使用 uv 管理依赖 (推荐)**

    ```bash
    # 创建并激活虚拟环境
    uv venv
    
    # 在 Windows PowerShell 中激活虚拟环境
    .venv\Scripts\Activate.ps1
    
    # 安装项目依赖
    uv pip install -r requirements.txt
    ```

    **或者使用传统的 pip 方式**

    ```bash
    # 安装依赖
    pip install pypdf>=4.0.0
    
    # 或者使用 requirements.txt
    pip install -r requirements.txt
    ```

## 🚀 使用方法

通过命令行运行 `pdf_to_text.py` 脚本，并提供输入文件夹路径。

**基本语法:**

```bash
python pdf_to_text.py <输入文件夹路径> [可选的输出文件夹路径]
```

- `<输入文件夹路径>`: (必需) 包含您想要转换的PDF文件的文件夹。
- `[可选的输出文件夹路径]`: (可选) 如果提供，转换后的 `.txt` 文件将保存在此文件夹中。如果未提供，`.txt` 文件将保存在输入文件夹内。

## 📝 示例

假设您的PDF文件都存放在一个名为 `my_pdfs` 的文件夹中。

**1. 将文本文件保存在原始文件夹中:**

```bash
python pdf_to_text.py ./my_pdfs
```

处理完成后，您会在 `my_pdfs` 文件夹中找到与每个PDF对应的 `.txt` 文件。

**2. 将文本文件保存在指定的输出文件夹 `output_texts` 中:**

```bash
python pdf_to_text.py ./my_pdfs ./output_texts
```

如果 `output_texts` 文件夹不存在，程序会自动创建它。

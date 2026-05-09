import os
import re
from collections import defaultdict
from datetime import datetime
from urllib.parse import quote

# 题目所在的根目录，可以根据实际情况修改
SOLUTIONS_ROOT = "."  # 当前仓库根目录，子文件夹遍历
README_PATH = "README.md"
EXCLUDE_DIRS = {".git", ".github", "__pycache__", ".vscode", "node_modules"}

def extract_metadata(md_path):
    """从 md 文件头部提取题号、标题、链接、日期、分类"""
    meta = {}
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.readlines()
    except:
        return None

    # 提取标题行：# 📝 LeetCode [题号]：[题目名称]
    title_pattern = re.compile(r"^#\s*📝\s*LeetCode\s*(\d+)\s*[:：]\s*(.*)")
    for line in content[:15]:
        line = line.strip()
        if not meta.get("id"):
            m = title_pattern.match(line)
            if m:
                meta["id"] = int(m.group(1))
                meta["title"] = m.group(2).strip()
        # 匹配 - **题目链接**: ...
        link_pat = re.match(r"-\s*\*\*题目链接\*\*\s*[:：]\s*(.*)", line)
        if link_pat and "link" not in meta:
            meta["link"] = link_pat.group(1).strip()
        # 匹配日期
        date_pat = re.match(r"-\s*\*\*刷题日期\*\*\s*[:：]\s*(.*)", line)
        if date_pat and "date" not in meta:
            meta["date"] = date_pat.group(1).strip()
        # 匹配模块分类
        mod_pat = re.match(r"-\s*\*\*模块分类\*\*\s*[:：]\s*(.*)", line)
        if mod_pat and "module" not in meta:
            meta["module"] = mod_pat.group(1).strip()

    # 如果没有提取到标题，尝试用文件名作为题目后备
    if "title" not in meta:
        filename = os.path.splitext(os.path.basename(md_path))[0]
        meta["id"] = 9999  # 占位
        meta["title"] = filename
        meta.setdefault("link", "")
        meta.setdefault("date", "未知")
        meta.setdefault("module", "未分类")

    return meta

IGNORE_FILES = {"📝 LeetCode [题号]：[题目名称].md", "模板.md"} #可忽略文档的地方

def find_all_md():
    """遍历目录，收集所有 md 文件（排除特殊目录）"""
    records = []
    for root, dirs, files in os.walk(SOLUTIONS_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for file in files:
            # 跳过忽略列表中的文件
            if file.lower() in IGNORE_FILES:
                continue
            if file.endswith(".md") and file.lower() != "readme.md":
                full_path = os.path.join(root, file)
                meta = extract_metadata(full_path)
                if meta is None:
                    continue
                # 计算相对于仓库根目录的路径，用于链接
                rel_path = os.path.relpath(full_path, SOLUTIONS_ROOT)
                # 对路径中的空格等字符进行转义，保证链接正确
                encoded_rel_path = quote(rel_path)
                meta["rel_path"] = encoded_rel_path
                records.append(meta)
    return records

def generate_readme(records):
    lines = []
    lines.append("# LeetCode 刷题记录")
    lines.append(f"> 🕒 自动更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # 统计
    solved = len(records)
    categories = set(r.get("module", "未分类") for r in records)
    lines.append("## 📊 统计")
    lines.append(f"- 已解决题目：**{solved}** 道")
    lines.append(f"- 分类数量：**{len(categories)}** 个")
    lines.append("")

    # 按模块分类分组，再按题号排序
    grouped = defaultdict(list)
    for r in records:
        grouped[r.get("module", "未分类")].append(r)

    # 模块排序（可选：按模块名字）
    sorted_modules = sorted(grouped.items(), key=lambda x: x[0])

    lines.append("## 📋 题目列表")
    lines.append("")

    for module, items in sorted_modules:
        # 模块标题
        lines.append(f"### {module}")
        lines.append("| 题号 | 题目名称 | 题目链接 | 题解 | 刷题日期 |")
        lines.append("|------|----------|----------|------|----------|")
        # 组内按题号排序
        items.sort(key=lambda x: x.get("id", 9999))
        for item in items:
            tid = item.get("id", "")
            title = item.get("title", "未知")
            link_url = item.get("link", "")
            if link_url:
                link_cell = f"[LeetCode]({link_url})"
            else:
                link_cell = "-"
            sol_cell = f"[📄 代码]({item['rel_path']})"
            date = item.get("date", "未知")
            lines.append(f"| {tid} | {title} | {link_cell} | {sol_cell} | {date} |")
        lines.append("")

    # 底部说明
    lines.append("---")
    lines.append("💡 本文件由 GitHub Actions 自动生成，请勿手动编辑。")
    return "\n".join(lines)

def main():
    records = find_all_md()
    readme_content = generate_readme(records)
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ README 已更新，包含 {len(records)} 道题目。")

if __name__ == "__main__":
    main()
import os
import re
from openai import OpenAI
from typing import Dict, Any

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class CodeFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.code = self._read_file()

    def _read_file(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def analyze_with_openai(self) -> Dict[str, str]:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"请分析以下代码并提供其文件构成和代码逻辑：\n\n{self.code}\n\n",
                }
            ],
            max_tokens=4000,
            temperature=0.5,
        )

        # 获取生成的消息内容
        message_content = response.choices[0].message.content

        return {
            "structure": self._extract_structure(message_content),
            "logic": self._extract_logic(message_content)
        }

    def _extract_structure(self, analysis: str) -> str:
        parts = analysis.split('代码逻辑:')
        return parts[0].strip() if len(parts) > 1 else analysis

    def _extract_logic(self, analysis: str) -> str:
        parts = analysis.split('代码逻辑:')
        return parts[1].strip() if len(parts) > 1 else "未能提取代码逻辑"


def analyze_project(directory: str) -> Dict[str, Dict[str, str]]:
    project_analysis = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                code_file = CodeFile(file_path)
                analysis = code_file.analyze_with_openai()
                project_analysis[file_path] = analysis
                return project_analysis  # 找到第一个文件并分析后立即返回
            except Exception as e:
                print(f"Error analyzing file: {e}")
                return {"error": f"Error analyzing file: {e}"}
    return project_analysis


def generate_output_filename(base_name: str, extension: str) -> str:
    if not os.path.exists(base_name + extension):
        return base_name + extension

    match = re.search(r'_(\d+)$', base_name)
    if match:
        base_name, num = base_name[:match.start()], int(match.group(1))
        num += 1
    else:
        num = 1

    while True:
        new_name = f"{base_name}_{num}{extension}"
        if not os.path.exists(new_name):
            return new_name
        num += 1


def write_analysis_to_md(analysis_result: Dict[str, Dict[str, str]], output_file: str):
    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# 项目分析报告\n\n")
        for file_path, analysis in analysis_result.items():
            md_file.write(f"## 文件: {file_path}\n\n")
            if "error" in analysis:
                md_file.write(f"**错误**: {analysis['error']}\n\n")
            else:
                md_file.write(f"### 文件结构\n\n{analysis['structure']}\n\n")
                md_file.write(f"### 代码逻辑\n\n{analysis['logic']}\n\n")
            md_file.write("\n---\n\n")


def main():
    project_dir = input("请输入文件路径: ").strip()

    if not os.path.exists(project_dir):
        print("输入的文件路径不存在，请检查后重试。")
        return

    analysis_result = analyze_project(project_dir)

    if "error" in analysis_result:
        print(f"测试失败: {analysis_result['error']}")
        return

    base_name = os.path.basename(project_dir.rstrip('/')) + "分析结果"
    output_file = generate_output_filename(base_name, ".md")

    write_analysis_to_md(analysis_result, output_file)
    print(f"测试成功，分析结果已输出到 {output_file}")


if __name__ == '__main__':
    main()


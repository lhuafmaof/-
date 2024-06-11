import os
import re
import shutil
import logging
from openai import OpenAI
from typing import Dict, Any
from git import Repo

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class CodeFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.code = self._read_file()

    def _read_file(self) -> str:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading file {self.file_path}: {e}")
            raise

    def analyze_with_openai(self) -> Dict[str, str]:
        try:
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
            message_content = response.choices[0].message.content.strip()

            return {
                "structure": self._extract_structure(message_content),
                "logic": self._extract_logic(message_content)
            }
        except Exception as e:
            logging.error(f"Error analyzing code with OpenAI: {e}")
            raise

    def _extract_structure(self, analysis: str) -> str:
        parts = analysis.split('代码逻辑:')
        return parts[0].strip() if len(parts) > 1 else analysis

    def _extract_logic(self, analysis: str) -> str:
        parts = analysis.split('代码逻辑:')
        return parts[1].strip() if len(parts) > 1 else "未能提取代码逻辑"

def clone_github_repo(github_url: str, clone_dir: str) -> str:
    try:
        repo_name = github_url.split('/')[-1].replace('.git', '')
        clone_path = os.path.join(clone_dir, repo_name)
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)
        Repo.clone_from(github_url, clone_path)
        return clone_path
    except Exception as e:
        logging.error(f"Error cloning GitHub repository: {e}")
        raise

def analyze_project(directory: str) -> Dict[str, Dict[str, str]]:
    project_analysis = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith(('.py', '.java', '.js', '.cpp', '.c', '.cs')):
                continue  # 过滤非代码文件
            try:
                code_file = CodeFile(file_path)
                analysis = code_file.analyze_with_openai()
                project_analysis[file_path] = analysis
                return project_analysis  # 找到第一个文件并分析后立即返回
            except Exception as e:
                logging.error(f"Error analyzing file {file_path}: {e}")
                return {"error": f"Error analyzing file: {e}"}
    return project_analysis

def analyze_entire_project(directory: str) -> Dict[str, Dict[str, str]]:
    project_analysis = {}
    overall_analysis = {
        "languages": set(),
        "dependencies": set(),
        "custom_constructs": set(),
        "file_overview": {}
    }

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith(('.py', '.java', '.js', '.cpp', '.c', '.cs')):
                continue  # 过滤非代码文件
            try:
                code_file = CodeFile(file_path)
                analysis = code_file.analyze_with_openai()
                project_analysis[file_path] = analysis

                # Collect overall analysis data
                language = file.split('.')[-1]
                overall_analysis["languages"].add(language)
                # Here you would add logic to analyze dependencies, custom constructs, etc.
                # For example, you might parse the analysis result and extract relevant information

                overall_analysis["file_overview"][file_path] = {
                    "structure": analysis["structure"],
                    "logic": analysis["logic"]
                }
            except Exception as e:
                logging.error(f"Error analyzing file {file_path}: {e}")
                project_analysis[file_path] = {"error": f"Error analyzing file: {e}"}

    return project_analysis, overall_analysis


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

def write_analysis_to_md(analysis_result: Dict[str, Dict[str, str]], output_file: str, is_overall: bool = False) -> str:
    with open(output_file, 'w', encoding='utf-8') as md_file:
        if is_overall:
            md_file.write("# 项目整体分析报告\n\n")
            md_file.write("## 开发语言\n\n")
            md_file.write(", ".join(analysis_result["languages"]) + "\n\n")
            md_file.write("## 依赖关系\n\n")
            md_file.write(", ".join(analysis_result["dependencies"]) + "\n\n")
            md_file.write("## 自行构造\n\n")
            md_file.write(", ".join(analysis_result["custom_constructs"]) + "\n\n")
            md_file.write("## 文件概览\n\n")
            for file_path, overview in analysis_result["file_overview"].items():
                md_file.write(f"### 文件: {file_path}\n\n")
                md_file.write(f"**结构**: {overview['structure']}\n\n")
                md_file.write(f"**逻辑**: {overview['logic']}\n\n")
                md_file.write("\n---\n\n")
        else:
            md_file.write("# 具体分析报告\n\n")
            for file_path, analysis in analysis_result.items():
                md_file.write(f"## 文件: {file_path}\n\n")
                if "error" in analysis:
                    md_file.write(f"**错误**: {analysis['error']}\n\n")
                else:
                    md_file.write(f"### 文件结构\n\n{analysis['structure']}\n\n")
                    md_file.write(f"### 代码逻辑\n\n{analysis['logic']}\n\n")
                md_file.write("\n---\n\n")
    return os.path.abspath(output_file)


def create_output_folders(output_dir: str, project_dir: str) -> str:
    project_name = os.path.basename(project_dir.rstrip('/'))
    output_base_dir = os.path.join(output_dir, project_name + "分析文件")
    os.makedirs(output_base_dir, exist_ok=True)

    for root, dirs, files in os.walk(project_dir):
        for dir in dirs:
            relative_path = os.path.relpath(os.path.join(root, dir), project_dir)
            os.makedirs(os.path.join(output_base_dir, relative_path + "分析文件"), exist_ok=True)

    return output_base_dir


def main():
    # 交互式输入
    path = input("请粘贴本地项目路径或GitHub项目URL: ").strip()
    output_dir = input("请输入输出目录（默认为当前目录）: ").strip() or os.getcwd()

    if os.path.exists(path):
        project_dir = path
        print("项目读取成功")
    elif path.startswith("https://github.com/"):
        try:
            project_dir = clone_github_repo(path, output_dir)
            print("项目读取成功")
        except Exception as e:
            print("项目读取失败，请检查本地文件路径或项目URL后重试。")
            return
    else:
        print("无效的输入，请输入本地项目路径或GitHub项目URL。")
        return

    # 测试流程
    analysis_result, overall_analysis = analyze_entire_project(project_dir)

    if "error" in analysis_result:
        print(f"测试失败: {analysis_result['error']}")
        return

    base_name = os.path.basename(project_dir.rstrip('/')) + "分析测试文档"
    output_file = generate_output_filename(base_name, ".md")

    output_file_path = write_analysis_to_md(analysis_result, output_file)
    print(f"测试成功，分析结果已输出到 {output_file_path}")

    # 提示用户是否继续分析整个项目
    logging.getLogger().setLevel(logging.WARNING)  # 临时设置日志级别为 WARNING 以上
    continue_analysis = input("是否分析整个文件？请输入继续或取消: ").strip()
    logging.getLogger().setLevel(logging.INFO)  # 恢复日志级别为 INFO

    if continue_analysis.lower() == '继续':
        output_base_dir = create_output_folders(output_dir, project_dir)
        analysis_result, overall_analysis = analyze_entire_project(project_dir)
        for file_path, analysis in analysis_result.items():
            relative_path = os.path.relpath(file_path, project_dir)
            output_file = os.path.join(output_base_dir, relative_path + "分析文件.md")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            output_file_path = write_analysis_to_md({file_path: analysis}, output_file)
            print(f"分析结果已输出到 {output_file_path}")

        # Write overall analysis
        overall_output_file = os.path.join(output_base_dir, "整体分析.md")
        overall_output_file_path = write_analysis_to_md(overall_analysis, overall_output_file, is_overall=True)
        print(f"整体分析结果已输出到 {overall_output_file_path}")

        print(f"分析成功，分析结果已输出到 {output_base_dir}") #增加文件路径
    else:
        print("流程已中断。")


if __name__ == '__main__':
    main()

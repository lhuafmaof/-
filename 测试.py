import openai
import sys


def check_openai_version():
    try:
        # 获取 OpenAI 库的版本
        import openai
        version = openai.__version__
        print(f"OpenAI library version: {version}")
    except ImportError:
        print("OpenAI 没有安装.")
        sys.exit(1)


def check_openai_api_key():
    try:
        # 检查是否配置了 API 密钥
        if not openai.api_key:
            print("OpenAI API key 没有配置.")
            sys.exit(1)

        # 测试 API 密钥是否有效
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
        print("OpenAI API 调用成功.")
        print("Sample response:", response.choices[0].text.strip())
    except openai.error.AuthenticationError:
        print("OpenAI API 调用失败，请检查配置.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check_openai_version()
    check_openai_api_key()

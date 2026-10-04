# 阿里云 DashScope API Key 配置

项目已经配置为优先使用阿里云 DashScope 的 Anthropic 兼容接口。

## 你需要填写的位置

打开项目根目录下的 `.env`：

```text
F:\codex\projects\agentic-rag-assistant\.env
```

把第一行改成：

```env
DASHSCOPE_API_KEY=你的阿里云百炼APIKey
```

当前模型已经配置为：

```env
DASHSCOPE_MODEL=qwen3.7-plus
```

当前 Anthropic 兼容地址：

```env
DASHSCOPE_ANTHROPIC_BASE_URL=https://dashscope.aliyuncs.com/apps/anthropic
```

## 配置后运行

```bash
cd F:\codex\projects\agentic-rag-assistant
python -m src.ingest
python -m src.web_app
```

然后打开：

```text
http://127.0.0.1:8000
```

## 说明

- 如果 `DASHSCOPE_API_KEY` 为空，系统会自动回落到本地演示模式。
- 如果填写了 `DASHSCOPE_API_KEY`，系统会调用 DashScope Anthropic-compatible Messages API。
- 不要把真实 API Key 提交到公开仓库。

#!/bin/bash

# RagForge 模型配置示例脚本
# 这个脚本展示了如何使用 ragforge CLI 来管理模型配置

echo "=== RagForge 模型配置示例 ==="
echo

# 1. 查看可用的模型工厂
echo "1. 查看可用的模型工厂:"
ragforge models factories
echo

# 2. 查看当前配置的模型
echo "2. 查看当前配置的模型:"
ragforge models list
echo

# 3. 添加 OpenAI 模型配置示例
echo "3. 添加 OpenAI 模型配置示例:"
echo "ragforge models add --factory OpenAI --name gpt-4 --type chat --api-key YOUR_API_KEY --base-url https://api.openai.com/v1"
echo

# 4. 添加 Ollama 模型配置示例
echo "4. 添加 Ollama 模型配置示例:"
echo "ragforge models add --factory Ollama --name llama2 --type chat --base-url http://localhost:11434"
echo

# 5. 添加 embedding 模型配置示例
echo "5. 添加 embedding 模型配置示例:"
echo "ragforge models add --factory OpenAI --name text-embedding-ada-002 --type embedding --api-key YOUR_API_KEY --base-url https://api.openai.com/v1"
echo

# 6. 编辑模型配置示例
echo "6. 编辑模型配置示例:"
echo "ragforge models edit --factory OpenAI --name gpt-4 --api-key NEW_API_KEY"
echo

# 7. 查看特定模型配置
echo "7. 查看特定模型配置:"
echo "ragforge models show --factory OpenAI --name gpt-4"
echo

# 8. 删除模型配置示例
echo "8. 删除模型配置示例:"
echo "ragforge models delete --factory OpenAI --name gpt-4"
echo

echo "=== 常用模型类型 ==="
echo "chat: 聊天模型，用于对话生成"
echo "embedding: 嵌入模型，用于文本向量化"
echo "rerank: 重排序模型，用于搜索结果重排序"
echo "image2text: 图像转文本模型，用于图像理解"
echo "speech2text: 语音转文本模型，用于语音识别"
echo "tts: 文本转语音模型，用于语音合成"
echo

echo "=== 常用模型工厂 ==="
echo "OpenAI: OpenAI API 兼容的模型"
echo "Ollama: 本地运行的 Ollama 模型"
echo "Xinference: 本地推理服务"
echo "HuggingFace: HuggingFace 模型"
echo "Azure-OpenAI: Azure OpenAI 服务"
echo "Google Cloud: Google Cloud AI 服务"
echo

echo "=== 注意事项 ==="
echo "1. API Key 会被安全存储，不会在日志中显示"
echo "2. 某些模型工厂可能需要特殊的认证方式"
echo "3. 本地模型（如 Ollama）通常不需要 API Key"
echo "4. 建议为不同的模型类型配置不同的模型"
echo 
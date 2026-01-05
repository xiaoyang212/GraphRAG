#!/bin/bash
# Example script to run multiple-choice question evaluation
# 运行选择题评估的示例脚本

echo "=========================================="
echo "Multiple-Choice Question Evaluation Example"
echo "选择题评估示例"
echo "=========================================="
echo ""

# Check if dataset exists
if [ ! -d "Data/MultipleChoiceExample" ]; then
    echo "❌ Error: Example dataset not found at Data/MultipleChoiceExample"
    echo "❌ 错误：未找到示例数据集 Data/MultipleChoiceExample"
    exit 1
fi

echo "✅ Example dataset found at Data/MultipleChoiceExample"
echo "✅ 找到示例数据集：Data/MultipleChoiceExample"
echo ""

# Rename dataset to include 'quality' for close-set evaluation
echo "Step 1: Setting up dataset for close-set evaluation mode"
echo "步骤 1：设置数据集以启用 close-set 评估模式"
echo ""

if [ -d "Data/quality_example" ]; then
    echo "✅ Dataset 'quality_example' already exists"
    echo "✅ 数据集 'quality_example' 已存在"
else
    echo "Creating symbolic link: Data/MultipleChoiceExample -> Data/quality_example"
    echo "创建符号链接：Data/MultipleChoiceExample -> Data/quality_example"
    ln -s MultipleChoiceExample Data/quality_example
    echo "✅ Created symbolic link"
    echo "✅ 已创建符号链接"
fi

echo ""
echo "Step 2: Running test to verify dataset format"
echo "步骤 2：运行测试以验证数据集格式"
echo ""

python tests/test_multiple_choice.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Dataset validation failed. Please check the error messages above."
    echo "❌ 数据集验证失败。请检查上述错误信息。"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Setup complete! You can now run evaluation:"
echo "✅ 设置完成！现在可以运行评估："
echo ""
echo "Standard mode / 标准模式:"
echo "  python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_example"
echo ""
echo "Per-corpus mode / Per-corpus 模式:"
echo "  python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_example"
echo ""
echo "Note: Make sure to configure your LLM settings in Option/Config2.yaml before running"
echo "注意：运行前请确保在 Option/Config2.yaml 中配置 LLM 设置"
echo "=========================================="

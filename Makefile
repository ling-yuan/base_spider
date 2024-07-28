# MIRROR = https://pypi.python.org/simple
MIRROR = https://pypi.tuna.tsinghua.edu.cn/simple


setup: venv install 

venv:
	@echo "创建虚拟环境..."
	virtualenv -p python3 .venv

install: install_packages upgrade format_code

install_packages:
	@echo "安装依赖..."
	.venv\Scripts\pip install -r requirements.txt -i ${MIRROR}

upgrade: upgrade_packages

upgrade_packages:
	@echo "升级依赖..."
	.venv\Scripts\python -m pip install --upgrade pip -i ${MIRROR}
	.venv\Scripts\pip install --upgrade -r requirements.txt -i ${MIRROR}

.PHONY: export_requirements
export_requirements:
	@echo "导出依赖..."
	.venv\Scripts\python -m pip freeze > requirements.txt

format_code: pre-commit
	@echo "格式化代码..."
	.venv\Scripts\pre-commit run --a
# .venv\Scripts\black main.py --line-length 120
# .venv\Scripts\black universal_spider --line-length 120

.PHONY: test
test:
	@echo "单元测试..."
	.venv\Scripts\pytest -q --tb=line -s

pre-commit:
	@echo "提交前检查..."
	.venv\Scripts\pre-commit install

# windows下有问题，待完善
# clean:
# 	@echo "清理虚拟环境..."
# 	rm -rf venv

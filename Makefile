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

upgrade: upgrade_packages export_requirements

upgrade_packages:
	@echo "升级依赖..."
	.venv\Scripts\python -m pip install --upgrade pip
	.venv\Scripts\pip install --upgrade -r requirements.txt

.PHONY: export_requirements
export_requirements:
	@echo "Exporting requirements..."
	.venv\Scripts\python -m pip freeze > requirements.txt

format_code:
	@echo "格式化代码..."
	.venv\Scripts\black main.py --line-length 120
	.venv\Scripts\black universal_spider --line-length 120

.PHONY: test
test:
	@echo "Running test coverage..."
	.venv\Scripts\pytest -v 

# windows下有问题，待完善
# clean:
# 	@echo "清理虚拟环境..."
# 	rm -rf venv

# MIRROR = https://pypi.python.org/simple
MIRROR = https://pypi.tuna.tsinghua.edu.cn/simple

# 设置venv路径
ifeq ($(OS),Windows_NT)
	VENV_PATH = .venv/Scripts
else
	VENV_PATH = .venv/bin
endif

setup: venv install 

venv:
	@echo "创建虚拟环境..."
	pip3 install virtualenv -i ${MIRROR}
	virtualenv -p python3 .venv

install: install_packages upgrade

install_packages:
	@echo "安装依赖..."
	${VENV_PATH}/pip install -r requirements.txt -i ${MIRROR}

upgrade: upgrade_packages

upgrade_packages:
	@echo "升级依赖..."
	${VENV_PATH}/python -m pip install --upgrade pip -i ${MIRROR}
	${VENV_PATH}/pip install --upgrade -r requirements.txt -i ${MIRROR}

.PHONY: export_requirements
export_requirements:
	@echo "导出依赖..."
	${VENV_PATH}/python -m pip freeze > requirements.txt

format_code: pre-commit
	@echo "格式化代码..."
	${VENV_PATH}/pipp install pre-commit -i ${MIRROR}
	${VENV_PATH}/pre-commit run --a
# ${VENV_PATH}/black main.py --line-length 120
# .${VENV_PATH}/black universal_spider --line-length 120

.PHONY: test
test:
	@echo "单元测试..."
	${VENV_PATH}/pytest -q --tb=line -s -vv

pre-commit:
	@echo "提交前检查..."
	${VENV_PATH}/pre-commit install

# windows下有问题，待完善
# clean:
# 	@echo "清理虚拟环境..."
# 	rm -rf venv

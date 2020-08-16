install_and_run:
		@echo "Install requirements..."
		pip install -r requirements.txt
		@echo "Wrapper run..."
		python3 urutu.py

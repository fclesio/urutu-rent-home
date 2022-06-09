install_and_run:
		@echo "Install requirements..."
		pip3 install -r requirements.txt
		@echo "Wrapper run..."
		python3 urutu.py

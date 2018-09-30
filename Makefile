main:
	python run.py
clnt:
	python client.py
t:
	/usr/bin/openssl s_client -proxy localhost:8080 -connect www.google.com -CAfile /home/yury/dev/pitonizm/habroproxy/cert/server.pem

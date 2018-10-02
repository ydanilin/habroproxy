main:
	python run.py
clnt:
	python client.py
gencert:
	python gencert.py
test:
	pytest
t:
	/usr/bin/openssl s_client -proxy localhost:8080 -connect www.google.com -CAfile /home/yury/dev/pitonizm/habroproxy/cert/server.pem
tw:
	C:\tp\OpenSSL-Win64\bin\openssl s_client -proxy localhost:8080 -connect www.google.com -CAfile C:\tp\docs\G\Pitonizm\habroproxy\cert\habroproxy-ca-cert.pem

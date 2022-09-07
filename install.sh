sudo apt update
sudo apt -y upgrade

echo "Instalando Docker"
curl -fsSL https://get.docker.com/ | bash

echo "Instalando docker-compose"
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Adicionando usuário atual no grupo Docker."
sudo gpasswd -a $USER docker
sudo setfacl -m user:$USER:rw /var/run/docker.sock

echo "Running Portainer on port 9000..."
docker run -d \
-p 9000:9000 \
--restart always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /opt/portainer:/data \
portainer/portainer


cd app
cp ../.env .
docker-compose -f docker-compose.yml up --build -d

echo "Fazendo a migração do banco"
docker container exec app_app_1 python manage.py migrate

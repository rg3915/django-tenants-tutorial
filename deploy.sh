# Colors
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`


cd app
git pull
cp ../.env .

# Parando todos os containers
echo "${green}>>> Stop all containers...${reset}"
docker stop $(docker ps -aq)

# Deletando todos os containers
# echo "${green}>>> Delete all containers...${reset}"
# docker rm $(docker ps -aq)

# Limpando containers parados
echo "${green}>>> Clear containers stopped...${reset}"
docker system prune -f
# docker volume prune -f
docker images -q --filter "dangling=true" | xargs -r docker rmi

# Subindo os containers novamente
echo "${green}>>> Up containers again...${reset}"
docker-compose up --build -d

echo "${green}>>> Make migrations...${reset}"
docker container exec app_app_1 python manage.py migrate

echo "${green}>>> Running collectstatic...${reset}"
docker container exec app_app_1 python manage.py collectstatic

echo "${green}>>> Done!${reset}"

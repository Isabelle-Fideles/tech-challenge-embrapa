# Variável
COMPOSE=docker-compose.yml

# ---------------------------
# Comandos principais
# ---------------------------
up:
	docker compose -f $(COMPOSE) up --build

up-detach:
	docker compose -f $(COMPOSE) up --build -d

down:
	docker compose -f $(COMPOSE) down

logs:
	docker compose -f $(COMPOSE) logs -f

# ---------------------------
# Limpeza
# ---------------------------
clean:
	docker system prune -af --volumes

clean-images:
	docker image prune -af

clean-volumes:
	docker volume prune -f

# ---------------------------
# Build manual (se quiser)
# ---------------------------
build:
	docker build -t embrapa-api .

# ---------------------------
# Status
# ---------------------------
ps:
	docker ps

# ---------------------------
# Ajuda
# ---------------------------
help:
	@echo ""
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "  make up               -> Sobe o ambiente (foreground)"
	@echo "  make up-detach        -> Sobe o ambiente (detached)"
	@echo "  make down             -> Derruba o ambiente"
	@echo "  make logs             -> Logs do ambiente"
	@echo "  make migrate          -> Roda as migrações"
	@echo ""
	@echo "Limpeza:"
	@echo "  make clean            -> Remove containers, imagens e volumes"
	@echo "  make clean-images     -> Remove imagens não usadas"
	@echo "  make clean-volumes    -> Remove volumes não usados"
	@echo ""
	@echo "Outros:"
	@echo "  make build            -> Build manual da imagem"
	@echo "  make ps               -> Lista containers em execução"
	@echo "  make help             -> Mostra esta ajuda"
	@echo ""

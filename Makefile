.PHONY: help install dev clean clean-all

help: ## Show this help message
	@echo "elitea.ai — Landing Page"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install landing page dependencies
	@cd web && npm ci

dev: ## Start landing page dev server (port 3000)
	@./scripts/dev-landing.sh

clean: ## Clean build outputs and caches
	@echo "🧹 Cleaning build outputs..."
	@rm -rf web/out/
	@rm -rf web/.next/
	@rm -rf _local_preview/
	@echo "✅ Clean complete"

clean-all: clean ## Clean everything including node_modules
	@echo "🧹 Cleaning dependencies..."
	@rm -rf web/node_modules/
	@echo "✅ Full clean complete"

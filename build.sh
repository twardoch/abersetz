#!/usr/bin/env bash
cd "$(dirname "$0")"
fd -e py -x autoflake {}; 
fd -e py -x pyupgrade --py311-plus {}; 
fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; 
fd -e py -x ruff format --respect-gitignore --target-version py311 {};
uvx hatch fmt;
llms .;
uvx hatch clean; 
gitnextver .; 
uvx hatch build;

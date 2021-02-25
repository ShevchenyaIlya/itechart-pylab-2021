# Document collaboration system

## Installation guide

### Frontend
    Creating project with basic packages:
    npx create-react-app application_name
    
    Additional package installations:
    1) npm install --save react-router-dom
    2) npm install @material-ui/core
    3) npm install --save react-draft-wysiwyg draft-js
    
    Description:
    1 - for routing
    2 - for interface
    3 - for editor
    
### Backend
    Flask
    
    For user authorization using "flask_jwt_extended" module
    Database - MongoDB. Using pymongo module.
    
### Config pre-commit
    .pre-commit-config.yaml consist of configurations for "mypy", "isort", "black", "flack8"
    
    Install hooks:
    pre-commit install
    
### ESLint
Configurations for eslint placed in package.json
Errors and warnings appear in code editor, because extension for ESLint enabled in PyCharme
    
    To run eslint from command line use:
    eslint [options] file
    
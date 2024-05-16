# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.1.0](https://github.com/Deeplearn-PeD/reg/releases/tag/0.1.0) - 2024-05-16

<small>[Compare with first commit](https://github.com/Deeplearn-PeD/reg/compare/4f522aa2378f284153f214afe96cd36bb6d22a4d...0.1.0)</small>

### Bug Fixes

- Adjust model import and response generation in LLLModel ([196206a](https://github.com/Deeplearn-PeD/reg/commit/196206a72e7edbea5a42ff617f948373edd8fb62) by Flávio Codeço Coelho).

### Features

- Add the ability to generate SQL code with semantic names for columns ([e475d8b](https://github.com/Deeplearn-PeD/reg/commit/e475d8be5fcfd8b46be1d825fbdac2506496f98c) by Flávio Codeço Coelho).
- Add method to prepare database for querying ([bf963a5](https://github.com/Deeplearn-PeD/reg/commit/bf963a5556072c49bdf9001d7e6766158a258e84) by Flávio Codeço Coelho).
- Add support for retrieving views in the database ([76e984a](https://github.com/Deeplearn-PeD/reg/commit/76e984a3fe5dc824e1790b1c68f6cba4208f2ee8) by Flávio Codeço Coelho).
- Add method to create semantic view in Database class ([62591a4](https://github.com/Deeplearn-PeD/reg/commit/62591a4f46be499f9cbe34fd103b3299bcd75a34) by Flávio Codeço Coelho).
- Added functionality to retrieve list of tables in the database. ([464a625](https://github.com/Deeplearn-PeD/reg/commit/464a62526c8056e996dbf80c4288a20605846450) by Flávio Codeço Coelho).
- Add method to create semantic view in dbtools ([08ecebe](https://github.com/Deeplearn-PeD/reg/commit/08ecebec11df9483f80af91412c29508acb96e7a) by Flávio Codeço Coelho).
- Update README.md with new bot name and image ([c7c8447](https://github.com/Deeplearn-PeD/reg/commit/c7c8447e0fd6216f1539d9f4260e5aa9a8e62ae9) by Flávio Codeço Coelho).
- Add language parameter to PromptTemplate instantiation ([dc60a81](https://github.com/Deeplearn-PeD/reg/commit/dc60a819617acb69aa479119ac9ab8cb79dc53f8) by Flávio Codeço Coelho).
- Add ollama as dependency and implement csv connection in dbtools ([9241744](https://github.com/Deeplearn-PeD/reg/commit/92417445a6e9e51079cd463fea60d966da8f8189) by Flávio Codeço Coelho).
- Add token count logging in Reggie class ([febe386](https://github.com/Deeplearn-PeD/reg/commit/febe386469749193b663f1c0d3399da0baf12122) by Flávio Codeço Coelho).
- Add auto method to Reggie class ([cccc659](https://github.com/Deeplearn-PeD/reg/commit/cccc659bf6d2ed15156355de67ae4ae1e607ed96) by Flávio Codeço Coelho).
- Add .onnx and .onnx.json files to .gitignore ([3821cc0](https://github.com/Deeplearn-PeD/reg/commit/3821cc06f251ac8f8ac16df2b10aba458a2f4630) by Flávio Codeço Coelho).
- Add language-specific introductory and questioning prompts ([4337981](https://github.com/Deeplearn-PeD/reg/commit/4337981b2a7e610cb4c3d2ed7f8a24e25e96f559) by Flávio Codeço Coelho).
- Refactor DBTools to use Database class ([928619b](https://github.com/Deeplearn-PeD/reg/commit/928619b47f0281128c8cea3ac0a187d2848a1874) by Flávio Codeço Coelho).
- Refactor PromptTemplate class for SQL query generation ([d4e8135](https://github.com/Deeplearn-PeD/reg/commit/d4e81353e767ccacb318a14a1d9c660f91fb7ba6) by Flávio Codeço Coelho).

### Code Refactoring

- Added tables property to Database class ([e81a220](https://github.com/Deeplearn-PeD/reg/commit/e81a220da40011e4468eaadcac07db9fec1913ce) by Flávio Codeço Coelho).
- Update cli script to use cli module instead of main module for Reggie class ([b9e7214](https://github.com/Deeplearn-PeD/reg/commit/b9e7214d456dcd5a29a00be1806f44d8471f1418) by Flávio Codeço Coelho).
- Update LLLModel with Ollama Client and modify response generation ([6f284fb](https://github.com/Deeplearn-PeD/reg/commit/6f284fba4cc2d40f8bd1f751d96b8a0db07531da) by Flávio Codeço Coelho).
- Modify Reggie class __init__ method to accept model parameter ([ce7d022](https://github.com/Deeplearn-PeD/reg/commit/ce7d022841858fd62c81bb6c611f23340ccf1c02) by Flávio Codeço Coelho).
- Update Database class in dbtools.py ([f533e10](https://github.com/Deeplearn-PeD/reg/commit/f533e107d72a5b5879d6e0147178d58a86f5f553) by Flávio Codeço Coelho).

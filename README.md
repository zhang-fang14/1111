# Jenkins + Git 自动化构建实验

## 项目简介

本项目演示了如何使用 Jenkins 和 Git 实现持续集成（CI）流程。  
通过 Jenkins 定时或触发器自动拉取 Git 仓库代码，执行构建任务，完成自动化测试和部署。

---

## 环境准备

- 操作系统：Windows 10  
- Jenkins 版本：2.x  
- Git 版本：2.49.0 或以上  
- Java 版本：JDK 17  
- 其他工具：Git Bash、浏览器  

---

## 使用说明

### 1. 配置 Jenkins Job

- 新建一个自由风格的软件项目（Freestyle Project）  
- 在“源码管理”中配置 Git 仓库地址  
- 配置构建触发器（如轮询 SCM 或 Webhook）  
- 配置构建步骤（例如执行构建脚本或命令）  

### 2. 代码提交

- 本地修改代码后执行 `git add`、`git commit`、`git push`  
- Jenkins 会自动检测代码变更，触发构建任务  

### 3. 构建结果查看

- 登录 Jenkins，进入对应 Job 页面  
- 查看构建历史和控制台日志  
- 查看测试报告和构建产物（如有）  

---

## 常用命令

```bash
git clone <仓库地址>
git add .
git commit -m "描述信息"
git push origin main

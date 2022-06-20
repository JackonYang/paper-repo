# Paper Repo - Workflow Design

## 设计目的

### 直接目的

建立一个自己的 pdf paper repo，解决 pdf (二进制)文件的存储需求。

主要的需求：

1. 在 git repo 里可以方便的 link、查阅。
2. 支持二次开发，方便的与其他开发者友好的工具对接。
3. 可以多处备份，防丢失。
4. 可以付费，但要便宜。对标自己买硬盘的价格。
5. 新增 pdf 文件，修改 meta data 方便。对 pdf 文件本身的修改，要求不高。

### 上下游对接

TODO

## WorkFlow 概述

基本流程：

1. 原始输入 pdf
2. 根据 PDF 初始化 meta data 文件
3. 根据 meta data 文件，生成用户可直接查阅的页面。比如 file list。

补充说明：

1. meta data 的部分字段是自动获取的，比如 pdf 的页数，paper title 等。
2. meta data 文件可以人工修改。修改后，重新自动生成时，不能覆盖人工修改过的内容。
3. 自动生成 meta data 的代码会改。典型需求是：新增/废弃字段，改进字段的取值等。比如，自动生成 paper title 的算法提升精度。
4. 已有的 meta data 也可以作为训练数据，提高模型的准确性。

## plugins 功能

TODO：

1. 根据 url / id 从 arxiv 下载 pdf & bibtex （meta data）
2. meta data 支持对 pdf 加 category & tag。如何更高效的管理、修改这些字段。

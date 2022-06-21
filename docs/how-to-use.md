# Paper Repo - How To Use

## 添加新书

手动把 pdf 文件拖入到 repo 的根目录。起个 unique & 易读的名字。最好就是 paper title、核心模型的名字缩写等。

执行如下命令：

```bash
# 新 pdf 由 dvc 管理
# 步骤包括: dvc add, gen meta, & check dup
# 如果发现重复的 pdf 文件，需要手动删除
make dvc-add

# review Readme.md 的改动 & git commit 后运行

# push to cloud
# 功能包括 flake8 check, dvc push, git push
make push-all

# 删除本地的 pvc & 对应的 pdf 文件
# https://dvc.org/doc/command-reference/remove
dvc remove *.dvc --outs
# 待验证。删 remove cloud 里的用不上的
# remote 存储不爆炸，就不要搞这个命令
# https://dvc.org/doc/command-reference/gc
dvc gc --workspace -c
```

## 开发

### 添加一个新的 pipeline

例如: `gen_md_notes`

1. 创建 code 文件：`pdf_pipeline/gen_md_notes.py`
2. 在 manage.py 中使用 code 文件
3. 在 Makefile 中添加快捷命令

example: <https://github.com/JackonYang/paper-repo/commit/39f8513bf3860d0f0e6ccaecbf3382006f9ead7f>

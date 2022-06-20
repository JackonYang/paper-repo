# Paper Repo - How To Use

## 添加新书

手动把 pdf 文件拖入到 repo 的根目录。起个 unique & 易读的名字。最好就是 paper title、核心模型的名字缩写等。

执行如下命令：

```bash
# 检查是否有重复的 pdf 文件，需要手动删除
make check-dup
# 删除本地的 pvc & 对应的 pdf 文件
# https://dvc.org/doc/command-reference/remove
dvc remove *.dvc --outs
# 待验证。删 remove cloud 里的用不上的
# https://dvc.org/doc/command-reference/gc
dvc gc --workspace -c

make dvc-add
# review Readme.md 的改动 & git commit
make push-all
```

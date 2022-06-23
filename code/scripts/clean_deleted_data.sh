SCRIPT_DIR=$(cd $(dirname "$0") && pwd)

PROJ_ROOT=$(realpath "$SCRIPT_DIR/../../")
paper_reading_root=$(realpath $PROJ_ROOT/../)

pushd $paper_reading_root >> /dev/null

# list deleted files
meta_keys=$(git status -s 01-zettelkasten/02-References | grep 'D' | awk '{print $2}' | awk -F'/' '{print $3}' | awk -F'.' '{print $1}')

popd >> /dev/null


pushd $PROJ_ROOT >> /dev/null

echo $meta_keys | xargs -I{} dvc remove pdf/{}.pdf.dvc --outs
echo $meta_keys | xargs -I{} rm metas/{}.yaml

popd >> /dev/null

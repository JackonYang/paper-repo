SCRIPT_DIR=$(cd $(dirname "$0") && pwd)

pushd $SCRIPT_DIR/../ > /dev/null

pip install -q -r requirements-dev.txt

popd > /dev/null

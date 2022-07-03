pushd ../.. > /dev/null

python3 -m paper_crawlers.semanticscholar_crawler.main

time python3 -m paper_crawlers.semanticscholar_crawler.build_ref_meta

popd > /dev/null

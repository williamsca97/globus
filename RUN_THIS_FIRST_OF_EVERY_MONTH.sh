mkdir tmp
./get_globus_data.py -c globus_config.json -o out -n
rm -rf tmp
./build_cache.py
python2 website_generate.py

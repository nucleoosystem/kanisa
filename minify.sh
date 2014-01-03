set -e

mkdir -p kanisa/static/kanisa/js/minified
mkdir -p kanisa/static/kanisa/css/minified
rm -f kanisa/static/kanisa/js/minified/*.js
rm -f kanisa/static/kanisa/css/minified/*.css

python setup.py minify_management_js
python setup.py minify_public_js
python setup.py minify_css

function shorthash()
{
    md5sum $1 | awk '{ print $1 }' | cut -c1-8
}

pushd kanisa/static/kanisa/

management_js_hash=`shorthash js/minified/kanisa-management.js`
public_js_hash=`shorthash js/minified/kanisa-public.js`
css_hash=`shorthash css/minified/kanisa.css`

mv js/minified/kanisa-management.js js/minified/kanisa-management.${management_js_hash}.js
mv js/minified/kanisa-public.js js/minified/kanisa-public.${public_js_hash}.js
mv css/minified/kanisa.css css/minified/kanisa.${css_hash}.css
popd

rm -f kanisa/static_conf.py
touch kanisa/static_conf.py

echo "KANISA_MANAGEMENT_JS_HASH = '${management_js_hash}'" >> kanisa/static_conf.py
echo "KANISA_PUBLIC_JS_HASH = '${public_js_hash}'" >> kanisa/static_conf.py
echo "KANISA_CSS_HASH = '${css_hash}'" >> kanisa/static_conf.py

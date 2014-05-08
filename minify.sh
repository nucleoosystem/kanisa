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

public_js_template="kanisa/templates/kanisa/public/_js.html"
rm -f ${public_js_template}
touch ${public_js_template}
echo "{% load static from staticfiles %}" >> ${public_js_template}
echo "{% if KANISA_DEBUG_STATIC %}" >> ${public_js_template}
for i in $(find kanisa/static/kanisa/js/public/ -type f | sort); do
    localpath=${i:14}
    echo "<script src=\"{% static '${localpath}' %}\"></script>" >> ${public_js_template}
done
echo "{% else %}" >> ${public_js_template}
echo "<script src=\"{% static }}kanisa/js/minified/kanisa-public.${public_js_hash}.js\"></script>" >> ${public_js_template}
echo "{% endif %}" >> ${public_js_template}

management_js_template="kanisa/templates/kanisa/management/_js.html"
rm -f ${management_js_template}
touch ${management_js_template}
echo "{% load static from staticfiles %}" >> ${management_js_template}
echo "{% if KANISA_DEBUG_STATIC %}" >> ${management_js_template}
for i in $(find kanisa/static/kanisa/js/management/ -type f | sort); do
    localpath=${i:14}
    echo "<script src=\"{% static '${localpath}' %}\"></script>" >> ${management_js_template}
done
echo "{% else %}" >> ${management_js_template}
echo "<script src=\"{{ STATIC_URL 'kanisa/js/minified/kanisa-management.${management_js_hash}.js' %}\"></script>" >> ${management_js_template}
echo "{% endif %}" >> ${management_js_template}

css_template="kanisa/templates/kanisa/_css.html"
rm -f ${css_template}
touch ${css_template}
echo "{% load static from staticfiles %}" >> ${css_template}
echo "{% if KANISA_DEBUG_STATIC %}" >> ${css_template}
for i in $(find kanisa/static/kanisa/css/*.css | sort); do
    localpath=${i:14}
    echo "<link rel=\"stylesheet\" type=\"text/css\" media=\"all\" href=\"{% static '${localpath}' %}\" />" >> ${css_template}
done
echo "{% else %}" >> ${css_template}
echo "<link rel=\"stylesheet\" type=\"text/css\" media=\"all\" href=\"{% static 'kanisa/css/minified/kanisa.${css_hash}.css' %}\">" >> ${css_template}
echo "{% endif %}" >> ${css_template}

#!/usr/bin/bash

# ARGS
PAGE_NAME="$1"
TARGET_APP="$2"

# VARIABLES
DIRNAME=$(dirname "$0")
ABS_PATH=$(readlink -f "$DIRNAME")
BASE_TEMPLATE=""
TEMPLATE_DIR="$TARGET_APP/templates/$TARGET_APP/"
TARGET_URLS="$TARGET_APP/urls.py"
TARGET_VIEWS="$TARGET_APP/views.py"
URLPATTERNS_ARRAY_EXISTS=""
DJANGO_PATH_EXISTS=""

# Moving to Django Project Base directory
cd $ABS_PATH
cd ..

introduction_msg(){
	echo "Django Page Generator"
	echo ""
}

check_app_exists(){
	[ ! -d "$TARGET_APP" ] && echo -e "Error: Application $TARGET_APP cannot be found. Make sure you are in the correct directory." && exit 1
}

check_archetype_exists(){
	[ ! -f "$ABS_PATH/../frontend/templates/archetype.html" ] && echo "Error: Base template not found. Please create in your base project: frontend/templates/archetype.html" && exit 1
	BASE_TEMPLATE=$(cat "$ABS_PATH/../frontend/templates/archetype.html")
}

check_args(){
	[ -z "$PAGE_NAME" ] && echo "Error: No page name provided..." && exit 1
	[ -z "$TARGET_APP" ] && echo "Error: No application name provided..." && exit 1
}

check_template_dir(){
	[ ! -d "$TEMPLATE_DIR" ] && echo "Could not find $TEMPLATE_DIR. Creating $TEMPLATE_DIR..." && mkdir -p $TEMPLATE_DIR
}

check_urlpatterns_array_exists(){
	URLPATTERNS_ARRAY_EXISTS=$(cat "$TARGET_URLS" | grep 'urlpatterns')
	[ -z "$URLPATTERNS_ARRAY_EXISTS" ] && echo "No urlpatterns, creating one..." && echo 'urlpatterns = []' >> "$TARGET_URLS"
}

check_page_has_already_url(){
	URL_TO_PAGE_EXISTS=$(cat "$TARGET_URLS" | grep "$PAGE_NAME")
	[ ! -z "$URL_TO_PAGE_EXISTS" ] && echo "It seems that urls already exists." && exit 1
}

check_view_already_exists(){
	[ ! -z $(cat "$TARGET_VIEWS" | grep "$PAGE_NAME") ] && echo "It seems that a view already exists." && exit 1
}

check_url_patterns(){
	check_urlpatterns_array_exists
	check_page_has_already_url
}


check_django_path(){
	[ ! -f "$TARGET_URLS" ] && echo "Creating urls.py" && touch "$TARGET_URLS" && check_url_patterns
	DJANGO_PATH_EXISTS=$(cat "$TARGET_URLS" | grep -e 'from django.urls import path')
	[ -z "$DJANGO_PATH_EXISTS" ] && echo "Importing django.urls.path..." && echo -e "from django.urls import path\n$(cat $TARGET_URLS)" > "$TARGET_URLS"
}

introduction_msg

# Check prerequisites 

check_args
check_app_exists
check_archetype_exists
check_template_dir
check_django_path
check_url_patterns
check_view_already_exists

echo "Generating new page '$PAGE_NAME' for application '$TARGET_APP'..."

# GENERATE PAGE FROM BASE TEMPLATE

echo "Generating base template..."
echo -e $BASE_TEMPLATE > "$TEMPLATE_DIR/$PAGE_NAME.html" && echo "Ok"

# GENERATE URL TO TRIGGER VIEW


URLPATTERNS=$"
urlpatterns += [\n
	path('$PAGE_NAME', views.$PAGE_NAME, name='$PAGE_NAME'),\n
]\n
"
echo "Generating urlpatterns..."
echo -e $URLPATTERNS >> $TARGET_URLS && echo "Ok"

# GENERATE VIEW TO SERVE THE PAGE

VIEW=$"
def $PAGE_NAME(request):\n
	return render(\n
		request,\n
		'$TARGET_APP/$PAGE_NAME.html',\n
		{\n
			'page_title':'$PAGE_NAME'\n
		}\n
	)\n
"
echo "Generating view..."
echo -e $VIEW >> $TARGET_VIEWS && echo "Ok"

echo "Formatting files..."

find $TARGET_APP -name "*.py" -exec black {} \;

echo "Page Generated successfully! Open on localhost:8000/$PAGE_NAME"



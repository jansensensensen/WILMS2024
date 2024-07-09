
Wildcats Innovation Laboratory 
Management System

Pre- Requisites | Tools Used
•	Python 3.11.6 (https://www.python.org/downloads/release/python-3117/)
•	Node js 20.10 (https://nodejs.org/en/download)
•	VS Code (https://code.visualstudio.com/download)
•	Mysql Work Bench(https://dev.mysql.com/downloads/workbench/)
•	Visual C++ Build Tools (https://go.microsoft.com/fwlink/?LinkId=691126)
o	Tutorial (https://stackoverflow.com/questions/40504552/how-to-install-visual-c-build-tools)
•	Nginx 1.25.3 (http://nginx.org/en/download.html)
•	Repository
o	Django WILMS app - https://github.com/Mauledby/WILMS-SERVER 
o	React (Bookings Front End) - https://github.com/JusstPi/capstone_frontend
•	Copy of the SQL database file – (https://drive.google.com/drive/folders/1YF4zoLqpJcqI_xp9k6CmgOg0ikYKoJOr?usp=drive_link)
•	Copy of the WILMS nginx configuration file (https://drive.google.com/drive/folders/1YF4zoLqpJcqI_xp9k6CmgOg0ikYKoJOr?usp=drive_link)
•	Any Chromium Based Browser (Brave, Chrome, Chromium)
Pre- Requisites | Libraries Used
 
•	arabic-reshaper: 3.0.0
•	argon2-cffi: 23.1.0
•	argon2-cffi-bindings: 21.2.0
•	asgiref: 3.7.2
•	asn1crypto: 1.5.1
•	beautifulsoup4: 4.12.2
•	certifi: 2023.7.22
•	cffi: 1.15.1
•	charset-normalizer: 3.3.2
•	click: 8.1.7
•	colorama: 0.4.6
•	contourpy: 1.2.0
•	cryptography: 40.0.2
•	cssselect2: 0.7.0
•	cycler: 0.12.1
•	dj-database-url: 0.5.0
•	Django: 4.2.5
•	django-bootstrap-modal-forms: 2.2.1
•	django-braces: 1.15.0
•	django-common-helpers: 0.9.2
•	django-cors-headers: 3.14.0
•	django-cron: 0.5.1
•	django-datatables-view: 1.20.0
•	django-filter: 23.2
•	django-heroku: 0.3.1
•	django-model-serializer: 0.1.0
•	django-model-utils: 4.2.0
•	django-multiselectfield: 0.1.12
•	django-scheduler: 0.10.1
•	django-star-ratings: 0.9.2
•	django-tempus-dominus: 5.1.2.17
•	djangorestframework: 3.14.0
•	djangorestframework-jwt: 1.11.0
•	djangorestframework-simplejwt: 5.2.2
•	et-xmlfile: 1.1.0
•	fonttools: 4.44.0
•	future: 0.18.3
•	gunicorn: 20.1.0
•	html5lib: 1.1
•	icalendar: 5.0.10
•	idna: 3.4
•	kiwisolver: 1.4.5
•	lxml: 4.9.3
•	matplotlib: 3.8.1
•	mysql: 0.0.3
•	mysqlclient: 2.2.0
•	node: 1.2.1
•	numpy: 1.26.1
•	odict: 1.9.0
•	openpyxl: 3.0.10
•	oscrypto: 1.3.0
•	packaging: 23.2
•	pandas: 2.1.2
•	Pillow: 10.0.1
•	plotly: 5.18.0
•	plumber: 1.7
•	psycopg2: 2.9.6
•	pycparser: 2.21
•	pyHanko: 0.20.1
•	pyhanko-certvalidator: 0.24.1
•	PyJWT: 1.7.1
•	pyparsing: 3.1.1
•	pypdf: 3.17.0
•	pypng: 0.20220715.0
•	python-bidi: 0.4.2
•	python-dateutil: 2.8.2
•	python-decouple: 3.8
•	python-http-client: 3.3.7
•	pytz: 2023.3.post1
•	PyYAML: 6.0.1
•	qrcode: 7.4.2
•	reportlab: 3.6.13
•	requests: 2.31.0
•	schedule: 1.2.0
•	sendgrid: 6.10.0
•	serializers: 0.2.4
•	six: 1.16.0
•	soupsieve: 2.4.1
•	sqlparse: 0.4.4
•	starkbank-ecdsa: 2.2.0
•	svglib: 1.5.1
•	swapper: 1.3.0
•	sweet-alert: 1.1.3
•	tenacity: 8.2.3
•	tinycss2: 1.2.1
•	typing_extensions: 4.6.1
•	tzdata: 2023.3
•	tzlocal: 5.2
•	uritools: 4.0.2
•	urllib3: 2.0.7
•	webencodings: 0.5.1
•	whitenoise: 6.4.0
•	xhtml2pdf: 0.2.11
•	xlwt: 1.3.0
•	zope.component: 6.0
•	zope.deferredimport: 5.0
•	zope.deprecation: 5.0
•	zope.event: 5.0
•	zope.hookable: 6.0
•	zope.interface: 6.1
•	zope.lifecycleevent: 5.0
•	zope.proxy: 5.1
 

Installation Guide
1.	Begin by installing python, Node JS and VS Code
2.	Install mysql workbench and set the password to the local instance to P@ssword123 or change the password in the PROJECT Settings.py
3.	Import the database to the mysql workbench and name the database wilms_server
4.	Open VS Code and open the project
If you are going to look at WILMS for Development Purposes Follow below otherwise proceed to the next section.
5.	Create a Virtual Environment using the command python -m venv (name-of-your-venv)
6.	Activate venv by using the command venv/scripts/activate
a.	If you are outside the project folder (Where the manage.py file is located) move to that directory
7.	Afterwards run the function pip install -r requirements.txt
8.	You can then migrate your files 
a.	If you did not include the migration folders run “python manage.py makemigrations” before migrating
9.	Once done with all that finally run python manage.py runserver
If you are going to look at WILMS for Deployment Purposes Follow below otherwise proceed to the next section.
1.	Proceed to follow this tutorial and watch the YouTube video before continuing: https://youtu.be/BBKq6H9Rm5g as well as the written tutorial https://github.com/Johnnyboycurtis/webproject?tab=readme-ov-file#nginx-and-waitress
2.	Install nginx and create the templates 
3.	Copy the existing conf file and modify the location of the MEDIA AND STATICFILES
4.	Run a command prompt with administrator privilege (right click + run as administrator)
5.	Move to the directory of nginx and run the command nginx.exe
a.	To stop open another terminal and run the command nginx.exe -s stop
6.	Afterwards run another command prompt and move to the directory of the WILMS PROJECT
7.	And run the command python runserver.py
8.	Open a browser and move to the current users/computers Ip address or domain provided you have one.
REMINDERS
•	If having a change of devices change the base URL of the booking front and run a new build command and copy the contents to the templates folder of the api app in the Django project.
•	Be mindful of the configuration never push to the main branch but fork the project and push using the forked repository. Only push to the main branch when prior changes have gone through rigorous evaluation
 
 
Default Administrator Credentials
Email:wilms.wallet@gmail.com
Password:WILMs.1234

Email:wilmsadmin1@gmail.com
Password:1234

Links to the following:
GitHub: https://github.com/Mauledby/WILMS-SERVER
Figma:
•	https://www.figma.com/file/k1aMVxAskd9Z3L4zaWgvNv/Latest-Front-End?type=design&t=CcewanZ0N1NG3wnU-6
•	https://www.figma.com/file/iafQFT6KZcK15RPvq0LTCO/Untitled?type=design&t=CcewanZ0N1NG3wnU-6
•	https://www.figma.com/file/afohH3DfFIeHedqIv6vTwW/Facility-Management-System?type=design&t=CcewanZ0N1NG3wnU-6


Contact Personnel

Name: Kirk Montejo
Mobile Number: +63 977 007 4364
Email: montejokirk@gmail.com
Institutional Email: kirk.montejo@cit.edu
Github Account Link: https://github.com/Mauledby

Name: Justin Juaman
Mobile Number: +63 9664115440
Email: justinabarquez73@gmail.com
Institutional Email: justin.juaman@cit.edu
Github Account Link: https://github.com/tuntin123

Name: Eloisa Marie Desucatan
Mobile Number: +63 966 185 7675
Email: eloisadesucatan29@gmail.com
Institutional Email: eloisamarie.desucatan@cit.edu
Github Account Link: https://github.com/Eloisamarie29

Name: Genica Seng
Mobile Number: +63 976 271 3637
Email: seng.genicamaee@gmail.com
Institutional Email: genicamae.seng@cit.edu
Github Account Link: https://github.com/gemmygs

Name: Mark Jerich A. Taboada
Mobile Number: +63 976 369 0004
Email: mjerichtaboada@gmail.com
Institutional Email: markjerich.taboada@cit.edu
Github Account Link: https://github.com/mjat123

Name: Charmaine Helven G. Resma
Mobile Number: +63 945 140 6326
Email: chgresma@gmail.com
Institutional Email: charmainehelven.resma@cit.edu
Github Account Link: https://github.com/chgresma

Name: Jhazer Andre A. Andrade
Mobile Number: +63 906 413 4527
Email: jhazer11@gmail.com
Institutional Email: jhazerandre.andrade@cit.edu
Github Account Link: https://github.com/Androi11

Name: Diether T. Gingoyon
Mobile Number: +63 9638524501
Email: gingoyondiether@gmail.com
Institutional Email:diether.gingoyon@cit.edu
Github Account Link: https://github.com/WildMan123122

Name: John Jay Gomez
Mobile Number: +63 9
Email: jaygomez2468@gmail.com
Institutional Email:johnjay.gomez@cit.edu
Github Account Link: 

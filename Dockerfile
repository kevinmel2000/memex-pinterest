FROM ubuntu:12.04
ENV DEBIAN_FRONTEND noninteractive

# software-properties-common contains "add-apt-repository" command for PPA conf
RUN apt-get update && apt-get install -y software-properties-common python-software-properties libxml2-dev libxslt1-dev python-dev build-essential python-lxml python-pip libffi-dev net-tools nmap python-numpy python-scipy gfortran libopenblas-dev liblapack-dev git apache2 libapache2-mod-wsgi

# Add the package verification key
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

RUN pip install \
	pymongo \
	scrapy \
	scrapyd \
	python-scrapyd-api \
	lxml \
	service_identity \
	pytest \
	tldextract \
	reppy \
	scrapy-inline-requests \
	flask \
	html2text \
	tqdm \
	tornado

RUN pip install numpy --upgrade
RUN pip install scipy --upgrade
RUN pip install scikit-learn

RUN git clone https://github.com/TeamHG-Memex/memex-scrapy-utils.git /memex-scrapy-utils
WORKDIR /memex-scrapy-utils
RUN python setup.py install

ADD . /memex-pinterest
RUN cp /memex-pinterest/ui/memexpin.conf /etc/apache2/sites-available/
RUN chmod 644 /etc/apache2/sites-available/memexpin.conf
RUN a2dissite default
RUN a2dissite default-ssl
RUN a2ensite memexpin.conf

EXPOSE 80
EXPOSE 6800

WORKDIR /memex-pinterest

CMD ["bash", "start_all_services.bash"]
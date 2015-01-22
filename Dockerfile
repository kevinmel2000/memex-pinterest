FROM ubuntu:12.04
ENV DEBIAN_FRONTEND noninteractive

# software-properties-common contains "add-apt-repository" command for PPA conf
RUN apt-get update && apt-get install -y software-properties-common python-software-properties libxml2-dev libxslt1-dev python-dev build-essential python-lxml python-pip libffi-dev net-tools nmap python-numpy python-scipy gfortran libopenblas-dev liblapack-dev

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
	tqdm

RUN pip install numpy --upgrade
RUN pip install scipy --upgrade
RUN pip install scikit-learn

ADD . /memex-pinterest

EXPOSE 80
EXPOSE 6800

WORKDIR /memex-pinterest

ENTRYPOINT ["bash", "start_all_services.bash"]
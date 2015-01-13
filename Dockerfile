FROM ubuntu:14.10
ENV DEBIAN_FRONTEND noninteractive

# software-properties-common contains "add-apt-repository" command for PPA conf
RUN apt-get update && apt-get install -y software-properties-common python-software-properties mongodb libxml2-dev libxslt1-dev python-dev build-essential python-lxml python-pip

RUN pip install \
	pymongo \
	scrapy \
	scrapyd \
	splash \
	python-scrapyd-api \
	lxml \
	service_identity \
	pytest \
	tldextract \
	reppy \
	scrapy-inline-requests \
	rfc822

ADD . /memex-pinterest
WORKDIR /memex-pinterest/ui/mongoutils
RUN python memex_mongo_utils.py



EXPOSE 5000
WORKDIR /memex-pinterest/ui
CMD python server.py
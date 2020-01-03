FROM centos:7

RUN yum install -y wget unzip

RUN yum install -y https://repo.ius.io/ius-release-el7.rpm

RUN yum install -y python36u python36u-libs python36u-devel python36u-pip

RUN yum install -y python3-devel mysql-devel

RUN yum groups install -y "Development Tools"

RUN mkdir /justeece

WORKDIR /justeece

ADD requirements.txt /justeece

RUN pip3 install -r requirements.txt

ADD . /justeece

EXPOSE 5500

HEALTHCHECK --interval=5000s --timeout=3s CMD curl --fail http://localhost:5500  || exit 0

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:5500



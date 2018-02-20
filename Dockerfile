FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update

# Here we install a python coverage tool and an
# https library that is out of date in the base image.

RUN pip install coverage

# Fix Python SSL warnings for python < 2.7.9 (system python on Trusty is 2.7.6)
# https://github.com/pypa/pip/issues/4098
RUN pip install pip==8.1.2
RUN pip install --disable-pip-version-check requests requests_toolbelt pyopenssl --upgrade
RUN pip install cerberus

# update security libraries in the base image
RUN pip install cffi --upgrade \
    && pip install pyopenssl --upgrade \
    && pip install ndg-httpsclient --upgrade \
    && pip install pyasn1 --upgrade \
    && pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module


#Install Diamond Binary v0.9.17
#WORKDIR /kb/deployment/bin
#RUN wget https://github.com/bbuchfink/diamond/releases/download/v0.9.17/diamond-linux64.tar.gz \
#    && tar -xvf diamond-linux64.tar.gz diamond \
#    && rm diamond-linux64.tar.gz

#WORKDIR /kb/deployment/bin
#    RUN wget https://github.com/bbuchfink/diamond/archive/master.zip \
#    && unzip master.zip \
#    && cd diamond-master \
#    && sh build_simple.sh \
#    && mv diamond ../ \
#    && cd .. \
#    && rm -rf diamond-master




WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]

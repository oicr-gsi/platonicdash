FROM python:3.6

USER root

# mount platonicdash code at /platonicdash
WORKDIR /platonicdash
# copy in just what directories are required to avoid accidentally copying in
# the cache or Dockerfile
COPY *.py requirements.txt /platonicdash/

# Requirements for pytables (HDF5) and scipy (blas and la and fortran) and expect for passing a passphrase to ssh-agent
RUN apt-get -yy update && apt-get -yy install libhdf5-serial-dev libblas3 liblapack3 liblapack-dev libblas-dev gfortran expect
RUN pip install --trusted-host pypi.python.org $(awk '!/git\+ssh.*/' requirements.txt) && pip install gunicorn

COPY application /platonicdash/application/

EXPOSE 5000
COPY .docker/start.sh .docker/nginx /dashi/.docker/ 
CMD bash /dashi/.docker/start.sh



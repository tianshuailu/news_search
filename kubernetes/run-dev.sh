#!/bin/bash

# create name space neww-search
kubectl create -f namespace.yaml

# set the namespace for the current context
kubectl config set-context --current --namespace=news-search

# create nginx configmap
# not sure if the path work for deployment env
kubectl create configmap nginx-conf --from-file=../frontend/nginx.conf

# create backend and frontend deployments
kubectl apply -f .


# ME TRACKER 

## install

### prerequisites
install python3.x (probably 3.7+??)


### install dependencies
`py -m pip install -r requirements.txt`


## run local
`py me_collections_tracker.py --log info`

# run in container
docker build . -t me_tracker:0.1 --no-cache
docker run -dp 8000:8000 me_tracker

# run in kubernetes (after building)
    * the key here is that it must be specifically tagged (not latest or it won't pull from local)
minikube image load me_tracker:0.1 
kubectl create deployment me-tr4k3r --image=me_tracker:0.1 
kubectl expose deployment me-tr4k3r --type=NodePort --port=8080
minikube service me-tr4k3r


## todo
everything

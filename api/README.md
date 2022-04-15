


# run in container
docker build . -t me_viz:0.1 --no-cache
docker run -dp 8000:8000 me_viz

# run in kubernetes (after building)
    * the key here is that it must be specifically tagged (not latest or it won't pull from local)
minikube image load me_viz:0.1 
kubectl create deployment me-2api --image=me_viz:0.1 
kubectl expose deployment me-2api --type=NodePort --port=8080
minikube service me-2api

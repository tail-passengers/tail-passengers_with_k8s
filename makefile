all:
	kubectl apply -f k8s/.

clean: 
	kubectl delete -f k8s/.
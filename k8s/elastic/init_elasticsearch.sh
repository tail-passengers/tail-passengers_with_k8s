#!/bin/bash
# 참고: https://somuch.medium.com/elk-k8s%EC%97%90-elastic-stack-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0-1-2-dcce5f3776e8

# Elastic Operator 추가
# kubectl get all -n elastic-system 명령어로 배포 확인 가능
# kubectl get crd 로도 확인 가능
# https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html
kubectl create -f https://download.elastic.co/downloads/eck/2.13.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.13.0/operator.yaml


# CRD를 활용하여 Elasticsearch 배포
# https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html
kubectl apply -f elasticsearch.yaml

# Elasticsearch 배포가 완료될 때까지 대기
# 이때 PVC도 자동으로 할당된다.
sleep 3
wait_time=10
output="unknown"
while [ "$output" == "unknown" ] ; do
  output=$(kubectl get elasticsearch -o jsonpath='{.items[0].status.health}')
  if [ "$output" == "unknown" ]; then
    echo "Wait..."
    sleep $wait_time
  elif [ "$output" != "green" ]; then
    echo "Elasticsearch is not healthy. Current HEALTH value: $output"
    exit 1
  fi
done
echo "Elasticsearch is ready."


# 기본으로 생성된 elastic 계정의 비밀번호 확인
#PASSWORD=$(kubectl get secret elasticsearch-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')

# TODO elasticsearch-es-http 서비스를 nodeport로 변경하기

# 포트포워딩 후, https://localhost:9200 접속
# ID: elastic, PW: 위에 값으로 입력하면 응답이 나온다.
# kubectl port-forward service/elasticsearch-es-http 9200
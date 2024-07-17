#!/bin/bash
# 참고: https://somuch.medium.com/elk-k8s%EC%97%90-elastic-stack-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0-2-2-f961e3447d01

# kibana 배포
# Elastic Operator에 kibana도 포함되어 있기에 따로 추가할 것은 없음
# https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-kibana.html

kubectl apply -f kibana.yaml

sleep 3
wait_time=10
output="red"
while [ "$output" == "red" ] ; do
  output=$(kubectl get kibana -o jsonpath='{.items[0].status.health}')
  if [ "$output" == "red" ]; then
    echo "Wait..."
    sleep $wait_time
  elif [ "$output" != "green" ]; then
    echo "Kibana is not healthy. Current HEALTH value: $output"
    exit 1
  fi
done
echo "Kibana is ready."


# TODO kibana-kb-http 서비스를 nodeport로 변경하기

# 포트포워딩 후, https://localhost:5601 접속
# ID: elastic, PW: elasticsearch 에서 얻는 비밀번호
# kubectl port-forward service/kibana-kb-http 5601

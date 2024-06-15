# tail-passengers with k8s

## 개요

이 프로젝트는 k8s를 이용하여 tail-passengers를 배포하는 프로젝트입니다.


## 기본 프로젝트와 차이점

- `docker compose` 대신 `k8s`를 사용합니다.
- `middlleware`와 `frontend`를 합쳐서 웹서버가 `frontend`와 함께 배포되도록 변경했습니다.
- load balancer를 따로 사용하지 않기 때문에 nodePort를 사용하여 30443 포트로 접근해야 합니다.


## 사용법

- `kubectl` 설치가 필요합니다.

### 배포

```shell
$ make
```

- 1분 정도 기다리면 배포가 완료됩니다.
- `https://127.0.0.1:30443/api/v1/login/Harry` 로 접속할 수 있습니다.

### 종료

```shell
$ make clean
```


## 추후 계획

- ELK Stack을 추가할 예정입니다.
- AWS에 배포하여 여러 사이트에서 사용할 수 있는지 실습할 예정입니다.
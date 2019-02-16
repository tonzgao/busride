# README
Many services exist which have release dates (IMDB, Goodreads, Amazon, Metacritic, etc).
However, it is a pain to constantly have to monitor these sites.

Busride will allow a user to submit their api keys for these services, query a user's watchlist, and notify when relevant releases occur.

Licensing: GPL/v3
This is a non-profit personal project.

--------
# Sanic
Busride uses sanic to manage it's infrastructure. 
Sanic is a build tool and cluster management tool used at parsehub.

It provides:
- Kubernetes
- Logging
- Prometheus Operator
- Distributed Docker Registry (not shown)
- Dynamic Storage (not shown)
```
NAMESPACE          NAME                                      READY   STATUS      RESTARTS   AGE
kube-system        coredns-86c58d9df4-54cwk                  1/1     Running     0          21m
kube-system        default-http-backend-695f988578-6qsxn     1/1     Running     0          19m
kube-system        es-data-chvww                             2/2     Running     1          13m
kube-system        es-master-cmhs9                           2/2     Running     1          13m
kube-system        etcd-macbook                              1/1     Running     0          20m
kube-system        filebeat-m9klw                            1/1     Running     0          13m
kube-system        journalbeat-8fxtm                         1/1     Running     0          13m
kube-system        kibana-7f9b4d6dbf-4tz4k                   1/1     Running     0          13m
kube-system        kube-apiserver-macbook                    1/1     Running     0          20m
kube-system        kube-controller-manager-macbook           1/1     Running     1          20m
kube-system        kube-flannel-ds-czpq5                     1/1     Running     0          21m
kube-system        kube-proxy-6dfr8                          1/1     Running     0          21m
kube-system        kube-scheduler-macbook                    1/1     Running     0          20m
kube-system        logstash-56bf499d79-zjcxm                 2/2     Running     0          13m
kube-system        nginx-ingress-controller-fpqxk            1/1     Running     0          19m
kube-system        node-reverse-proxy-macbook                1/1     Running     0          20m
kube-system        tiller-deploy-6cf89f5895-7qr48            1/1     Running     0          14m
monitoring         prometheus-operator-867bbfddbd-w9cd5      1/1     Running     0          13m
```

---

# Infra
Infra is installed through helm. 
Specific values.yaml files are generated through ph-confer, based on the mako templating engine.
Currently used:
- SQL: Postgresql
    - Users
    - ApiKeys
    - Subscriptions
- Document: MongoDB
- Key-Value: Redis

```
NAMESPACE          NAME                                      READY   STATUS      RESTARTS   AGE
infra              mongo-mongodb-7f456f88d5-jp5vt            1/1     Running     1          67m
infra              redis-ha-server-0                         2/2     Running     0          60m
infra              sql-postgresql-0                          1/1     Running     0          67m
```

---
# Services
- Web: react ui
- Admin: dashboards
- Backup: backup infra
- Apis:
    - auth
    - subscriber
    - exporter
- Fetcher(s):
    - Amazon
    - Goodreads
    - Metacritic
    - etc.

```
NAMESPACE          NAME                                      READY   STATUS      RESTARTS   AGE
default            api-deployment-646697dd59-2jv9h           1/1     Running     0          64s
default            web-deployment-876dd69c7-5g6fg            1/1     Running     0          64s
```
-------

# Release Schedule: 
I'm too lazy for personal projects. 
I'll probably work on this for ~5-10 hours every long weekend.

1. setup local cluster + infra helm charts (done).
2. setup basic consumer api and maybe 1 fetcher
3. more fetchers and tests
4. very basic web ui
5. auth
6. buy and setup dns
7. tbd
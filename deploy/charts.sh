

helm init --client-only
helm repo update

helm upgrade --install redis-ha stable/redis-ha --namespace infra --values=deploy/values/redis.yaml
helm upgrade --install mongo stable/mongodb --namespace infra --values=deploy/values/mongo.yaml
helm upgrade --install sql stable/postgresql --namespace infra --values=deploy/values/sql.yaml
#helm upgrade --install cert-manager stable/cert-manager --namespace kube-system
# prometheus
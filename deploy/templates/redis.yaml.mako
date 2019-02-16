<%!
    import os
    import sys
    import base64
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../values/redis.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
    num_replicas = 1 if run_mode == 'dev' else 2
%>\

## Configure resource requests and limits
## ref: http://kubernetes.io/docs/user-guide/compute-resources/
##
image:
  repository: redis
  tag: 5.0.0-stretch
  pullPolicy: IfNotPresent
## replicas number for each component
replicas: ${num_replicas}

## Redis specific configuration options
redis:
  port: 6379
  masterGroupName: mymaster
  config:
    ## Additional redis conf options can be added below
    ## For all available options see http://download.redis.io/redis-stable/redis.conf
    min-slaves-to-write: ${max(0, min(num_replicas-2, num_replicas/2-1))}
    min-slaves-max-lag: 5   # Value in seconds
    maxmemory: "0"       # Max memory to use for each redis instance. Default is unlimited.
    maxmemory-policy: "volatile-lru"  # Max memory policy to use for each redis instance. Default is volatile-lru.
    # Determines if scheduled RDB backups are created. Default is false.
    # Please note that local (on-disk) RDBs will still be created when re-syncing with a new slave. The only way to prevent this is to enable diskless replication.
    save: "900 1"
    # When enabled, directly sends the RDB over the wire to slaves, without using the disk as intermediate storage. Default is false.
    repl-diskless-sync: "yes"
    rdbcompression: "yes"
    rdbchecksum: "yes"
    appendonly: "yes"

  ## Custom redis.conf files used to override default settings. If this file is
  ## specified then the redis.config above will be ignored.
  # customConfig: |-
      # Define configuration here

  resources: {}
  #  requests:
  #    memory: 200Mi
  #    cpu: 100m
  #  limits:
  #    memory: 700Mi

## Sentinel specific configuration options
sentinel:
  port: 26379
  quorum: ${num_replicas/2+1}
  config:
    ## Additional sentinel conf options can be added below. Only options that
    ## are expressed in the format simialar to 'sentinel xxx mymaster xxx' will
    ## be properly templated.
    ## For available options see http://download.redis.io/redis-stable/sentinel.conf
    down-after-milliseconds: 10000
    ## Failover timeout value in milliseconds
    failover-timeout: 180000
    parallel-syncs: 5

  ## Custom sentinel.conf files used to override default settings. If this file is
  ## specified then the sentinel.config above will be ignored.
  # customConfig: |-
      # Define configuration here

  resources: {}
  #  requests:
  #    memory: 200Mi
  #    cpu: 100m
  #  limits:
  #    memory: 200Mi

securityContext:
  runAsUser: 1000
  fsGroup: 1000
  runAsNonRoot: true

## Node labels, affinity, and tolerations for pod assignment
## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector
## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#taints-and-tolerations-beta-feature
## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
affinity: |
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app:  {{ template "redis-ha.name" . }}
            release: {{ .Release.Name }}
        topologyKey: failure-domain.beta.kubernetes.io/zone

podDisruptionBudget: {}
  # maxUnavailable: 1
  # minAvailable: 1

## Configures redis with AUTH (requirepass & masterauth conf params)
auth: false
redisPassword: password

persistentVolume:
  enabled: true
  storageClass: ${'sanic-rook' if run_mode == 'prod' else 'local'}
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  annotations: {}
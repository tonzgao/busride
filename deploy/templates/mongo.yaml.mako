<%!
    import os
    import sys
    import base64
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../values/mongo.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
%>\
## Global Docker image registry
## Please, note that this will override the image registry for all the images, including dependencies, configured to use the global value
##
# global:
#   imageRegistry:

image:
  ## Bitnami MongoDB registry
  ##
  registry: docker.io
  ## Bitnami MongoDB image name
  ##
  repository: bitnami/mongodb
  ## Bitnami MongoDB image tag
  ## ref: https://hub.docker.com/r/bitnami/mongodb/tags/
  ##
  tag: 4.0.6

  ## Specify a imagePullPolicy
  ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
  ##
  pullPolicy: Always
  ## Optionally specify an array of imagePullSecrets.
  ## Secrets must be manually created in the namespace.
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistrKeySecretName

  ## Set to true if you would like to see extra information on logs
  ## It turns NAMI debugging in minideb
  ## ref:  https://github.com/bitnami/minideb-extras/#turn-on-nami-debugging
  debug: false

## Enable authentication
## ref: https://docs.mongodb.com/manual/tutorial/enable-authentication/
#
usePassword: false

## MongoDB custom user and database
## ref: https://github.com/bitnami/bitnami-docker-mongodb/blob/master/README.md#creating-a-user-and-database-on-first-run
##
# mongodbUsername: username
# mongodbPassword: password
# mongodbDatabase: database

## Whether enable/disable IPv6 on MongoDB
## ref: https://github.com/bitnami/bitnami-docker-mongodb/blob/master/README.md#enabling/disabling-ipv6
##
mongodbEnableIPv6: false

## MongoDB System Log configuration
## ref: https://github.com/bitnami/bitnami-docker-mongodb#configuring-system-log-verbosity-level
##
mongodbSystemLogVerbosity: 0
mongodbDisableSystemLog: false

## MongoDB additional command line flags
##
## Can be used to specify command line flags, for example:
##
## mongodbExtraFlags:
##  - "--wiredTigerCacheSizeGB=2"
mongodbExtraFlags: []

## Pod Security Context
## ref: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
##
securityContext:
  enabled: true
  fsGroup: 1001
  runAsUser: 1001

## Kubernetes Cluster Domain
clusterDomain: cluster.local

## Kubernetes service type
service:
  annotations: {}
  type: ClusterIP
  # clusterIP: None
  port: 27017

  ## Specify the nodePort value for the LoadBalancer and NodePort service types.
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
  ##
  # nodePort:


## Setting up replication
## ref: https://github.com/bitnami/bitnami-docker-mongodb#setting-up-a-replication
#
replicaSet:
  ## Whether to create a MongoDB replica set for high availability or not
  enabled: ${'true' if run_mode == 'prod' else 'false'}
  useHostnames: true

  ## Name of the replica set
  ##
  name: rs0

  ## Key used for replica set authentication
  ##
  # key: key

  ## Number of replicas per each node type
  ##
  replicas:
    secondary: 1
    arbiter: 1
  ## Pod Disruption Budget
  ## ref: https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
  pdb:
    minAvailable:
      primary: 1
      secondary: 1
      arbiter: 1

# Annotations to be added to MongoDB pods
podAnnotations: {}

# Additional pod labels to apply
podLabels: {}

## Configure resource requests and limits
## ref: http://kubernetes.io/docs/user-guide/compute-resources/
##
resources: {}
# limits:
#   cpu: 500m
#   memory: 512Mi
# requests:
#   cpu: 100m
#   memory: 256Mi

## Node selector
## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector
nodeSelector: {}

## Affinity
## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
affinity: {}

## Tolerations
## ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
tolerations: []

## Enable persistence using Persistent Volume Claims
## ref: http://kubernetes.io/docs/user-guide/persistent-volumes/
##
persistence:
  enabled: true
  ## A manually managed Persistent Volume and Claim
  ## Requires persistence.enabled: true
  ## If defined, PVC must be created manually before volume will be bound
  # existingClaim:

  ## mongodb data Persistent Volume Storage Class
  ## If defined, storageClassName: <storageClass>
  ## If set to "-", storageClassName: "", which disables dynamic provisioning
  ## If undefined (the default) or set to null, no storageClassName spec is
  ##   set, choosing the default provisioner.  (gp2 on AWS, standard on
  ##   GKE, AWS & OpenStack)
  ##
  storageClass: ${'sanic-rook' if run_mode == 'prod' else 'local'}
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  annotations: {}

## Configure extra options for liveness and readiness probes
## ref: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#configure-probes)
livenessProbe:
  enabled: true
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 6
  successThreshold: 1
readinessProbe:
  enabled: true
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 6
  successThreshold: 1

# Entries for the MongoDB config file
configmap:
#  # Where and how to store data.
#  storage:
#    dbPath: /opt/bitnami/mongodb/data/db
#    journal:
#      enabled: true
#    #engine:
#    #wiredTiger:
#  # where to write logging data.
#  systemLog:
#    destination: file
#    logAppend: true
#    path: /opt/bitnami/mongodb/logs/mongodb.log
#  # network interfaces
#  net:
#    port: 27017
#    bindIp: 0.0.0.0
#    unixDomainSocket:
#      enabled: true
#      pathPrefix: /opt/bitnami/mongodb/tmp
#  # replica set options
#  replication:
#    replSetName: replicaset
#  # process management options
#  processManagement:
#     fork: false
#     pidFilePath: /opt/bitnami/mongodb/tmp/mongodb.pid
#  # set parameter options
#  setParameter:
#     enableLocalhostAuthBypass: true
#  # security options
#  security:
#    authorization: enabled
#    keyFile: /opt/bitnami/mongodb/conf/keyfile

## Prometheus Exporter / Metrics
##
metrics:
  enabled: ${'true' if run_mode == 'prod' else 'false'}

  image:
    registry: docker.io
    repository: forekshub/percona-mongodb-exporter
    tag: latest
    pullPolicy: IfNotPresent
    ## Optionally specify an array of imagePullSecrets.
    ## Secrets must be manually created in the namespace.
    ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
    ##
    # pullSecrets:
    #   - myRegistrKeySecretName

  ## Metrics exporter resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  # resources: {}

  ## Metrics exporter pod Annotation
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9216"

  ## Prometheus Service Monitor
  ## ref: https://github.com/coreos/prometheus-operator
  ##      https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md
  serviceMonitor:
    ## If the operator is installed in your cluster, set to true to create a Service Monitor Entry
    enabled: false
    ## Used to pass Labels that are used by the Prometheus installed in your cluster to select Service Monitors to work with
    ## ref: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#prometheusspec
    additionalLabels: {}

    ## Specify Metric Relabellings to add to the scrape endpoint
    ## ref: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#endpoint
    # relabellings:

    alerting:
      ## Define individual alerting rules as required
      ## ref: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#rulegroup
      ##      https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
      rules: {}

      ## Used to pass Labels that are used by the Prometheus installed in your cluster to select Prometheus Rules to work with
      ## ref: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#prometheusspec
      additionalLabels: {}

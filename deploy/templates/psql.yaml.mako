<%!
    import os
    import sys
    import base64
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../values/sql.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
%>\

## Global Docker image registry
### Please, note that this will override the image registry for all the images, including dependencies, configured to use the global value
###
## global:
##   imageRegistry:

## Bitnami PostgreSQL image version
## ref: https://hub.docker.com/r/bitnami/postgresql/tags/
##
image:
  registry: docker.io
  repository: bitnami/postgresql
  tag: 10.7.0
  ## Specify a imagePullPolicy
  ## Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
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
  ## It turns BASH and NAMI debugging in minideb
  ## ref:  https://github.com/bitnami/minideb-extras/#turn-on-bash-debugging
  debug: false

##
## Init containers parameters:
## volumePermissions: Change the owner of the persist volume mountpoint to RunAsUser:fsGroup
##
volumePermissions:
  enabled: true
  image:
    registry: docker.io
    repository: bitnami/minideb
    tag: latest
    ## Specify a imagePullPolicy
    ## Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
    ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
    ##
    pullPolicy: Always
  ## Init container Security Context
  securityContext:
    runAsUser: 0

## Pod Security Context
## ref: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
##
securityContext:
  enabled: true
  fsGroup: 1001
  runAsUser: 1001

replication:
  enabled: false
  user: repl_user
  password: repl_password
  slaveReplicas: 1
  ## Set synchronous commit mode: on, off, remote_apply, remote_write and local
  ## ref: https://www.postgresql.org/docs/9.6/runtime-config-wal.html#GUC-WAL-LEVEL
  synchronousCommit: "off"
  ## From the number of `slaveReplicas` defined above, set the number of those that will have synchronous replication
  ## NOTE: It cannot be > slaveReplicas
  numSynchronousReplicas: 0
  ## Replication Cluster application name. Useful for defining multiple replication policies
  applicationName: my_application

## PostgreSQL admin user
## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md#setting-the-root-password-on-first-run
postgresqlUsername: postgres

## PostgreSQL password
## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md#setting-the-root-password-on-first-run
##
# postgresqlPassword:

## PostgreSQL password using existing secret
## existingSecret: secret

## Mount PostgreSQL secret as a file instead of passing environment variable
# usePasswordFile: false

## Create a database
## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md#creating-a-database-on-first-run
##
# postgresqlDatabase:

## PostgreSQL data dir
## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md
##
postgresqlDataDir: /bitnami/postgresql

## Specify extra initdb args
## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md
##
# postgresqlInitdbArgs:

## Specify a custom location for the PostgreSQL transaction log
## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md
##
# postgresqlInitdbWalDir:


## PostgreSQL configuration
## Specify runtime configuration parameters as a dict, using camelCase, e.g.
## {"sharedBuffers": "500MB"}
## Alternatively, you can put your postgresql.conf under the files/ directory
## ref: https://www.postgresql.org/docs/current/static/runtime-config.html
##
# postgresqlConfiguration:

## PostgreSQL extended configuration
## As above, but _appended_ to the main configuration
## Alternatively, you can put your *.conf under the files/conf.d/ directory
## https://github.com/bitnami/bitnami-docker-postgresql#allow-settings-to-be-loaded-from-files-other-than-the-default-postgresqlconf
##
# postgresqlExtendedConf:

## PostgreSQL client authentication configuration
## Specify content for pg_hba.conf
## Default: do not create pg_hba.conf
## Alternatively, you can put your pg_hba.conf under the files/ directory
# pgHbaConfiguration: |-
#   local all all trust
#   host all all localhost trust
#   host mydatabase mysuser 192.168.0.0/24 md5

## ConfigMap with PostgreSQL configuration
## NOTE: This will override postgresqlConfiguration and pgHbaConfiguration
# configurationConfigMap:

## ConfigMap with PostgreSQL extended configuration
# extendedConfConfigMap:

## initdb scripts
## Specify dictionnary of scripts to be run at first boot
## Alternatively, you can put your scripts under the files/docker-entrypoint-initdb.d directory
##
# initdbScripts:
#   my_init_script.sh:|
#      #!/bin/sh
#      echo "Do something."
#
## ConfigMap with scripts to be run at first boot
## NOTE: This will override initdbScripts
# initdbScriptsConfigMap:

## Secret with scripts to be run at first boot (in case it contains sensitive information)
## NOTE: This can work along initdbScripts or initdbScriptsConfigMap
# initdbScriptsSecret:

## Optional duration in seconds the pod needs to terminate gracefully.
## ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods
##
# terminationGracePeriodSeconds: 30

## PostgreSQL service configuration
service:
  ## PosgresSQL service type
  type: ClusterIP
  # clusterIP: None
  port: 5432

  ## Specify the nodePort value for the LoadBalancer and NodePort service types.
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
  ##
  # nodePort:

  ## Provide any additional annotations which may be required. This can be used to
  annotations: {}
  ## Set the LoadBalancer service type to internal only.
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#internal-load-balancer
  ##
  # loadBalancerIP:

## PostgreSQL data Persistent Volume Storage Class
## If defined, storageClassName: <storageClass>
## If set to "-", storageClassName: "", which disables dynamic provisioning
## If undefined (the default) or set to null, no storageClassName spec is
##   set, choosing the default provisioner.  (gp2 on AWS, standard on
##   GKE, AWS & OpenStack)
##
persistence:
  enabled: true
  ## A manually managed Persistent Volume and Claim
  ## If defined, PVC must be created manually before volume will be bound
  # existingClaim:
  mountPath: /bitnami/postgresql
  storageClass: ${'sanic-rook' if run_mode == 'prod' else 'local'}
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  annotations: {}

## updateStrategy for PostgreSQL StatefulSet and its slaves StatefulSets
## ref: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies
updateStrategy:
  type: RollingUpdate

##
## PostgreSQL Master parameters
##
master:
  ## Node, affinity and tolerations labels for pod assignment
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#taints-and-tolerations-beta-feature
  nodeSelector: {}
  affinity: {}
  tolerations: []

##
## PostgreSQL Slave parameters
##
slave:
  ## Node, affinity and tolerations labels for pod assignment
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#taints-and-tolerations-beta-feature
  nodeSelector: {}
  affinity: {}
  tolerations: []

## Configure resource requests and limits
## ref: http://kubernetes.io/docs/user-guide/compute-resources/
##
resources:
  requests:
    memory: 256Mi
    cpu: 250m

networkPolicy:
  ## Enable creation of NetworkPolicy resources.
  ##
  enabled: false

  ## The Policy model to apply. When set to false, only pods with the correct
  ## client label will have network access to the port PostgreSQL is listening
  ## on. When true, PostgreSQL will accept connections from any source
  ## (with the correct destination port).
  ##
  allowExternal: true

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

## Configure metrics exporter
##
metrics:
  enabled: false
  # resources: {}
  service:
    type: ClusterIP
    annotations:
      prometheus.io/scrape: "true"
      prometheus.io/port: "9187"
    loadBalancerIP:
  image:
    registry: docker.io
    repository: wrouesnel/postgres_exporter
    tag: v0.4.7
    pullPolicy: IfNotPresent
    ## Optionally specify an array of imagePullSecrets.
    ## Secrets must be manually created in the namespace.
    ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
    ##
    # pullSecrets:
    #   - myRegistrKeySecretName

  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#configure-probes)
  ## Configure extra options for liveness and readiness probes
  livenessProbe:
    enabled: true
    initialDelaySeconds: 5
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

# Define custom environment variables to pass to the image here
extraEnv: {}
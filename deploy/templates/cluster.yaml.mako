<%!
    import os
    import subprocess
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../built/cluster.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
    cluster_id = os.getenv('CLUSTER_ID')
    if cluster_id is None:
      raise Exception('You must set the CLUSTER_ID variable! Try CLUSTER_ID=[...] [command]!')
    sanic_domain = os.getenv('SANIC_DOMAIN')
    if sanic_domain is None:
      raise Exception('You must set the SANIC_DOMAIN variable to, e.g., local.busride.com!')
    image_tag = os.getenv('IMAGE_TAG')
    if image_tag is None:
      raise Exception('You must set the IMAGE_TAG variable to a valid image tag!')
%>\
<%def name="service(
    name,
    image=None,
    label=None,
    replicas=1,
    limit_mem=None,
    requested_mem=None,
    limit_cpu=None,
    requested_cpu=None,
    probe_url=None,
    ports=(),
    volumes=(),
    live_mount=True,
    additional_pod_spec=(),
    additional_container_spec=()
)">\
<% if image is None: image = '{}/services/{}'.format('localhost:5599' if run_mode != 'dev' else 'registry.placeholder.com', name.replace('-','_')) %>\
<% has_volumes = (run_mode == 'dev' and live_mount) or len(volumes) > 0 %>\
<% if label is None: raise Exception('You must specify a node label!') %>\
---

kind: Deployment
apiVersion: apps/v1beta1
metadata:
  name: ${name}-deployment
  namespace: ${cluster_id}
spec:
  replicas: ${replicas}
  template:
    metadata:
      labels:
        app: ${name}
    spec:
      nodeSelector:
        ${label}: ""
      # additional pod spec begins
      %for spec in additional_pod_spec:
${spec()}\
      %endfor
      # additional pod spec ends
      containers:
      - name: ${name}
        image: ${image}:${image_tag}
        % if run_mode == 'dev':
        imagePullPolicy: Never
        %else:
        imagePullPolicy: Always
        % endif
        %if probe_url:
        livenessProbe:
          exec:
            command:
            - curl
            - ${probe_url}
          initialDelaySeconds: 120
          periodSeconds: 10
        %endif
        # additional container spec begins
        %for spec in additional_container_spec:
${spec()}\
        %endfor
        # additional container spec ends
        env:
        - name: RUN_MODE
          value: ${run_mode}
        - name: SANIC_DOMAIN
          value: ${sanic_domain}
        - name: CLUSTER_ID
          value: ${cluster_id}
        resources:
          limits:
            %if limit_mem is not None:
            memory: ${limit_mem}
            %endif
            %if limit_cpu is not None:
            cpu: ${limit_cpu}
            %endif
          requests:
            %if requested_mem is not None:
            memory: ${requested_mem}
            %endif
            %if requested_cpu is not None:
            cpu: ${requested_cpu}
            %endif
        %if len(ports) > 0:
        ports:
        %for port in ports:
        - containerPort: ${port.split(':')[1]}
        %endfor
        %endif
        %if has_volumes:  
        volumeMounts:
        %if run_mode == 'dev' and live_mount:
        - mountPath: /busride/linkedlib
          name: linked-lib
        - mountPath: /busride/services/${name.replace('-', '_')}
          name: service-livemount
        %endif
        %for volume in volumes:
        - mountPath: ${volume.split(':')[1]}
          name: ${volume.split(':')[1].replace('/', '-').replace('.', '-').replace('_', '-')[-63:].strip('-')}
        %endfor
        %endif
      %if has_volumes:
      volumes:
      %if run_mode == 'dev' and live_mount:
      - name: linked-lib
        hostPath:
          path: ${os.environ['SANIC_ROOT']}/registry.placeholder.com/linkedlib
      - name: service-livemount
        hostPath:
          path: ${os.environ['SANIC_ROOT']}/registry.placeholder.com/services/${name.replace('-', '_')}
      %endif
      %for volume in volumes:
      - name: ${volume.split(':')[1].replace('/', '-').replace('.', '-').replace('_', '-')[-63:].strip('-')}
        hostPath:
          path: ${volume.split(':')[0]}
      %endfor
      %endif
---
%if len(ports) > 0:
kind: Service
apiVersion: v1
metadata:
  name: ${name}
  namespace: ${cluster_id}
spec:
  selector:
    app: ${name}
  ports:
  %for port in ports:
  - name: ${port.replace(':', '-')}
    port: ${port.split(':')[1]}
  %endfor
%endif
</%def>\

${service(
    name="web",
    label="generic.busride.com",
    ports=("80:80",),
    #probe_url="localhost:80/ping",
)}
${service(
    name="api",
    label="generic.busride.com",
    ports=("80:80",),
    #probe_url="localhost:80/ping",
)}

% for name, service_host in (('redis', 'redis-ha'), ('mongo', 'mongo-mongodb'), ('sql', 'sql-postgresql-headless')):
---
kind: Service
apiVersion: v1
metadata:
  name: ${name}
  namespace: ${cluster_id}
spec:
  type: ExternalName
  externalName: ${service_host}.infra.svc.cluster.local
% endfor
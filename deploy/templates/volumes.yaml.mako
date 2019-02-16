<%!
    import os
    import subprocess
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../values/volumes.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
    hostname = subprocess.check_output('hostname').lower()
%>\

kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: Immediate

% if run_mode != 'prod':
% for i in range(3): # TODO: make dynamic
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-${i}
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local
  local:
    path: /data/busride/${i}
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - ${hostname}
% endfor
% endif
<%!
    import os
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../built/ingress.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
    sanic_domain = os.getenv('SANIC_DOMAIN')
    if sanic_domain is None:
      raise Exception('You must set the SANIC_DOMAIN variable to one of prod, dev, or test!')
    busride_domain = 'local.busride.network' if 'local' in sanic_domain else 'www.busride.network'
    cluster_id = os.getenv('CLUSTER_ID')
    if cluster_id is None:
      if run_mode == 'dev':
        cluster_id = 'cluster-dev'
      else:
        raise Exception('You must set the CLUSTER_ID variable! Try CLUSTER_ID=[...] [command]!')
%>\
---
## main web ingress
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: busride-ingress
  namespace: ${cluster_id}
spec:
  tls:
  - hosts:
    - ${sanic_domain}
    secretName: busride-tls
  rules:
  - host: ${sanic_domain}
    http:
      paths:
      - path: /
        backend:
          serviceName: web
          servicePort: 80
      - path: /api
        backend:
          serviceName: api
          servicePort: 80
---

## Basic auth endpoint for api/admin_login: used for sanic logs
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: admin-auth
  namespace: ${cluster_id}
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required"
spec:
  tls:
  - hosts:
    - ${sanic_domain}
    secretName: busride-tls
  rules:
  - host: ${sanic_domain}
    http:
      paths:
      - path: /admin
        backend:
          serviceName: admin
          servicePort: 80
      - path: /api/admin
        backend:
          serviceName: admin
          servicePort: 80

---
% if run_mode == 'prod':
apiVersion: certmanager.k8s.io/v1alpha1
kind: Certificate
metadata:
  name: busride
  namespace: ${cluster_id}
spec:
  secretName: busride-tls
  issuerRef:
    name: letsencrypt
    kind: ClusterIssuer
  commonName: ${sanic_domain}
  acme:
    config:
    - http01:
        ingressClass: nginx
      domains:
      - ${sanic_domain}
---
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:
  name: letsencrypt
  namespace: ${cluster_id}
spec:
  acme:
    email: hello@busride.com
    privateKeySecretRef:
      name: letsencrypt
    http01: {}
---
% endif

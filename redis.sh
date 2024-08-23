#!/usr/bin/env bash


kubectl exec -it c-skc-redis62-m-0 -c mgmt -- /bin/bash -c 'redis-cli -p 6379 --default skc -a pass'
kubectl exec -it c-skc-redis62new-m-0 -c mgmt -- /bin/bash -c 'redis-cli -p 6379 --user skc -a pass'
kubectl exec -it c-skc-redis62new-m-0 -c mgmt -- /bin/bash -c 'redis-cli -p 6379 --user skc -a pass'
kubectl exec -it c-skc-redis62new-m-0 -c mgmt -- /bin/bash -c 'redis-cli -p 6379 --user skc -a pass'
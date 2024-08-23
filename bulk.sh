icdctl fs redis | awk 'NR > 1 {print $2,$4}' | while read -r formation version; 
do
    echo "Namespace: $formation, Version: $version"
    icdctl f $formation
    pods=$(icdctl pods | grep leader | awk '{print $1}')

    kubectl cp /Users/sanjeevchoubey/go/src/github.ibm.com/SANJEEV-Choubey/Redis-handson/bulk.py $pods:/tmp/bulk.py -c mgmt

    if [[ "$version" == "5"* ]]; then
        echo "For Redis 5"
        kubectl exec $pods -c mgmt -- /bin/sh -c 'cred=$(cdb execute redis get_credentials); python /tmp/bulk.py | redis-cli -a "$cred" --pipe'
    else
        echo "For Redis 6 or later"
        kubectl exec $pods -c mgmt -- /bin/sh -c 'cred=$(cdb execute redis get_credentials); python /tmp/bulk.py | redis-cli --user ibm-user --pass "$cred" --pipe'
    fi
done

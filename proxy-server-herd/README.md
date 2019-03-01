## Proxy Server Herd Application
## README

### Components

The organization and descriptions of the project files are listed below:

- main.py: contains the starting code for the proxy server herd application
- server.py: contains the server-side classes, namely `ProxyServerProtocol` and `ProxyServerFactory`, and their implementations
- client.py: contains the client-side classes, namely `ProxyClientProtocol` and `ProxyClientFactory`, and their implementations
- conf.py: contains the configuration information for the application to run; these include TCP port numbers, network topology, and Google API private key (removed from submission)
- utils.py: contains the error handling decorator for use with the message protocol error handlers

### How to Run

To start the server herd, use the following command:

```
python main.py [server name]
```

or follow the prompt after:

```
make run
```

where `[server name]` can be "Alford", "Ball", "Hamilton", "Holiday", or "Welsh" (given the current configuration file).

    var webSocket      = null;
    var last_tapped_id = 'never-tapped';
    var cy             = null;

    function openWSConnection(protocol, hostname, port, endpoint) {
        var webSocketURL = protocol + "://" + hostname + ":" + port + endpoint;
        console.log("openWSConnection::Connecting to: " + webSocketURL);
        try {
            webSocket = new WebSocket(webSocketURL);
            webSocket.onopen = function(openEvent) {
                console.log("WebSocket OPEN: " + JSON.stringify(openEvent, null, 4));
            };
            webSocket.onclose = function (closeEvent) {
                console.log("WebSocket CLOSE: " + JSON.stringify(closeEvent, null, 4));
            };
            webSocket.onerror = function (errorEvent) {
                console.log("WebSocket ERROR: " + JSON.stringify(errorEvent, null, 4));
            };
            webSocket.onmessage = function (messageEvent) {
                var wsMsg = messageEvent.data;
                console.log("WebSocket MESSAGE: " + wsMsg);
                if (wsMsg.indexOf("error") > 0) {
                    console.log("wsMsg.error: " + wsMsg.error);
                } else {
                    if (wsMsg.startsWith("key")) {
                       cy.add({
                          data: { id: wsMsg }
                          }   
                       );
                       cy.layout({
                          name: 'circle'
                       }).run();                      
                    }
                }
            };
        } catch (exception) {
            console.error(exception);
        }
    }

        cy = cytoscape({
        container: document.getElementById('cy'),
        elements: [
            // nodes
            { data: { id: 'a' }, 'position': {'x': 20, 'y': 20} },
            { data: { id: 'b' }, 'position': {'x': 40, 'y': 30} },
            { data: { id: 'c' } },
            { data: { id: 'open' } },  
            { data: { id: 'get newly named node' } },
            { data: { id: 'close' } },
            {
              data: {
                id: 'ab',
                source: 'a',
                target: 'b'
              }
            },
            {
              data: {
                id: 'cd',
                source: 'c',
                target: 'open'
              }
            },
            {
              data: {
                id: 'ef',
                source: 'get newly named node',
                target: 'close'
              }
            },
            {
              data: {
                id: 'ac',
                source: 'a',
                target: 'c'
              }
            },
            {
              data: {
                id: 'be',
                source: 'b',
                target: 'get newly named node'
              }
            }],
        /*layout: {
            name: 'preset'
        },*/    
        style: [
            {
                selector: 'node',
                style: {
                    shape: 'hexagon',
                    'background-color': 'red',
                    label: 'data(id)'
                }
            }]     
        });
        for (var i = 0; i < 10; i++) {
            cy.add({
                data: { id: 'node' + i }
                }
            );
            var source = 'node' + i;
            cy.add({
                data: {
                    id: 'edge' + i,
                    source: source,
                    target: (i % 2 == 0 ? 'a' : 'b')
                }
            });
        }
        cy.layout({
            name: 'preset'
        }).run();
        cy.on('tap', 'node', function(event) {
            var tapped_id = event.target.data('id');
            if (tapped_id == 'open') {
                openWSConnection('ws', '127.0.0.1', '8060', '/ws');
            } else if (tapped_id == 'close') {
                webSocket.close();
            } else if (tapped_id == 'get newly named node') {
                if (webSocket.readyState != WebSocket.OPEN) {
                    console.error("webSocket is not open: " + webSocket.readyState);
                }
                webSocket.send('key ' + last_tapped_id);
            } else {
                last_tapped_id = tapped_id;
                cy.add({
                    data: { id: tapped_id + ' JUST ONCE FOR EACH NODE AT THE MOMENT' }
                    }
                );
            }
            cy.layout({
                name: 'circle'
            }).run();  
        
        });

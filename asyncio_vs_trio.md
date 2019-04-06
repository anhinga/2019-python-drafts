## asyncio vs Trio

There were hopes that **asyncio** would be a nice high-quality platform for async needs. Apparently that turned out **not to be the case**:

https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/

http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/

---

It looks like **Trio** is the sane alternative to asyncio:

https://github.com/python-trio/trio

https://trio.readthedocs.io/en/latest/

As an alternative to the asyncio-based **websockets** library, it makes sense to use **Trio WebSocket**:

https://github.com/HyperionGray/trio-websocket

https://trio-websocket.readthedocs.io/en/latest/

---

An example of successful refactoring from asyncio+websockets to Trio+Trio WebSocket:

https://github.com/jsa-aerial/pyhanasu

("no more weird exceptions and no more hangs")

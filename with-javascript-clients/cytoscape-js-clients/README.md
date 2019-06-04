Exercises to have Cytoscape.js clients interacting via websockets with a Python server

Include `cytoscape.min.js` from Cytoscape 3.6.2 into this directory to run (see https://unpkg.com/cytoscape@3.6.2/dist/ ).
Replace in `index.html` and in the repository by `cytoscape.umd.js` for debugging purpoes.

Run by opening `index.html`

`version4.js` - very rudimentary functionality (I would just e-mail it to myself at this stage, but it turns out that Gmail hates Javascript attachments "for security reasons", so I am storing it here instead). This one interacts with https://github.com/anhinga/2019-python-drafts/tree/master/with-javascript-clients/trio-websocket-server

***

In some sense, using Cytoscape.js directly is better than using Dash Cytoscape (see a remark at the end of https://github.com/anhinga/2019-design-notes/blob/master/interactive-framework/History.md ).

But I don't have much experience with JavaScript (from looking at _JavaScript: The Good Parts_ book by Douglas Crockford JavaScript has a lot of rather awful traps one needs to avoid; at least I have this book to guide me).

Also the Cytoscape.js data structures are rather complicated. E.g. I tried to study `event` object I am getting in `version4.js` here: `cy.on('tap', 'node', function(event) { ...`

It turns out that it has cycles, so one can't just use `JSON.stringify(event)` out of the box, and moreover it is so complicated that `JSON.stringify(JSON.decycle(event))` from https://github.com/douglascrockford/JSON-js/blob/master/cycle.js takes forever (it's not clear, if it would terminate at all).

The more straightforward `Cereal.stringify(event)` from https://github.com/atomizejs/cereal/blob/master/lib/cereal.js works instantly (kudos!), but the length of the resulting string representation of this object is about 200 thousand characters for this example. So it is a complicated nested object, and the idea to send it all to the Python side and process there is not necessarily all that attractive (one should really extract what matters and form a more compact object on the JavaScript side before sending it to a Python server).


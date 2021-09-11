/Users/feldman/packages/elm-xb/docs/index.html

game goals
- savage incisive word duels
  - understand your opponent
  - prepare your lexicon wisely
  - impale the enemy on sharp word combos
- encounter enemies and resources in a simple RPG environment
  - unlock new words and grammars
- pokemon-style combat layout

dev goals
- browser-based (ideally +mobile, -backend)
- use the elm architecture
  - event-driven, model-based
- develop collaboratively
  - hot reload from last model
  - 
  - git repo but import from master, then users (no merge conflicts)
- start with only python (inclusive)
  - first terminal view, then JS view over sockets

basic version
update
- 

event loop
 - 1: walking around
 - 2: interactive encounter (send choices to backend, receive content)
 - 3: combat (send choices to backend, receive content)
   - similar frontend structure to menu?

JS visuals
- render maps on backend, send to front

model
- entities
 - image, position, zorder
- nav map
- camera position

what about battle overlay?
can develop a view
- fixed port size to make life easy

how to work on this together?
- just learn how to use github branches

split front/back-end
- websockets can probably work in local/dev mode and online
- 3 kinds of changes
 - 1: front end
 - 2: back end
 - 3: content

content editing
- grammar, vocab from google sheets
- environment in harlowe?w

front end change
-> pull github
-> refresh browser (or use browser refresh plugin)
-> separate front-end repo?

back end change
-> flask app.run(debug=True) or env variable

content change
-> python watchdog? resend Content item


tech to setup
- see if drive works quickly for others
- pyte or another 
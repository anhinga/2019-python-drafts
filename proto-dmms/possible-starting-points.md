#### Scope

It is probably too early to try to implement the whole DMM pipeline along these lines:

https://github.com/anhinga/2019-design-notes

Instead I am thinking about experiments with possible parts of this pipeline 
(without much commitment, and trying to keep parts modular and replaceable).

#### Possible starting points

  * `initial_steps.md` in https://github.com/anhinga/2019-design-notes/tree/master/nexus 
    (various drafts related to "flat dmms", which can be both in NumPy and in PyTorch)

  * using a `node editor` with a setup similar to
    https://github.com/jsa-aerial/DMM/tree/master/examples/dmm/quil-controlled/interactive
    (it's fine to use a multilingual system and just to connect a node editor with
    the existing Clojure system at first, even if I'd like to have a Python system here
    eventually)
    
  * straightforward PyTorch experiments in the style of 
    https://github.com/anhinga/synapses/blob/master/regularization.md  
    and further plans I have in those directions.
    
  * experiments in the style of
    https://github.com/anhinga/2019-design-notes/tree/master/research-notes
    (including additional notes for June preprint)
    
  * machine learning experiments in the style of
    https://github.com/jsa-aerial/DMM/blob/master/design-notes/Early-2017/population-coordinate-descent.md
    (with index flattening used for visualization only, if at all)
    
I am going to start with https://github.com/anhinga/population-of-directions
    
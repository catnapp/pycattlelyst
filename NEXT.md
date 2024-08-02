# Whats next

> ### Disclaimer 
> The contents of this file is a fairly coherent stream of conscience brainstorm about different direction to take the design of this library, and intended to be documentation with accurate code examples that reflect how you would actually use the library. For that refer to `README.md`


## hard questions x hopefully some answers

### what should be the initial rules for the first iteration? how to decide?
- helps if the rule makes the stage gen process more simple
- should be enough complexity to be an interesting game

ok lets decide on which of these two rules to go ahead with

- cows teleport away after the fart - this makes the stage empty out over time
- cows don't go anywhere - this makes the stage stay the same over time and also:
  - infinite farts because cows just stay there
  - stage gen will be more complex because we now have to pepper cows that we need to fart-move the cows into the pens for a win. this means more possibilities to consider
  - could lead to an interesting mechanics chain

> 💡 reaction based mechanics? timing the fart properly

> building machines out of the systems. puzzle becomes how do you complete the machine. win condition based __rate__ of cows funnelled into pens



### can a world state be mapped to many distinct previous world states, or just one?
this one really depends on the rules


### should actions be included in states
yes. a world state w/o actions would be considered a stable state - these are states where players can act. while a state is unstable it'll need to be ran through the reducer some more
###
# NOTES

## goal 
defining the (unstructured) shape of the data containing the graph of states  previous to an input state, such that:

- and expectation test can be written checking the result from some __unsolver function__
- a hypothetical __unsolver function__ yielding an expected result is implementable (w/ as much practicality as reasonable)

these will be factors/principles guiding how we design the shape of our data and processes and other technical requirements

adhering to these design priniciples is what allows us to (agile?) our way through multiple iterations of this project, where on each iteration expect to flux around with rules of the system, breaking existing __unsolver function__ (we call this development 😉)

## discoveries

so here are some essential observations i made while exploring how to achieve the goal:

### defining heirarchy of states

we need to define the heirarchial order of states (or how each state proceeds one another) 

this heirarchial order needs to be defined in a flat way (list-like) because of there may be looped series of states causing the alternative non-flat way (tree-like/nested-object-like) to potentially infinitely long in some cases

flat way:
```json
{
  "e0dcd803580ee1a974f7e4fd192e12be": {
    "cows": [{ "id": "abe", "pos": [0, 2], "emo": "chilling" }]
  },
  "fcd584fe6dc5640124fdf69807777c72": {
    "next_state_uuid": "e0dcd803580ee1a974f7e4fd192e12be",
    "cows": [{ "id": "abe", "pos": [0, 1], "emo": "moving", "v": [0, 1] }]
  },
}
```

non-flat way:
```json
{
  "cows": [{ "id": "abe", "pos": [0, 2], "emo": "chilling" }],
  "prev_states": {
    "cows": [{ "id": "abe", "pos": [0, 1], "emo": "moving", "v": [0, 1] }],
    "prev_states": {
      "cows": [{ "id": "abe", "pos": [0, 2], "emo": "chilling" }],
      "prev_states": {
        /* ... */ /* here's where it can potentially get infinitely long for looped series of states */
      }     
    }
  }
}
```

we need uuids for states to reference them when defining the heirarchial order of states in a flat way

> uuids also help us identify these looped series

so the conclusion is that states need to be hashable to generate uuids for them


### problem w/ defining uuids for cows that are hypothesized into existance
for the purpose of defining the expected results for unit tests, we can arbitrarily assign ids/names for cows in an end state

```json
{
  "cows": [
    {
      "id": "abe",
      "pos": [0, 2],
      "emo": "chilling"
    }
  ]
}
```

however for cows that we add (retroactively) when we are hypothesizing previous states, what should we do about assigning this id? 

for QA-er, they can also arbitrarily assign these ids within the expected results, but if they're arbitrary then how would an implementor be able to assign the same ids so their result matches the expected results of the unit test? this approach violates our design principles, foiling and spoiling our ability to write a passable unit test

```json
{
  "next_state_uuid": "e0dcd803580ee1a974f7e4fd192e12be",
  "cows": [
    {
      "id": "abe",
      "pos": [0, 1],
      "emo": "chilling"
    },
    {
      "id": "dan", // would be unknownable to implementors
      "pos": [0, 2],
      "emo": "flatulating"
    }        
  ]
}
```

so whatever it is we use for the id of the cows and other entities of the state, it must be something knowable (or determinable) to the implementor - a convention must be established

#### approach #1 - hash of next state
one potential solution is to assign the hash of the next/proceeding state as the uuid for the hypothesized cow:

```json
{
  "next_state_uuid": "e0dcd803580ee1a974f7e4fd192e12be",
  "cows": {
    "abe": {
      "pos": [0, 1],
      "emo": "chilling"
    },
    "e0dcd803580ee1a974f7e4fd192e12be": { // hash of next state - this is knownable to implementors
      "pos": [0, 2],
      "emo": "flatulating"
    }        
  }
}
```

this works but limits us to only 1 hypothesized cow per state - what if the rules of our system support more?

#### approach #2 - hash of cow
one potential solution is to hash the hypothesized cow and assign that as it's uuid:
```json
{
  "next_state_uuid": "e0dcd803580ee1a974f7e4fd192e12be",
  "cows": {
    "abe": {
      "pos": [0, 1],
      "emo": "chilling"
    },
    "a94d522590f6326dfb24b1f020bb0f41": { // hash of hypothesized cow
      "pos": [0, 2],
      "emo": "flatulating"
    }        
  }
}
```

this works for the implementor - they can generate the hash for the uuid trivially

the downside however is there's a distinct possiblity that disparate states might hypothesize the same cow in the same `pos`/`emo` (just at different times), and as a result generate the same uuids and causing a collision

#### approach #3 - hash of next state + hash of cow
luckily for us it turns out that combining the first two approaches actually eliminates the issues present w/ each:

```json
{
  "next_state_uuid": "e0dcd803580ee1a974f7e4fd192e12be",
  "cows": {
    "abe": {
      "pos": [0, 1],
      "emo": "chilling"
    },
    "e0dcd803580ee1a974f7e4fd192e12be-a94d522590f6326dfb24b1f020bb0f41": { // hash of next state + hash of cow
      "pos": [0, 2],
      "emo": "flatulating"
    },
    "e0dcd803580ee1a974f7e4fd192e12be-81fcc6ea9d4973cfd6da51e06096c81c": { // hash of next state + hash of another cow
      "pos": [0, 0],
      "emo": "flatulating"
    }            
  }
}
```

but wait there seems to be a gap w/ this approach: what about when the state in which we're hypothesizing cows has more than 1 proceeding/next states?

```json
{
  "next_state_uuids": ["e0dcd803580ee1a974f7e4fd192e12be","__some_other_state_uuid__"],
  "cows": { 
    /* ... */
  }
}
```

> my conjecture is that any state that injects/hypotheszies (specifically flatulating) cows and other entities will have 1 and only 1 proceeding/next state

these states would be considered __transient states__, where thing is happening that must be resolved, and deterministically so, into 1 and only 1 proceeding/next state

and only __stable states__ can have many proceeding/next states - makes sense because these are states that players can _act_ upon. with these states the next state is multidimensional (like it's a wave function?)


### classifications of states

#### stable states

#### transient states

### defining unorderd lists in json - when ordering shouldn't matter for comparing equality

`.json` is the go-to format for the encoding state data, but one limitation it has to the ability to specify flavors of lists, such as one where the order does not matter. this is important for us because we're trying to compare the result from some implementation of the __unsolver function__ to an expected result in our unit test. in our expected result we have some lists where the order doesn't matter

to be clear the motivation is to avoid writing special logic doing the equality test. for example, since only some of the lists in a world state are unordered, we may need to write an entire `WorldState` class to specify this condition and facilitate the equality testing.

> is this more of a job for a custom `JSONDecoder`?

#### approach #1
one workaround is to use a dictionary w/ null values to basically define a `set` - this works currently for our use cases, but looking at it might take some getting used to

[explain more]

```json
{
  "next_state_by_uuid": {"e0dcd803580ee1a974f7e4fd192e12be": null, "__some_other_state_uuid__": null},
  "cows": { 
    /* ... */
  }
}
```

perhaps tweaking the naming will make it look less hacky and just a bit weird?

```json
{
  "next_state_accessiblity_by_uuid": {"e0dcd803580ee1a974f7e4fd192e12be": true, "__some_other_state_uuid__": true},
  "cows": { 
    /* ... */
  }
}
```

#### approach #2

another way to go about is just to establish a convention where we expect these lists to be sorted by the QA'er and implementor

[explain more]



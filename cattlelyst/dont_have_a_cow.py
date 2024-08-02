def generate_past_world_state_by_uuid(end_state, tiles):
    raise NotImplementedError

def generate_immediate_past_world_states(current_world_state):
    raise NotImplementedError


# const mapToPrevStates = (state) => mods.flatMap(m => m.mapToPrevStates(state))

# shotMod = {}
# shotMod.mapToPrevStates = (state) => {
#     if(isPlayerEventState(state)) {
#         // look for shots and simply remove them and that's the prev state
#         prevState = I.setIn(state, 'shots', [])
#     }else{
#         // look for moving cows
#         movingCows = state.cows.filter(c => c.move)
#         shots = movingCows.map(mapMovingCowToShot(state))
#         // for each moving cow, place shot behind movement and make cow chilling
#         prevState = {...state, shots}
#     }
# }

# shotMod.mapMovingCowToShot = (state) => (cow) {
#     cowToShot = c.move.map(v => -v) // behind the movement vector
#     pos = c.pos + cowToShot

#     if(hasCell(state,pos) && !hasCow(state,pos)) { // if the cell exists and it's cowless/empty-ish
#         return {pos}
#     }

# }


# coreMod = {}
# coreMod.mapToPrevStates = (state) => {
#     if(isStableState(state)) {
#         // for each cow, generate prev states where cow moves from adjacent cells
#         return state.cows.flatMap(
#             c => mapToPrevStatesIfCowMovedFromAdjacentCell(c, state)
#         )
#     }else{
#         return []
#     }
# }

# mapToPrevStatesIfCowMovedFromAdjacentCell = (cow, state) => {
#     adjacentCells = mapToAdjacentCells(state, cow.pos)
#     prevStates = adjacentCells.filter(noHasCow(state)).map(pos => {
#         prevState = I.clone(state)
#         prevCow = {...cow, pos, move: cow.pos - pos}
#         I.setIn(prevState.cows, `[{cow.index}]`, prevCow)
#     }
#     return prevStates
# }
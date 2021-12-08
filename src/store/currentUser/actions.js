export function saveTokenAction ({ commit, state }, payload) {
  commit('saveTokenMutation', payload.token)
}

export function saveUserAction ({ commit, state }, payload) {
  commit('saveUserMutation', payload.user)
}

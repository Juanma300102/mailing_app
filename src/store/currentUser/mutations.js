export function saveTokenMutation (state, token) {
  state.sessionToken = token
}

export function saveUserMutation (state, user) {
  state.currentUser = user
}

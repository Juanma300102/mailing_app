export function getSessionToken (state) {
  return state.sessionToken
}

export function getCurrentUserName (state) {
  return `${state.currentUser.nombre} ${state.currentUser.apellido}`
}

export function getCurrentUserEmail (state) {
  return state.currentUser.correo
}

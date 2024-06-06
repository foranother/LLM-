const BASE_TOKEN = import.meta.env.VITE_BASE_TOKEN_STORAGE_NAME
const BASE_USER = import.meta.env.VITE_BASE_USER_STORAGE_NAME

export default {
  isLoggedIn() {
    return localStorage.getItem(BASE_TOKEN) != undefined
  },
  setToken(token) {
    localStorage.setItem(BASE_TOKEN, token)
  },
  getToken(token) {
    return localStorage.getItem(BASE_TOKEN, token)
  },
  deleteToken() {
    localStorage.clear(BASE_TOKEN)
  },
  setUser(user) {
    localStorage.setItem(BASE_USER, JSON.stringify(user))
  },
  getUser() {
    try {
      return JSON.parse(localStorage.getItem(BASE_USER))
    } catch (e) {
      return null
    }
  },
  deleteUser() {
    localStorage.clear(BASE_USER)
  },
  logout() {
    this.deleteToken()
    this.deleteUser()
  }
}

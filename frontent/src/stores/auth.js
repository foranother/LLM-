import { defineStore } from 'pinia'
import { getAuth, onAuthStateChanged } from "firebase/auth"
import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import auth from '@/utils/auth'
import { useRouter } from 'vue-router'



export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null
  }),
  getters: {
    // doubleCount: (state) => state.count * 2
  },
  actions: {
    logout() {
      const firebaseAuth = getAuth()
      auth.logout()
      return firebaseAuth.signOut().then(()=>{
        this.setUser(null)
        return
      })
  },
    updateToken() {
        const firebaseAuth = getAuth()
        if(auth.isLoggedIn()) {
          const unsub = onAuthStateChanged(firebaseAuth, (user) => {
            if (user) {
                firebaseAuth.currentUser.getIdToken().then(token=>{
                    auth.setToken(token)
                })
                this.setUser(user)
            } else {
                // User is signed out
                // ...
                  auth.logout()
                  location.reload()
            }
            unsub()
            })
        }
    },
    login(){
      const firebaseAuth = getAuth()
      const provider = new GoogleAuthProvider();
      return signInWithPopup(firebaseAuth, provider)
          .then((result) => {
              // This gives you a Google Access Token. You can use it to access the Google API.
              // The signed-in user info
              const user = result.user

              user.getIdToken().then(token=>{
                  auth.setToken(token)
              })
              this.setUser(user)
              return result;
          })
    },
    setUser(user) {
      this.user = user
      auth.setUser(user)
    },
    isLoggedIn() {
        return this.user != null
    }
  }
})
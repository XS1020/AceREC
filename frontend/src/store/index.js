import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    login: !!localStorage.getItem('authorization'),
    localId: localStorage.getItem('localId'),
    remoteId: localStorage.getItem('remoteId'),
    userName: localStorage.getItem('username'),
    authorization: localStorage.getItem('authorization') ? localStorage.getItem('authorization') : ''
  },
  mutations: {
    changeLogin (state, user) {
      state.authorization = user.authorization
      localStorage.setItem('authorization', user.authorization)
      localStorage.setItem('username', user.userName)
      localStorage.setItem('localId', user.localId)
      localStorage.setItem('remoteId', user.remoteId)
      state.login = true
      state.localId = user.localId
      state.remoteId = user.remoteId
      state.userName = user.userName
    },
    logout (state) {
      state.authorization = ""
      state.login = false
      state.remoteId = state.localId = ""
      state.userName = ""
      localStorage.removeItem('authorization')
      localStorage.removeItem('username')
      localStorage.removeItem('localId')
      localStorage.removeItem('remoteId')
    }
  },
  actions: {
  },
  modules: {
  }
})

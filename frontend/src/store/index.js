import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    login: !!localStorage.getItem('authorization'),
    localId: localStorage.getItem('localId'),
    remoteId: 0,
    userName: localStorage.getItem('username'),
    authorization: localStorage.getItem('authorization') ? localStorage.getItem('authorization') : ''
  },
  mutations: {
    changeLogin (state, user) {
      state.authorization = user.authorization
      localStorage.setItem('authorization', user.authorization)
      localStorage.setItem('username', user.userName)
      localStorage.setItem('localId', user.localId)
      state.login = true
      state.localId = user.localId
      state.remoteId = user.remoteId
      state.userName = user.userName
    },
    logout (state) {
      state.authorization = ""
      state.login = false
      state.remoteId = state.localId = 0
      state.userName = ""
      localStorage.removeItem('authorization')
      localStorage.removeItem('username')
      localStorage.removeItem('localId')
    }
  },
  actions: {
  },
  modules: {
  }
})

import axios from 'axios'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
function clearToken () {
    localStorage.removeItem('authorization')
    localStorage.removeItem('username')
    localStorage.removeItem('localId')
}
const request = (config) => {
    const axiosInstance = axios.create({
        timeout: 100000
    })
    axiosInstance.interceptors.request.use(config  => {
        if (localStorage.getItem('authorization')) {
            config.headers.token = localStorage.getItem('authorization')
            config.headers.username = localStorage.getItem('username')
        }
        return config
    }, error => {
        switch (error.response.status) {
            case 401:
                clearToken()
                this.store.state.login = false
                break
            case 403:
                clearToken()
                break
        }
        return Promise.reject(error)
    })
    return axiosInstance(config)
}
export default request
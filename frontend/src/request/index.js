import axios from 'axios'
const baseURL = "http://192.168.3.75:8008"
const request = (config) => {
    const axiosInstance = axios.create({
        baseURL: baseURL,
        timeout: 1000
    })
    return axiosInstance(config)
}
export default request
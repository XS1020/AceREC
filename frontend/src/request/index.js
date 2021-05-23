import axios from 'axios'
const request = (config) => {
    const axiosInstance = axios.create({
        timeout: 5000
    })
    return axiosInstance(config)
}
export default request
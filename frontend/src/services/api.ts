import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (
            axios.isAxiosError(error) &&
            error.response?.status === 401
        ) {
            sessionStorage.removeItem('stockwise_token')

            window.dispatchEvent(
                new Event('stockwise:unauthorized')
            )
        }

        return Promise.reject(error)
    }
)

export default api
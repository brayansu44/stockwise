import {
    createContext,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from 'react'

interface AuthContextType {
    token: string | null
    isAuthenticated: boolean
    login: (accessToken: string) => void
    logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(
    undefined
)

export function AuthProvider({
    children,
}: {
    children: ReactNode
}) {
    const [token, setToken] = useState<string | null>(() => {
        return sessionStorage.getItem('stockwise_token')
    })

    const login = (accessToken: string) => {
        sessionStorage.setItem('stockwise_token', accessToken)
        setToken(accessToken)
    }

    const logout = () => {
        sessionStorage.removeItem('stockwise_token')
        setToken(null)
    }

    useEffect(() => {
        function handleUnauthorized() {
            setToken(null)
            sessionStorage.removeItem('stockwise_token')
        }

        window.addEventListener(
            'stockwise:unauthorized',
            handleUnauthorized
        )

        return () => {
            window.removeEventListener(
                'stockwise:unauthorized',
                handleUnauthorized
            )
        }
    }, [])

    return (
        <AuthContext.Provider
            value={{
                token,
                isAuthenticated: Boolean(token),
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)

    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }

    return context
}
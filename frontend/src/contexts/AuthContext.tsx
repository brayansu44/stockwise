import {
    createContext,
    useContext,
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
    const [token, setToken] = useState<string | null>(null)

    const login = (accessToken: string) => {
        setToken(accessToken)
    }

    const logout = () => {
        setToken(null)
    }

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
import {
    createContext,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from 'react'
import type { User } from '../types/user'
import { authService } from '../services/authService'

interface AuthContextType {
    token: string | null
    user: User | null
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

    const [user, setUser] = useState<User | null>(null)

    useEffect(() => {
        let cancelled = false

        async function loadUser() {
            if (!token) {
                setUser(null)
                return
            }

            try {
                const currentUser = await authService.getMe(token)

                if (!cancelled) {
                    setUser(currentUser)
                }
            } catch {
                if (!cancelled) {
                    setUser(null)
                }
            }
        }

        loadUser()

        return () => {
            cancelled = true
        }
    }, [token])

    const login = (accessToken: string) => {
        sessionStorage.setItem('stockwise_token', accessToken)
        setToken(accessToken)
    }

    const logout = () => {
        sessionStorage.removeItem('stockwise_token')
        setToken(null)
        setUser(null)
    }

    useEffect(() => {
        function handleUnauthorized() {
            setToken(null)
            setUser(null)
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
                user,
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
import { useState, type FormEvent } from 'react'
import { authService } from '../services/authService'
import { useNavigate } from 'react-router'
import { useAuth } from '../contexts/AuthContext'

export default function LoginPage() {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()
    const { login } = useAuth()

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        setError('')
        setLoading(true)

        try {
            const response = await authService.login({
                email,
                password,
            })

            login(response.access_token)
            navigate('/dashboard')
        } catch {
            setError('Invalid credentials or connection error')
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
            <section className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">
                <h1 className="mb-2 text-center text-3xl font-bold text-blue-400">
                    StockWise
                </h1>

                <p className="mb-8 text-center text-slate-400">
                    Sign in to your account
                </p>

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label
                            htmlFor="email"
                            className="mb-2 block text-sm font-medium text-slate-300"
                        >
                            Email
                        </label>

                        <input
                            id="email"
                            type="email"
                            placeholder="you@example.com"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="password"
                            className="mb-2 block text-sm font-medium text-slate-300"
                        >
                            Password
                        </label>

                        <input
                            id="password"
                            type="password"
                            placeholder="Enter your password"
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:opacity-50"
                    >
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>

                    {error && (
                        <p role="alert" className="text-center text-sm text-red-400">
                            {error}
                        </p>
                    )}
                </form>
            </section>
        </main>
    )
}
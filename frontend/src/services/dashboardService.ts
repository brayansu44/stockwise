import api from './api'
import type { DashboardSummary } from '../types/dashboard'

export const dashboardService = {
    async getSummary(token: string): Promise<DashboardSummary> {
        const response = await api.get<DashboardSummary>(
            '/dashboard/summary',
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },
}
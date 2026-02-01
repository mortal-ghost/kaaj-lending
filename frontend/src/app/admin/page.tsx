"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import axios from "axios"
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

type Application = {
    id: number
    business_name: string
    amount_requested: number
    status: string
    created_at: string
    fico_score: number
}

export default function AdminDashboard() {
    const [applications, setApplications] = useState<Application[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // In a real app, this would be a server component or use SWR/React Query.
        // Keeping it simple with useEffect for MVP.
        const fetchApps = async () => {
            try {
                // Mocking the get all endpoint if it doesn't exist yet, but assuming standard REST
                // If /applications/ doesn't return a list, we might need to adjust the backend.
                // Based on implementation plan, GET /api/applications/{id} exists, need to verify list endpoint.
                // Assuming GET /api/applications/ returns list based on standard conventions.
                const res = await axios.get("http://127.0.0.1:8000/api/applications?limit=50")
                setApplications(res.data)
            } catch (error) {
                console.error("Failed to fetch applications", error)
            } finally {
                setLoading(false)
            }
        }
        fetchApps()
    }, [])

    return (
        <div className="container mx-auto py-10">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
                <Button asChild>
                    <Link href="/apply">Create New App</Link>
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Applications</CardTitle>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="text-center py-10">Loading applications...</div>
                    ) : (
                        <Table>
                            <TableCaption>A list of recent loan applications.</TableCaption>
                            <TableHeader>
                                <TableRow>
                                    <TableHead className="w-[100px]">ID</TableHead>
                                    <TableHead>Business Name</TableHead>
                                    <TableHead>Amount</TableHead>
                                    <TableHead>FICO</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Action</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {applications.length === 0 && (
                                    <TableRow>
                                        <TableCell colSpan={6} className="text-center py-10 text-muted-foreground">
                                            No applications found.
                                        </TableCell>
                                    </TableRow>
                                )}
                                {applications.map((app) => (
                                    <TableRow key={app.id}>
                                        <TableCell className="font-medium">#{app.id}</TableCell>
                                        <TableCell>{app.business_name}</TableCell>
                                        <TableCell>${app.amount_requested.toLocaleString()}</TableCell>
                                        <TableCell>{app.fico_score}</TableCell>
                                        <TableCell>
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${app.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                                                    app.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                                                }`}>
                                                {app.status}
                                            </span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button variant="ghost" size="sm" asChild>
                                                <Link href={`/applications/${app.id}`}>View</Link>
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    )
}

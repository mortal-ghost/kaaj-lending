"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import Link from "next/link"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, CheckCircle2, XCircle } from "lucide-react"

type MatchResult = {
    lender_name: string
    policy_name: string
    eligible: boolean
    reasons: string[]
    score: number
}

type Application = {
    id: number
    business_name: string
    amount_requested: number
    status: string
    fico_score: number
    years_in_business: number
    annual_revenue: number
    equipment_type: string
    city: string
    state: string
}

export default function ApplicationResults() {
    const params = useParams()
    const id = params?.id
    const [application, setApplication] = useState<Application | null>(null)
    const [matches, setMatches] = useState<MatchResult[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!id) return

        const fetchData = async () => {
            try {
                const [appRes, matchRes] = await Promise.all([
                    axios.get(`http://127.0.0.1:8000/api/applications/${id}`),
                    axios.get(`http://127.0.0.1:8000/api/applications/${id}/matches`),
                ])
                setApplication(appRes.data)
                setMatches(matchRes.data)
            } catch (error) {
                console.error("Failed to fetch data", error)
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [id])

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                Loading results...
            </div>
        )
    }

    if (!application) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                Application not found.
            </div>
        )
    }

    return (
        <div className="container mx-auto py-10 space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <Link href="/admin" className="text-sm text-muted-foreground hover:underline mb-2 block">
                        &larr; Back to Dashboard
                    </Link>
                    <h1 className="text-3xl font-bold tracking-tight">{application.business_name}</h1>
                    <p className="text-muted-foreground">
                        {application.city}, {application.state} • ${application.amount_requested.toLocaleString()} requested
                    </p>
                </div>
                <div className="text-right">
                    <span className={`inline-flex items-center px-4 py-1.5 rounded-full text-sm font-medium ${application.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                            application.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                        {application.status}
                    </span>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
                {/* Application Details Summary */}
                <Card className="md:col-span-1 h-fit">
                    <CardHeader>
                        <CardTitle>Application Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex justify-between border-b pb-2">
                            <span className="text-muted-foreground">FICO Score</span>
                            <span className="font-medium">{application.fico_score}</span>
                        </div>
                        <div className="flex justify-between border-b pb-2">
                            <span className="text-muted-foreground">Years in Business</span>
                            <span className="font-medium">{application.years_in_business}</span>
                        </div>
                        <div className="flex justify-between border-b pb-2">
                            <span className="text-muted-foreground">Revenue</span>
                            <span className="font-medium">${application.annual_revenue.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between pt-2">
                            <span className="text-muted-foreground">Equipment</span>
                            <span className="font-medium">{application.equipment_type}</span>
                        </div>
                    </CardContent>
                </Card>

                {/* Matching Results */}
                <div className="md:col-span-2 space-y-4">
                    <h2 className="text-xl font-semibold">Lender Matches</h2>
                    {matches.length === 0 && (
                        <p className="text-muted-foreground">No matches found yet. Run the matching engine.</p>
                    )}
                    {matches.map((match, idx) => (
                        <Card key={idx} className={`transition-all ${match.eligible ? 'border-green-200 bg-green-50/10' : 'opacity-80'}`}>
                            <CardContent className="p-6">
                                <div className="flex items-start justify-between">
                                    <div className="flex gap-4">
                                        {match.eligible ? (
                                            <CheckCircle2 className="mt-1 h-6 w-6 text-green-500" />
                                        ) : (
                                            <XCircle className="mt-1 h-6 w-6 text-muted-foreground" />
                                        )}
                                        <div>
                                            <h3 className="text-lg font-bold">{match.lender_name}</h3>
                                            <p className="text-sm text-muted-foreground">{match.policy_name}</p>

                                            {!match.eligible && (
                                                <div className="mt-3 space-y-1">
                                                    {match.reasons.map((reason, rIdx) => (
                                                        <p key={rIdx} className="text-sm text-destructive flex items-center gap-2">
                                                            <AlertCircle className="h-4 w-4" /> {reason}
                                                        </p>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                    <div>
                                        {match.eligible ? (
                                            <div className="text-right">
                                                <span className="font-bold text-green-600">Matched</span>
                                                {/* <p className="text-xs text-muted-foreground pt-1">Score: {match.score}</p> */}
                                            </div>
                                        ) : (
                                            <span className="text-sm font-medium text-muted-foreground">Ineligible</span>
                                        )}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    )
}

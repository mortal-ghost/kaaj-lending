"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    Select,
} from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from "next/navigation"

type FormData = {
    business_name: string
    amount_requested: number
    equipment_type: string
    fico_score: number
    years_in_business: number
    annual_revenue: number
    state: string
    city: string
    paynet_score?: number
}

export default function ApplicationForm() {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<FormData>()
    const router = useRouter()
    const [submitting, setSubmitting] = useState(false)

    const onSubmit = async (data: FormData) => {
        setSubmitting(true)
        try {
            const payload = {
                ...data,
                amount_requested: Number(data.amount_requested),
                fico_score: Number(data.fico_score),
                years_in_business: Number(data.years_in_business),
                annual_revenue: Number(data.annual_revenue),
                paynet_score: data.paynet_score ? Number(data.paynet_score) : null,
            }

            // We'll assume the backend is proxied or CORS enabled. 
            // For now hitting localhost:8000 directly.
            const res = await axios.post("http://127.0.0.1:8000/api/applications/", payload)
            router.push(`/applications/${res.data.id}`)
        } catch (e) {
            console.error(e)
            alert("Failed to submit application")
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
            <Card className="w-full max-w-2xl">
                <CardHeader>
                    <CardTitle>New Loan Application</CardTitle>
                    <CardDescription>
                        Enter your business details to find matching lenders.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                        <div className="grid gap-4 md:grid-cols-2">
                            <div className="col-span-2 space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    Business Name
                                </label>
                                <Input
                                    {...register("business_name", {
                                        required: "Business Name is required",
                                    })}
                                    placeholder="Acme Corp"
                                />
                                {errors.business_name && (
                                    <span className="text-xs text-destructive">
                                        {errors.business_name.message}
                                    </span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    Amount Requested ($)
                                </label>
                                <Input
                                    type="number"
                                    {...register("amount_requested", {
                                        required: "Amount is required",
                                        min: 0,
                                    })}
                                    placeholder="50000"
                                />
                                {errors.amount_requested && (
                                    <span className="text-xs text-destructive">
                                        {errors.amount_requested.message}
                                    </span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    Equipment Type
                                </label>
                                <Select {...register("equipment_type", { required: true })}>
                                    <option value="">Select...</option>
                                    <option value="Truck">Truck / Vehicle</option>
                                    <option value="Medical">Medical</option>
                                    <option value="Construction">Construction</option>
                                    <option value="IT">IT / Software</option>
                                    <option value="Other">Other</option>
                                </Select>
                                {errors.equipment_type && (
                                    <span className="text-xs text-destructive">Required</span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    FICO Score
                                </label>
                                <Input
                                    type="number"
                                    {...register("fico_score", {
                                        required: "FICO is required",
                                        min: 300,
                                        max: 850,
                                    })}
                                    placeholder="700"
                                />
                                {errors.fico_score && (
                                    <span className="text-xs text-destructive">
                                        {errors.fico_score.message}
                                    </span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    Years in Business
                                </label>
                                <Input
                                    type="number"
                                    step="0.1"
                                    {...register("years_in_business", {
                                        required: "Required",
                                    })}
                                    placeholder="2.5"
                                />
                                {errors.years_in_business && (
                                    <span className="text-xs text-destructive">
                                        {errors.years_in_business.message}
                                    </span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    Annual Revenue ($)
                                </label>
                                <Input
                                    type="number"
                                    {...register("annual_revenue", {
                                        required: "Required",
                                    })}
                                    placeholder="1000000"
                                />
                                {errors.annual_revenue && (
                                    <span className="text-xs text-destructive">
                                        {errors.annual_revenue.message}
                                    </span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    State
                                </label>
                                <Input
                                    {...register("state", {
                                        required: "Required",
                                        maxLength: 2,
                                    })}
                                    className="uppercase"
                                    placeholder="CA"
                                />
                                {errors.state && (
                                    <span className="text-xs text-destructive">
                                        {errors.state.message}
                                    </span>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    City
                                </label>
                                <Input
                                    {...register("city", { required: "Required" })}
                                    placeholder="San Francisco"
                                />
                                {errors.city && (
                                    <span className="text-xs text-destructive">
                                        {errors.city.message}
                                    </span>
                                )}
                            </div>
                        </div>

                        <Button type="submit" className="w-full" disabled={submitting}>
                            {submitting ? "Analyzing..." : "Submit Application"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}

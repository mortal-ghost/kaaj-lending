import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 font-[family-name:var(--font-inter)]">
      {/* Navigation */}
      <nav className="border-b bg-white">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2 font-bold text-xl text-slate-900">
            <span className="flex h-8 w-8 items-center justify-center rounded bg-blue-600 text-white">L</span>
            LenderMatch
          </div>
          <div className="flex gap-4">
            <Link href="/admin" className="text-sm font-medium text-slate-600 hover:text-slate-900">
              Admin
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20 text-center">
        <h1 className="mb-6 text-5xl font-extrabold tracking-tight text-slate-900 sm:text-6xl">
          Find the Perfect Lender <br className="hidden sm:inline" />
          <span className="text-blue-600">In Seconds</span>
        </h1>
        <p className="mx-auto mb-10 max-w-2xl text-lg text-slate-600">
          Our intelligent matching engine connects your business with the right financial partners based on your credit profile, industry, and revenue.
        </p>

        <div className="flex flex-col justify-center gap-4 sm:flex-row">
          <Button size="lg" className="h-12 w-full px-8 text-lg sm:w-auto" asChild>
            <Link href="/apply">Start Your Application</Link>
          </Button>
          <Button size="lg" variant="outline" className="h-12 w-full px-8 text-lg sm:w-auto" asChild>
            <Link href="/admin">View Dashboard</Link>
          </Button>
        </div>

        {/* Feature Grid */}
        <div className="mt-24 grid gap-8 sm:grid-cols-3">
          <div className="rounded-xl bg-white p-8 shadow-sm">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="mb-2 text-xl font-bold text-slate-900">Instant Matching</h3>
            <p className="text-slate-600">Get matched with lenders immediately after submitting your basic information.</p>
          </div>
          <div className="rounded-xl bg-white p-8 shadow-sm">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="mb-2 text-xl font-bold text-slate-900">Pre-Qualified</h3>
            <p className="text-slate-600">We check lender policies against your data to ensure high approval odds.</p>
          </div>
          <div className="rounded-xl bg-white p-8 shadow-sm">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="mb-2 text-xl font-bold text-slate-900">Secure & Private</h3>
            <p className="text-slate-600">Your data is encrypted and only shared with matches you approve.</p>
          </div>
        </div>
      </main>
    </div>
  );
}

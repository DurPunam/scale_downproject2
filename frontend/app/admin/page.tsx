import { Button } from "@/components/ui/button";

export default function AdminPage() {
  return (
    <main className="mx-auto max-w-5xl px-6 py-10">
      <h1 className="text-2xl font-semibold">Admin / Model Ops</h1>
      <p className="mt-2 text-slate-300">
        Feature flags, model rollouts, and quality metrics.
      </p>
      <div className="mt-6">
        <Button variant="outline">Create Feature Flag</Button>
      </div>
    </main>
  );
}

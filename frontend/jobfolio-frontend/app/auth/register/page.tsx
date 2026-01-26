 "use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

 export default function RegisterPage() {
  const router = useRouter();
   const [fullName, setFullName] = useState("");
   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
   const [loading, setLoading] = useState(false);
   const [error, setError] = useState<string | null>(null);
   const [success, setSuccess] = useState<string | null>(null);

   const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
     event.preventDefault();
     setError(null);
     setSuccess(null);

     if (!fullName || !email || !password) {
       setError("Please fill out all fields.");
       return;
     }

     try {
       setLoading(true);
       const response = await fetch("/api/v1/auth/register", {
         method: "POST",
         headers: {
           "Content-Type": "application/json",
         },
         body: JSON.stringify({
           email,
           password,
           full_name: fullName,
         }),
       });

       if (!response.ok) {
         const data = await response.json().catch(() => null);
         const message =
           data?.detail || data?.message || "Registration failed. Try again.";
         throw new Error(message);
       }

       setSuccess("Account created. Redirecting...");
       router.push("/");
     } catch (err) {
       setError(err instanceof Error ? err.message : "Something went wrong.");
     } finally {
       setLoading(false);
     }
   };

   return (
     <main className="min-h-screen bg-slate-950 text-slate-100">
       <div className="mx-auto flex min-h-screen w-full max-w-6xl items-center justify-center px-4 py-16">
         <div className="grid w-full gap-10 lg:grid-cols-2">
           <section className="hidden flex-col justify-center gap-6 rounded-3xl border border-slate-800/80 bg-linear-to-br from-slate-900 to-slate-950 p-10 shadow-2xl lg:flex">
             <span className="inline-flex w-fit rounded-full border border-emerald-400/40 bg-emerald-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-emerald-200">
               JobFolio
             </span>
             <h1 className="text-3xl font-semibold leading-tight">
               Create your profile and start applying in minutes.
             </h1>
             <p className="text-sm text-slate-300">
               Build a polished job profile, track applications, and get matched
               with roles that fit you.
             </p>
             <div className="space-y-3 text-sm text-slate-300">
               <div className="flex items-center gap-3">
                 <span className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-800 text-emerald-300">
                   1
                 </span>
                 <span>Showcase your experience in one place.</span>
               </div>
               <div className="flex items-center gap-3">
                 <span className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-800 text-emerald-300">
                   2
                 </span>
                 <span>Keep applications organized automatically.</span>
               </div>
               <div className="flex items-center gap-3">
                 <span className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-800 text-emerald-300">
                   3
                 </span>
                 <span>Receive curated role recommendations.</span>
               </div>
             </div>
           </section>

           <section className="flex items-center">
             <div className="w-full rounded-3xl border border-slate-800/80 bg-slate-900/70 p-8 shadow-xl backdrop-blur">
               <div className="mb-8 space-y-2">
                 <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
                   Create account
                 </p>
                 <h2 className="text-2xl font-semibold text-white">
                   Register for JobFolio
                 </h2>
                 <p className="text-sm text-slate-400">
                   Use your email address to get started.
                 </p>
               </div>

               <form className="space-y-5" onSubmit={handleSubmit}>
                 <div className="space-y-2">
                   <label
                     className="text-xs font-semibold uppercase tracking-wider text-slate-400"
                     htmlFor="fullName"
                   >
                     Full name
                   </label>
                   <input
                     id="fullName"
                     type="text"
                     autoComplete="name"
                     value={fullName}
                     onChange={(event) => setFullName(event.target.value)}
                     className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                     placeholder="Jane Doe"
                   />
                 </div>

                 <div className="space-y-2">
                   <label
                     className="text-xs font-semibold uppercase tracking-wider text-slate-400"
                     htmlFor="email"
                   >
                     Email
                   </label>
                   <input
                     id="email"
                     type="email"
                     autoComplete="email"
                     value={email}
                     onChange={(event) => setEmail(event.target.value)}
                     className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                     placeholder="you@email.com"
                   />
                 </div>

                 <div className="space-y-2">
                   <label
                     className="text-xs font-semibold uppercase tracking-wider text-slate-400"
                     htmlFor="password"
                   >
                     Password
                   </label>
                   <input
                     id="password"
                     type="password"
                     autoComplete="new-password"
                     value={password}
                     onChange={(event) => setPassword(event.target.value)}
                     className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                     placeholder="Create a secure password"
                   />
                 </div>

                 {error ? (
                   <p className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
                     {error}
                   </p>
                 ) : null}

                 {success ? (
                   <p className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
                     {success}
                   </p>
                 ) : null}

                 <button
                   type="submit"
                   disabled={loading}
                   className="w-full rounded-xl bg-emerald-500 px-4 py-3 text-sm font-semibold text-emerald-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-70"
                 >
                   {loading ? "Creating account..." : "Create account"}
                 </button>
               </form>

               <p className="mt-6 text-sm text-slate-400">
                 Already have an account?{" "}
                 <a
                   className="font-semibold text-emerald-300 hover:text-emerald-200"
                   href="/auth/login"
                 >
                   Sign in
                 </a>
               </p>
             </div>
           </section>
         </div>
       </div>
     </main>
   );
 }

"use client";

import { signIn } from "next-auth/react";

export default function Login() {
  return (
    <div className="min-h-screen bg-linear-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white/10 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 text-center">
        <h1 className="text-4xl font-extrabold mb-2 bg-linear-to-r from-blue-200 to-pink-200 bg-clip-text text-transparent">
          Welcome
        </h1>
        <p className="text-gray-300 mb-8">
          Sign in to access the ATS Resume Evaluator
        </p>

        <button
          onClick={() => signIn("google")}
          className="w-full py-4 px-6 rounded-xl font-bold text-white bg-white/20 hover:bg-white/30 transition-all duration-200 flex items-center justify-center gap-3 group"
        >
          <svg className="w-5 h-5 text-white group-hover:scale-110 transition-transform" viewBox="0 0 24 24" fill="currentColor">
             <path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 0.507 5.387 0 12s5.36 12 12.48 12c3.6 0 6.613-1.2 8.4-3.413 1.84-2.293 2.293-5.307 2.293-6.96 0-.667-.053-1.307-.16-1.707h-10.533z" />
          </svg>
          Sign in with Google
        </button>
      </div>
    </div>
  );
}

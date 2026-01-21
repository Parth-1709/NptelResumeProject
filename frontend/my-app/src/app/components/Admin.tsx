"use client";

import { useEffect, useState } from "react";
import api from "@/src/app/api/users/api";
import { signOut } from "next-auth/react";

interface Stats {
  total_users: number;
  avg_score: number;
  top_missing_skills: string[];
}

export default function Admin() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    api.get("/admin/stats").then((res) => {
      setStats(res.data);
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="flex justify-between items-center bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-700">
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-purple-400">
            Admin Dashboard
          </h1>
          <button
            onClick={() => signOut()}
            className="px-4 py-2 bg-red-500/10 text-red-400 rounded-lg hover:bg-red-500/20 transition-colors"
          >
            Sign Out
          </button>
        </header>

        {stats ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Stat Card 1 */}
            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl">
              <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Total Users</h3>
              <p className="text-5xl font-bold text-white">{stats.total_users}</p>
            </div>

            {/* Stat Card 2 */}
            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl">
              <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Average Score</h3>
              <div className="flex items-end gap-2">
                <p className="text-5xl font-bold text-green-400">{stats.avg_score}</p>
                <span className="text-gray-400 mb-2">/ 100</span>
              </div>
            </div>

            {/* Stat Card 3 */}
            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl">
              <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-4">Top Missing Skills</h3>
              <div className="space-y-2">
                {stats.top_missing_skills.map((skill) => (
                  <div key={skill} className="flex items-center gap-3 text-gray-300">
                    <span className="w-2 h-2 rounded-full bg-red-400"></span>
                    {skill}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">Loading stats...</div>
        )}
      </div>
    </div>
  );
}

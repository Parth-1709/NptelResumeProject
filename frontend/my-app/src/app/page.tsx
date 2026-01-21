"use client";

import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import Login from "@/src/app/components/Login";
import Admin from "@/src/app/components/Admin";
import User from "@/src/app/components/User";
import api from "@/src/app/api/users/api";
import { signOut } from "next-auth/react";

export default function Home() {
  const { data: session, status } = useSession();
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    if (status === "authenticated" && session?.user?.email && !role) {
      api
        .post("/verify-user", {
          email: session.user.email,
          name: session.user.name || "Unknown",
        })
        .then((res) => {
          setRole(res.data.role);
        })
        .catch((err) => {
          console.error("Verification failed", err);
          alert("User verification failed. Please try again.");
          signOut(); 
        });
    }
  }, [status, session, role]);

  if (status === "loading" || (status === "authenticated" && !role)) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (status === "unauthenticated") {
    return <Login />;
  }

  if (role === "admin") {
    return <Admin />;
  }

  if (role === "user") {
    return <User />;
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center text-white">
      Preparing your experience...
    </div>
  );
}

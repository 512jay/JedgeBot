// /frontend/src/pages/VerifyEmail.jsx

import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("verifying");
  const navigate = useNavigate();

  useEffect(() => {
    const verify = async () => {
      const token = searchParams.get("token");
  
      if (!token) {
        setStatus("missing");
        toast.error("Verification token is missing.");
        return;
      }
  
      try { 
        const res = await fetch(`/auth/verify-email?token=${token}`, {
          method: "GET",
        });
  
        if (res.ok) {
          setStatus("success");
          toast.success("✅ Email verified! Redirecting to login...");
          setTimeout(() => navigate("/login"), 3000);
        } else {
          const data = await res.json();
          throw new Error(data.detail || "Verification failed.");
        }
      } catch (err) {
        console.error(err);
        setStatus("error");
        toast.error(err.message || "Verification failed.");
      }
    };
  
    verify(); // Call the async function
  }, [searchParams, navigate]);
  

  return (
    <div className="text-center p-5">
      {status === "verifying" && <p>🔄 Verifying your email...</p>}
      {status === "missing" && (
        <p>
          ❌ Invalid verification link.{" "}
          <a href="/resend-verification">Resend verification</a>
        </p>
      )}
      {status === "success" && <p>✅ Email verified. Redirecting to login...</p>}
      {status === "error" && (
        <p>
          ❌ Email verification failed.{" "}
          <a href="/resend-verification">Try again</a>
        </p>
      )}
    </div>
  );
}

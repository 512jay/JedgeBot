import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("verifying");
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setStatus("missing");
      toast.error("Verification token is missing.");
      return;
    }

    fetch(`/auth/verify-email?token=${token}`, {
      method: "POST",
    })
      .then(async (res) => {
        if (res.ok) {
          setStatus("success");
          toast.success("Email verified! Redirecting to login...");
          setTimeout(() => navigate("/login"), 3000);
        } else {
          const data = await res.json();
          throw new Error(data.detail || "Verification failed.");
        }
      })
      .catch((err) => {
        console.error(err);
        setStatus("error");
        toast.error(err.message || "Verification failed.");
      });
  }, [searchParams, navigate]);

  return (
    <div className="text-center p-5">
      {status === "verifying" && <p>Verifying your email...</p>}
      {status === "missing" && (
        <p>
          Invalid verification link.{" "}
          <a href="/resend-verification">Resend verification</a>
        </p>
      )}
      {status === "success" && <p>Redirecting to login...</p>}
      {status === "error" && (
        <p>
          Email verification failed.{" "}
          <a href="/resend-verification">Try again</a>
        </p>
      )}
    </div>
  );
}

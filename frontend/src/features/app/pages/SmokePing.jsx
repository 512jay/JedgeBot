// /frontend/src/features/app/pages/SmokePing.jsx
import React, { useEffect } from "react";

const SmokePing = () => {
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/auth/check`, {
      credentials: "include", // Only needed if you’re using cookies
    })
      .then((res) => {
        console.log("Smoke Test Response Status:", res.status);
        return res.json();
      })
      .then((data) => {
        console.log("Smoke Test Response Data:", data);
      })
      .catch((err) => {
        console.error("Smoke Test Error:", err);
      });
  }, []);

  return <div>Running Smoke Test... Check your console</div>;
};

export default SmokePing;

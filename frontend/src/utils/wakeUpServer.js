// /frontend/src/utils/wakeUpServer.js
import { toast } from "react-toastify";

/**
 * Pings the backend to wake it up. Shows a toast if it takes longer than 1 second.
 * @param {number} timeout - Max wait time before aborting (default: 10s)
 */
export async function wakeUpServer(timeout = 10000) {
  if (import.meta.env.DEV) return; // Skip in local dev

  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  let toastId = null;
  const delayBeforeToast = 1000; // 1 second delay before showing toast

  const timer = setTimeout(() => {
    toastId = toast.info("Waking up server... please wait", { autoClose: false });
  }, delayBeforeToast);

  try {
    await fetch(`${import.meta.env.VITE_API_URL}/docs`, {
      method: "GET",
      mode: "no-cors",
      signal: controller.signal,
    });
  } catch (err) {
    console.warn("[wakeUpServer] Wake-up failed (ignored):", err);
  } finally {
    clearTimeout(timer);
    clearTimeout(id);
    if (toastId) toast.dismiss(toastId);
  }
}

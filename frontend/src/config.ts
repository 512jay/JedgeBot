// /frontend/src/config.ts
// Centralized access to Vite environment variables with TypeScript support

interface AppConfig {
    API_URL: string;
    IS_PRODUCTION: boolean;
    // Add more keys as needed
  }
  
  export const config: AppConfig = {
    API_URL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
    IS_PRODUCTION: import.meta.env.MODE === "production",
  };
  
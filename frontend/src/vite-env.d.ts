/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    // add additional VITE_ keys as needed
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  
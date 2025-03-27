/** @type {import("eslint").Linter.Config} */
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
  ],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  settings: {
    react: {
      version: "detect",
    },
  },
  rules: {
    // your custom rules can go here
  },
  overrides: [
    {
      files: ["**/*.test.{js,jsx,ts,tsx}"],
      env: {
        vitest: true, // enables vi, test, describe, expect, etc.
      },
    },
  ],
};

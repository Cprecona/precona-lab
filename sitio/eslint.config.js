import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(js.configs.recommended, ...tseslint.configs.recommended, {
  rules: {
    complexity: ["error", 10],
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": "error",
  },
});

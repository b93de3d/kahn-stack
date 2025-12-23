import { env } from "$env/dynamic/public";
// import { writable } from "svelte/store";

export async function getCsrfToken() {
  const response = await fetch(`${env.PUBLIC_API_URL}/csrf`, {
    credentials: "include",
  });
  const data = await response.json();
  return data.csrfToken;
}

// export const csrfToken = writable<string | null>(null);

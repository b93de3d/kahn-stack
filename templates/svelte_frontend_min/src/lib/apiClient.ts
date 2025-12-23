import { create } from "apisauce";
import { env } from "$env/dynamic/public";
import { getCsrfToken } from "./stores/csrf";

const apiClient = create({
  baseURL: env.PUBLIC_API_URL,
});

apiClient.addAsyncRequestTransform(async (request) => {
  let token = await getCsrfToken();
  console.log("GOT FROM API", token);

  // if (!token) {
  //   console.log("FETCHED NEW", token);
  //   token = await fetchCsrfToken();
  // }

  request.headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": token,
    ...request.headers,
  };
  request.withCredentials = true;
});

export default apiClient;

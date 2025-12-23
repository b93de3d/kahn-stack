<script>
  import { page } from "$app/state";
  import apiClient from "$lib/apiClient";

  let token = page.params.token;
  let pending = $state(true);

  const verify = async () => {
    const res = await apiClient.post("/_allauth/browser/v1/auth/email/verify", {
      key: token,
    });
    if (res.ok) {
      pending = false;
    }
  };

  verify();
</script>

<div class="verification-container">
  <h1>Account Verification</h1>
  <p>{token}</p>
  <p>{pending ? "Verifying your email..." : "Email verified"}</p>
</div>

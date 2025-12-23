<script lang="ts">
  import { userStore } from "$lib/stores/userStore.svelte";
  let email = $state("");
  let password = $state("");
</script>

<div class="container">
  <form>
    <p style="font-size: 14px; text-align: center;">Welcome Friend</p>
    <label for="email" hidden>Email</label>
    <input bind:value={email} id="email" type="email" placeholder="Email" />
    <label for="password" hidden>Password</label>
    <input
      bind:value={password}
      id="password"
      type="password"
      placeholder="Password"
    />
    <button
      onclick={() =>
        userStore.login({
          email,
          password,
        })}>Sign In</button
    >
    <p style="font-size: 14px; text-align: center;">
      Not a member?
      <a href="/signup">Sign Up</a>
    </p>
  </form>
</div>

<style>
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100dvh;
  }
  form {
    display: flex;
    flex-direction: column;
    background-color: var(--dark-purple-6);
    padding: var(--spacing-xl);
    gap: var(--spacing-md);
    width: 90vw;
    max-width: 300px;
  }
</style>

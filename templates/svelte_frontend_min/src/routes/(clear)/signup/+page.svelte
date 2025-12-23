<script lang="ts">
  import { userStore } from "$lib/stores/userStore.svelte";

  let email = $state("");
  let password = $state("");
</script>

<div class="container">
  <form>
    <p style="font-size: 14px; text-align: center;">Create an Account</p>
    <!-- <input type="text" placeholder="Name" /> -->
    <input bind:value={email} type="email" placeholder="Email" />
    <input bind:value={password} type="password" placeholder="Password" />
    <!-- <input type="password" placeholder="Confirm Password" /> -->
    <button
      onclick={() =>
        userStore.signup({
          email,
          password,
        })}>Sign Up</button
    >
    <p style="font-size: 14px; text-align: center;">
      Already a member?
      <a href="/">Sign In</a>
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

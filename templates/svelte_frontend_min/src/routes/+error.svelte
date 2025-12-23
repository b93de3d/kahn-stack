<script lang="ts">
  import { page } from "$app/state";
</script>

<div class="container">
  <h2>{page.status}: {page?.error?.message}</h2>
  <a href="/">Go home</a>
</div>

<style>
  .container {
    min-height: 100dvh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: var(--spacing-xl);
  }
</style>
